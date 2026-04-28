---
name: vscode-workspace-add
description: Create or update VS Code `.code-workspace` files with distinctive window title and border decoration under the current repository's `workspaces/` directory from a provided project path. Use when the user works on multiple VS Code projects in parallel and wants workspace files that can be opened by double-clicking or from VS Code to make project windows easier to tell apart.
---

# VS Code Workspace Add

Create workspace files for the current repository's `workspaces/` directory by using the bundled script instead of hand-writing JSON.

This is an optional companion skill for keeping multiple VS Code project windows easy to distinguish during parallel project work. It creates a base `.code-workspace` file with distinctive `window.title`, `window.border`, and related color settings.

The generated file is intended to be used by double-clicking the `.code-workspace` file or opening it from VS Code. It does not modify the target project itself; it opens the target project by absolute path.

## Workflow

1. Resolve the target project path and stop if it does not exist.
2. Derive the workspace name from the last path segment unless the user explicitly requests a different filename or title.
3. Run the bundled script from the repository where this skill is installed.
- If the repository uses `uv`: `uv run python vscode-workspace-add/scripts/create_workspace.py "<absolute-project-path>"`
- Otherwise: `python vscode-workspace-add/scripts/create_workspace.py "<absolute-project-path>"`
4. Use options when needed.
- `--name <file-stem>` changes the output filename stem.
- `--title <window-title>` changes the title prefix.
- `--border <#rrggbb>` pins the border color.
- `--overwrite` intentionally replaces an existing file.
- `--dry-run` previews the output without writing.
5. For multiple paths, run the script once per path.
6. Verify the created file contains the expected `folders.path`, `window.title`, and `window.border`.
7. Report the created workspace file path, the project path it opens, how to open it, and any overwrite or color choice.

## Defaults

- Write to `workspaces/<Name>.code-workspace`.
- Use the last path segment for both filename stem and title by default.
- Use `/` separators even on Windows.
- Generate a deterministic color theme automatically when no border color is provided.
- Keep `folders.path` as an absolute path.
- Store workspace files in the repository where the command is run, not in the target project unless the user intentionally runs it there or passes `--workspace-dir`.

## Validation

Before finishing, check all of the following:

- The target project path exists.
- The workspace file exists in `workspaces/`.
- `folders[0].path` matches the intended absolute project path.
- `window.title` begins with `[Name]`.
- `window.border` is present.
- The user can open the generated `.code-workspace` file by double-clicking it or using VS Code's workspace open flow.
