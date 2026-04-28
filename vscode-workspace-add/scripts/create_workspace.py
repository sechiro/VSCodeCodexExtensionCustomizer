from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import re
import sys
from pathlib import Path

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}")
WINDOW_TITLE_TEMPLATE = "[{title}] ${{dirty}}${{activeEditorShort}}${{separator}}${{rootName}}${{separator}}${{appName}}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a VS Code .code-workspace file.")
    parser.add_argument("project_path", help="Target project path to open in the workspace")
    parser.add_argument("--workspace-dir", default="workspaces", help="Directory that stores .code-workspace files")
    parser.add_argument("--name", help="Output filename stem without .code-workspace")
    parser.add_argument("--title", help="Window title prefix without brackets")
    parser.add_argument("--border", help="Border color in #rrggbb format")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing workspace file")
    parser.add_argument("--dry-run", action="store_true", help="Print the workspace JSON without writing a file")
    return parser.parse_args()


def sanitize_name(value: str) -> str:
    name = value.strip()
    if name.lower().endswith(".code-workspace"):
        name = name[: -len(".code-workspace")]
    name = re.sub(r'[<>:"/\\|?*]+', "_", name)
    name = name.strip()
    return name or "Workspace"


def as_posix(path: Path) -> str:
    return path.resolve().as_posix()


def hex_from_hls(hue: float, lightness: float, saturation: float) -> str:
    red, green, blue = colorsys.hls_to_rgb((hue % 360.0) / 360.0, lightness, saturation)
    return f"#{round(red * 255):02x}{round(green * 255):02x}{round(blue * 255):02x}"


def hue_from_hex(color: str) -> float:
    red = int(color[1:3], 16) / 255.0
    green = int(color[3:5], 16) / 255.0
    blue = int(color[5:7], 16) / 255.0
    hue, _, _ = colorsys.rgb_to_hls(red, green, blue)
    return hue * 360.0


def with_alpha(color: str, alpha: str) -> str:
    return f"{color}{alpha.lower()}"


def collect_used_borders(workspace_dir: Path) -> set[str]:
    used: set[str] = set()
    if not workspace_dir.exists():
        return used
    for workspace_file in workspace_dir.glob("*.code-workspace"):
        try:
            payload = json.loads(workspace_file.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        border = payload.get("settings", {}).get("window.border")
        if isinstance(border, str) and HEX_COLOR_RE.fullmatch(border):
            used.add(border.lower())
    return used


def choose_hue(seed_text: str, used_borders: set[str]) -> float:
    seed = int(hashlib.sha1(seed_text.encode("utf-8")).hexdigest()[:8], 16) % 360
    for offset in range(0, 360, 17):
        hue = (seed + offset) % 360
        border = hex_from_hls(hue, 0.48, 0.84)
        if border.lower() not in used_borders:
            return float(hue)
    return float(seed)


def build_palette(seed_text: str, used_borders: set[str], border_override: str | None) -> dict[str, str]:
    if border_override is not None:
        border = border_override.lower()
        hue = hue_from_hex(border)
    else:
        hue = choose_hue(seed_text, used_borders)
        border = hex_from_hls(hue, 0.48, 0.84)

    title_bg = hex_from_hls(hue, 0.22, 0.65)
    activity_bg = hex_from_hls(hue, 0.30, 0.72)
    status_bg = hex_from_hls(hue, 0.38, 0.78)
    accent = hex_from_hls(hue, 0.72, 0.92)
    badge_fg = hex_from_hls(hue, 0.14, 0.72)
    foreground = "#f8fafc"
    inactive_foreground = "#e2e8f0cc"

    return {
        "window.activeBorder": border,
        "window.inactiveBorder": with_alpha(border, "66"),
        "titleBar.activeBackground": title_bg,
        "titleBar.inactiveBackground": with_alpha(title_bg, "99"),
        "titleBar.activeForeground": foreground,
        "titleBar.inactiveForeground": inactive_foreground,
        "activityBar.background": activity_bg,
        "activityBar.foreground": foreground,
        "activityBar.activeBorder": accent,
        "activityBarBadge.background": accent,
        "activityBarBadge.foreground": badge_fg,
        "statusBar.background": status_bg,
        "statusBar.foreground": foreground,
        "statusBar.debuggingBackground": activity_bg,
        "statusBar.debuggingForeground": foreground,
    }


def build_workspace_payload(project_path: Path, title: str, palette: dict[str, str]) -> dict[str, object]:
    return {
        "folders": [
            {
                "path": as_posix(project_path),
            }
        ],
        "settings": {
            "window.title": WINDOW_TITLE_TEMPLATE.format(title=title),
            "window.titleSeparator": " | ",
            "window.border": palette["window.activeBorder"],
            "workbench.colorCustomizations": palette,
        },
    }


def main() -> int:
    args = parse_args()
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Target project path does not exist: {project_path}", file=sys.stderr)
        return 1

    workspace_dir = Path(args.workspace_dir)
    if not workspace_dir.is_absolute():
        workspace_dir = Path.cwd() / workspace_dir
    workspace_dir.mkdir(parents=True, exist_ok=True)

    name = sanitize_name(args.name or project_path.name)
    title = args.title.strip() if args.title else name
    output_path = workspace_dir / f"{name}.code-workspace"

    if args.border is not None and not HEX_COLOR_RE.fullmatch(args.border):
        print("--border must be in #rrggbb format", file=sys.stderr)
        return 1

    if output_path.exists() and not args.overwrite and not args.dry_run:
        print(f"Workspace file already exists: {output_path}", file=sys.stderr)
        return 1

    used_borders = collect_used_borders(workspace_dir)
    palette = build_palette(title, used_borders, args.border)
    payload = build_workspace_payload(project_path, title, palette)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    if args.dry_run:
        print(f"Output path: {output_path.resolve().as_posix()}")
        print(rendered, end="")
        return 0

    output_path.write_text(rendered, encoding="utf-8")
    print(f"Created: {output_path.resolve().as_posix()}")
    print(f"Project path: {as_posix(project_path)}")
    print(f"Title: [{title}]")
    print(f"Border: {palette['window.activeBorder']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
