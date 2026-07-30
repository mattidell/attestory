"""Track 1 — build the resolved surface artifact offline, then open it.

This proves the two steps the resolver test above does not: that the
verified content actually builds into a working page with no network and no
install-time lifecycle script, and that the built page opens through the
live-viewing vehicle (ADR-0047) against a synthetic workspace capability.

Node is a workspace precondition this project does not ship or install
(see the milestone plan's open question 2); CI has no Node toolchain, so
every test here is skipped, not failed, when `node` is absent. That is a
real gap, not a simulated one: this file is the only place the offline build
and the vehicle launch are exercised as committed, automated evidence. A
human running this locally with Node and Chrome present gets the full proof;
CI gets the resolver's pure-Python guarantees only.

The network-off proof uses `sandbox-exec`, which is macOS-only and
deprecated upstream. On any other platform the build still runs (offline in
fact, since the vendored tree ships as literal files and the build script
never invokes a package manager), but the *enforcement* is unverified there
— an honest limitation, not an assumption.
"""

from __future__ import annotations

import http.server
import platform
import shutil
import subprocess
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from packages.derivation.live_viewing import LiveViewingVehicle
from packages.derivation.live_workspace import WorkspaceCapability, bootstrap_workspace
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.surface_resolver import ResolvedSurface, resolve_surface_artifact

REPO = Path(__file__).resolve().parent.parent
SURFACE_T1 = REPO / "packages" / "sample_data" / "surface_t1"
CONTENT_DIR = SURFACE_T1 / "content" / "app"

SCOPE_USER = "demo.user.filer-1"
CLEAN_SCOPE = {"jurisdiction": "us", "year": "2025"}

# The vendored dependency tree ships in the surface artifact but is not stored
# in this repository (owner decision 2026-07-28, see .gitignore). Restore it with
# `npm ci` in the content directory before running these.
_VENDORED = (CONTENT_DIR / "node_modules").is_dir()
_NEEDS_VENDORED = "vendored dependency tree absent; run `npm ci` in packages/sample_data/surface_t1/content/app"

_NODE = shutil.which("node")
_SANDBOX_EXEC = shutil.which("sandbox-exec") if platform.system() == "Darwin" else None
_BROWSER = next(
    (
        str(p)
        for p in (
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/chromium"),
        )
        if p.is_file()
    ),
    None,
)

_DENY_NETWORK_PROFILE = """(version 1)
(deny default)
(allow process-fork)
(allow process-exec)
(allow file-read*)
(allow file-write* (subpath (param "WORKSPACE")))
(allow sysctl-read)
(allow mach-lookup)
(allow signal (target self))
(deny network*)
"""


def _resolve() -> ResolvedSurface:
    import json

    act = json.loads((SURFACE_T1 / "adoptions" / "adopt-surface-entry-page-v1.json").read_text())
    surface = PublicationSurface(
        release_dir=SURFACE_T1 / "publication_surface" / "releases",
        package_registry_path=SURFACE_T1 / "registry" / "published-surface-artifacts.json",
        member_dir=SURFACE_T1 / "manifest",
    )
    r = resolve_surface_artifact(
        [act], run_scope=CLEAN_SCOPE, scope_user=SCOPE_USER, workspace_revision=10,
        surface=surface, content_dir=CONTENT_DIR,
    )
    assert isinstance(r, ResolvedSurface), r
    return r


@unittest.skipUnless(_NODE and _VENDORED, "needs Node (a workspace precondition) and the vendored tree; " + _NEEDS_VENDORED)
class OfflineBuild(unittest.TestCase):
    def test_verified_content_builds_offline_into_a_served_page(self) -> None:
        resolved = _resolve()
        with TemporaryDirectory(prefix="demo-surface-build-") as tmp:
            build_dir = (Path(tmp) / "app").resolve()
            shutil.copytree(resolved.content_dir, build_dir)

            command = resolved.manifest["build_command"].split()
            if _SANDBOX_EXEC:
                argv = [_SANDBOX_EXEC, "-D", f"WORKSPACE={build_dir}", "-p", _DENY_NETWORK_PROFILE, *command]
            else:
                argv = command
            result = subprocess.run(argv, cwd=build_dir, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)

            entrypoint = build_dir / resolved.manifest["entrypoint_html"]
            self.assertTrue(entrypoint.is_file())
            html = entrypoint.read_text("utf-8")
            self.assertIn("importmap", html)
            self.assertIn("Legible Entry Surface", html)

    @unittest.skipUnless(_SANDBOX_EXEC, "sandbox-exec network confinement is macOS-only")
    def test_a_real_network_attempt_is_actually_blocked_under_the_same_profile(self) -> None:
        # Proves the sandbox profile used above is not a no-op: a script that
        # tries to reach the network under it is refused, not silently allowed.
        assert _NODE is not None and _SANDBOX_EXEC is not None
        with TemporaryDirectory(prefix="demo-surface-netcheck-") as tmp:
            probe = (
                "fetch('http://example.com').then(()=>process.exit(0))"
                ".catch(()=>process.exit(7))"
            )
            argv = [_SANDBOX_EXEC, "-D", f"WORKSPACE={Path(tmp).resolve()}", "-p", _DENY_NETWORK_PROFILE, _NODE, "-e", probe]
            result = subprocess.run(argv, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 7, result.stdout + result.stderr)


@unittest.skipUnless(_NODE and _BROWSER and _VENDORED, "requires Node, a local Chrome/Chromium, and the vendored tree; " + _NEEDS_VENDORED)
class OpenInTheViewingVehicle(unittest.TestCase):
    def test_built_page_opens_through_the_viewing_vehicle_on_a_synthetic_workspace(self) -> None:
        resolved = _resolve()
        with TemporaryDirectory(prefix="demo-surface-build-") as build_tmp, \
             TemporaryDirectory(prefix="demo-surface-workspace-") as ws_tmp:
            build_dir = (Path(build_tmp) / "app").resolve()
            shutil.copytree(resolved.content_dir, build_dir)
            command = resolved.manifest["build_command"].split()
            argv = (
                [_SANDBOX_EXEC, "-D", f"WORKSPACE={build_dir}", "-p", _DENY_NETWORK_PROFILE, *command]
                if _SANDBOX_EXEC
                else command
            )
            result = subprocess.run(argv, cwd=build_dir, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            dist = build_dir / "dist"

            # A synthetic capability, outside the repository, is the only
            # thing the vehicle is handed — never a real residency.
            workspace_location = Path(ws_tmp) / "L"
            live_workspace = bootstrap_workspace(WorkspaceCapability(workspace_location), repo_root=REPO)
            self.assertTrue(live_workspace.location.is_dir())

            httpd = http.server.ThreadingHTTPServer(
                ("127.0.0.1", 0), lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(dist), **kw)
            )
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                port = httpd.server_address[1]
                url = f"http://127.0.0.1:{port}/index.html"
                vehicle = LiveViewingVehicle()
                session = vehicle.launch(
                    WorkspaceCapability(workspace_location),
                    chrome_executable=_BROWSER,
                    launch_timeout_seconds=10.0,
                    initial_url=url,
                )
                try:
                    self.assertTrue(session.websocket_url.startswith("ws://127.0.0.1:"))
                    self.assertEqual(session.navigate(url), url)
                finally:
                    session.close()
            finally:
                httpd.shutdown()
                thread.join(timeout=5)
                httpd.server_close()


if __name__ == "__main__":
    unittest.main()
