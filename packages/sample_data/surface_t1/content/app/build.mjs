// The surface artifact's one fixed build command: `node build.mjs`, run at
// the workspace against these already-resolved files. There is no install
// step here at all — no npm invocation, no registry lookup, no lifecycle
// script — because the dependency tree this script imports from
// (`node_modules/`) already ships inside the artifact as verified bytes.
// That is stronger than an offline install flag: there is nothing here that
// could reach the network or run an install hook even if it tried.
import { compile } from "svelte/compiler";
import { readFileSync, writeFileSync, mkdirSync, cpSync } from "node:fs";

mkdirSync("dist", { recursive: true });

const source = readFileSync("src/EntryPage.svelte", "utf-8");
const { js } = compile(source, { filename: "EntryPage.svelte", generate: "client" });
writeFileSync("dist/EntryPage.js", js.code);

cpSync("src/mount.js", "dist/mount.js");
// Only the browser-runtime packages are copied into the served output;
// svelte/compiler's own build-time dependencies (acorn, esrap, magic-string,
// ...) stay out of dist/ because the browser never needs them.
cpSync("node_modules/svelte", "dist/vendor/svelte", { recursive: true });
cpSync("node_modules/esm-env", "dist/vendor/esm-env", { recursive: true });
cpSync("node_modules/clsx", "dist/vendor/clsx", { recursive: true });

// Every bare specifier the compiled output and the vendored Svelte runtime
// resolve at the browser's module graph, mapped to the files just copied
// above. No bundler: the browser's own import map does this resolution.
const importMap = {
  imports: {
    "svelte": "./vendor/svelte/src/index-client.js",
    "svelte/internal/client": "./vendor/svelte/src/internal/client/index.js",
    "svelte/internal/disclose-version": "./vendor/svelte/src/internal/disclose-version.js",
    "svelte/internal/flags/legacy": "./vendor/svelte/src/internal/flags/legacy.js",
    "#client/constants": "./vendor/svelte/src/internal/client/constants.js",
    "esm-env": "./vendor/esm-env/index.js",
    "esm-env/browser": "./vendor/esm-env/true.js",
    "esm-env/development": "./vendor/esm-env/false.js",
    "esm-env/node": "./vendor/esm-env/false.js",
    "clsx": "./vendor/clsx/dist/clsx.mjs"
  }
};

const html = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Legible Entry Surface</title>
<script type="importmap">${JSON.stringify(importMap, null, 2)}</script>
</head>
<body>
<div id="app"></div>
<script type="module" src="./mount.js"></script>
</body>
</html>
`;
writeFileSync("dist/index.html", html);
console.log("built dist/index.html");
