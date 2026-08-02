// Fixed offline build command for the adopted synthetic entry surface.
import { compile } from "svelte/compiler";
import {
  cpSync,
  mkdirSync,
  readFileSync,
  writeFileSync
} from "node:fs";

mkdirSync("dist", { recursive: true });

const source = readFileSync("src/EntryPage.svelte", "utf-8");
const { js, css } = compile(source, {
  filename: "EntryPage.svelte",
  generate: "client"
});
writeFileSync("dist/EntryPage.js", js.code);
writeFileSync("dist/styles.css", css.code);
cpSync("src/mount.js", "dist/mount.js");
cpSync("src/w2-box1-format.js", "dist/w2-box1-format.js");
cpSync("src/w2-box1-field.js", "dist/w2-box1-field.js");

const workspaceSource = readFileSync("src/WorkspacePage.svelte", "utf-8");
const workspaceCompiled = compile(workspaceSource, {
  filename: "WorkspacePage.svelte",
  generate: "client"
});
writeFileSync("dist/WorkspacePage.js", workspaceCompiled.js.code);
writeFileSync("dist/workspace-styles.css", workspaceCompiled.css.code);
cpSync("src/mount-workspace.js", "dist/mount-workspace.js");
cpSync("node_modules/svelte", "dist/vendor/svelte", { recursive: true });
cpSync("node_modules/esm-env", "dist/vendor/esm-env", { recursive: true });
cpSync("node_modules/clsx", "dist/vendor/clsx", { recursive: true });

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
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>W-2 entry · Attestory</title>
<link rel="stylesheet" href="./styles.css">
<script type="importmap">${JSON.stringify(importMap, null, 2)}</script>
</head>
<body>
<div id="app"></div>
<script type="module" src="./mount.js"></script>
</body>
</html>
`;
writeFileSync("dist/index.html", html);

const workspaceHtml = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>Workspace · Attestory</title>
<link rel="stylesheet" href="./workspace-styles.css">
<script type="importmap">${JSON.stringify(importMap, null, 2)}</script>
</head>
<body>
<div id="app"></div>
<script type="module" src="./mount-workspace.js"></script>
</body>
</html>
`;
writeFileSync("dist/workspace.html", workspaceHtml);
