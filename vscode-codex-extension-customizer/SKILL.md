---
name: vscode-codex-extension-customizer
description: Re-evaluate the latest VS Code Codex extension after an update, reapply this user's personal customizations for first-line thread titles and 20-task sidebar display when needed, and record project-specific application history under docs/. Use when the user says the Codex VS Code extension updated, behavior changed, the customizations may have been reset, or they want to apply the same customization on another Windows or Mac machine. Designed to work reliably even with low reasoning effort.
---

# VS Code Codex Extension Customizer

Use this skill when the user wants the latest installed VS Code Codex extension checked and, if needed, customized to preserve this user's personal workflow.

This is not an official extension setting. It is a local, user-owned customization applied directly to the installed VS Code extension files.

## Low-Cost Workflow

1. Resolve the installed extension root for the current machine. Do not hard-code the original Windows path when working on another PC.
- Windows default: `%USERPROFILE%/.vscode/extensions`
- macOS default: `$HOME/.vscode/extensions`
- If VS Code uses a different extensions directory, confirm it from the environment before editing.
2. Inspect only the latest `openai.chatgpt-*` extension directory under the resolved extension root.
3. Check only these two latest-extension targets first.
- `out/extension.js`
- `webview/assets/index-*.js`
4. In `out/extension.js`, verify whether `generate-thread-title` already contains the first-line title branch:
- `split(/\r?\n/,1)[0]`
- `return{title:n}`
5. In the latest `index-*.js`, verify whether the Tasks sidebar still shows only 3 items:
- look for `slice(0,Math.max(3,e.length))`
- if present, change it to `slice(0,Math.max(20,e.length))`
6. If the exact `slice(0,Math.max(...))` pattern is absent, inspect the sidebar list implementation around `sidebarElectron.showMore` and the `maxItems:` props. Newer builds may use minified constants instead of the old inline slice. In that case:
- identify the constants passed to `maxItems:` for grouped project chats and recent chats
- back up the current `index-*.js`
- change only those display-count constants to `20`
- record the exact constants changed in the docs log
7. Before changing either file, create dated backups beside the originals:
- `extension.js.bak-YYYY-MM-DD`
- `index-*.js.bak-YYYY-MM-DD`
8. Reapply only the minimal string replacements needed for the current version.
9. Record project-specific work under the target project's `docs/` directory. Prefer an existing extension-customizer history document; otherwise create one such as `docs/VSCODE_CODEX_EXTENSION_CUSTOMIZER_APPLY_LOG.md`.
10. For each application run, append a new entry instead of rewriting past entries. Include:
- date
- target OS and machine context when known; keep Windows and macOS runs distinguishable in the entry text
- resolved extension folder
- extension version
- files changed
- backup files created
- validation results
- issues, risks, or follow-up tasks for that run
11. Finish with a short report: changed files, why, impact, and `Developer: Reload Window`.

## Cross-Machine Notes

- Use `/` separators in documentation and chat file references even on Windows.
- On macOS, expect the installed extension directory to live under the current user's home directory, for example `$HOME/.vscode/extensions/openai.chatgpt-<version>-darwin-*`. The exact suffix can vary, so discover it from the filesystem.
- On Windows, expect paths like `C:/Users/<user>/.vscode/extensions/openai.chatgpt-<version>-win32-x64`.
- Do not assume the username, CPU architecture, or extension version from this repository's history.
- Treat all extension-file edits as user-environment-wide changes, not project-local changes.

## Required Checks

- Confirm the latest installed extension version.
- Confirm the current OS and resolved extension root.
- Confirm whether the title customization is missing before patching.
- Confirm whether the Tasks sidebar display customization is missing before patching.
- Confirm backups exist after patching.
- Confirm the target project's `docs/` entry records the latest extension version, backup date, validation results, and per-run issues or follow-up tasks.

## Required Output Style

- Keep the workflow tight and deterministic.
- Prefer short status updates and concise final reporting.
- Do not re-read the entire history when the latest version plus current doc references are enough.
- Assume Low reasoning effort should still succeed by following the fixed checklist above.

## Validation

Before finishing, check all of the following:

- The latest extension folder was identified.
- The extension folder path matches the current machine, not a stale path copied from this repository.
- `out/extension.js` contains the first-line title branch after patching.
- The latest `index-*.js` contains either `slice(0,Math.max(20,e.length))` and no longer contains `slice(0,Math.max(3,e.length))`, or the current build's sidebar `maxItems:` constants have been changed to `20` and the former lower constants are absent.
- Both dated backup files exist.
- A project-specific document under `docs/` records the run.
- The `docs/` entry includes the extension version, changed files, backup files, validation results, and issues or follow-up tasks for that application.
