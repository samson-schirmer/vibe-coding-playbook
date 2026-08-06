#!/usr/bin/env python3
"""Render the Excalidraw primitives used by this skill to SVG and PNG.

This renderer is intentionally self-contained: it supports rectangle, ellipse,
diamond, line, arrow, and text elements without fetching browser code.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def points_for(element: dict) -> list[tuple[float, float]]:
    x, y = element.get("x", 0), element.get("y", 0)
    points = element.get("points") or [[0, 0], [element.get("width", 0), element.get("height", 0)]]
    return [(x + point[0], y + point[1]) for point in points]


def bounds(elements: list[dict]) -> tuple[float, float, float, float]:
    values: list[tuple[float, float]] = []
    for element in elements:
        if element.get("isDeleted"):
            continue
        if element.get("type") in {"line", "arrow"}:
            values.extend(points_for(element))
        else:
            x, y = element.get("x", 0), element.get("y", 0)
            values.extend([(x, y), (x + abs(element.get("width", 0)), y + abs(element.get("height", 0)))])
    if not values:
        raise ValueError("The Excalidraw file contains no visible elements.")
    xs, ys = zip(*values)
    return min(xs), min(ys), max(xs), max(ys)


def color(element: dict, key: str, default: str) -> str:
    return element.get(key) or default


def shape_svg(element: dict) -> str:
    kind = element.get("type")
    stroke = color(element, "strokeColor", "#F2F0EA")
    fill = color(element, "backgroundColor", "transparent")
    width = element.get("strokeWidth", 2)
    x, y = element.get("x", 0), element.get("y", 0)
    w, h = abs(element.get("width", 0)), abs(element.get("height", 0))
    common = f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"'
    if kind == "rectangle":
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" {common}/>'
    if kind == "ellipse":
        return f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" {common}/>'
    if kind == "diamond":
        return f'<path d="M {x + w / 2} {y} L {x + w} {y + h / 2} L {x + w / 2} {y + h} L {x} {y + h / 2} Z" {common}/>'
    if kind in {"line", "arrow"}:
        coordinates = points_for(element)
        points = " ".join(f"{px},{py}" for px, py in coordinates)
        line = f'<polyline points="{points}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
        if kind == "line" or len(coordinates) < 2:
            return line
        (start_x, start_y), (end_x, end_y) = coordinates[-2:]
        angle = math.atan2(end_y - start_y, end_x - start_x)
        head = 12
        left = (end_x - head * math.cos(angle - 0.45), end_y - head * math.sin(angle - 0.45))
        right = (end_x - head * math.cos(angle + 0.45), end_y - head * math.sin(angle + 0.45))
        triangle = f"{end_x},{end_y} {left[0]},{left[1]} {right[0]},{right[1]}"
        return f'{line}<polygon points="{triangle}" fill="{stroke}"/>'
    if kind == "text":
        text = html.escape(element.get("text", ""))
        font_size = element.get("fontSize", 20)
        lines = text.split("\n")
        tspans = "".join(f'<tspan x="{x}" dy="{font_size * 1.25 if index else 0}">{line}</tspan>' for index, line in enumerate(lines))
        return f'<text x="{x}" y="{y + font_size}" fill="{stroke}" font-family="Arial, sans-serif" font-size="{font_size}" font-weight="{element.get("fontFamily") == 3 and 600 or 400}">{tspans}</text>'
    return ""


def render(input_path: Path, output_path: Path | None) -> tuple[Path, Path | None]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    if data.get("type") != "excalidraw" or not isinstance(data.get("elements"), list):
        raise ValueError("Expected an Excalidraw JSON object with an elements array.")
    elements = [item for item in data["elements"] if not item.get("isDeleted")]
    min_x, min_y, max_x, max_y = bounds(elements)
    padding = 80
    view_box = f"{min_x - padding} {min_y - padding} {max_x - min_x + 2 * padding} {max_y - min_y + 2 * padding}"
    background = data.get("appState", {}).get("viewBackgroundColor", "#0E0E11")
    svg_path = output_path.with_suffix(".svg") if output_path else input_path.with_suffix(".svg")
    body = "\n  ".join(filter(None, (shape_svg(element) for element in elements)))
    svg_path.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" width="1600" height="900">
  <rect x="{min_x - padding}" y="{min_y - padding}" width="{max_x - min_x + 2 * padding}" height="{max_y - min_y + 2 * padding}" fill="{background}"/>
  {body}
</svg>''', encoding="utf-8")
    png_path = svg_path.with_suffix(".png")
    if shutil.which("sips"):
        subprocess.run(["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)], check=True, capture_output=True)
        return svg_path, png_path
    return svg_path, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a supported Excalidraw diagram to SVG and PNG.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output PNG or SVG path stem.")
    args = parser.parse_args()
    output = args.output.with_suffix("") if args.output else None
    try:
        svg_path, png_path = render(args.input, output)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(svg_path)
    if png_path:
        print(png_path)
    else:
        print("PNG not created: sips is unavailable.", file=sys.stderr)


if __name__ == "__main__":
    main()
