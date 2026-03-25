#!/usr/bin/env python3
"""Generate an Excalidraw catalog canvas from OCI Icons Master library."""

from __future__ import annotations

import copy
import json
from pathlib import Path


def visible_bounds(element: dict) -> tuple[float, float, float, float]:
    x = float(element.get("x", 0))
    y = float(element.get("y", 0))
    if element.get("type") == "line":
        points = element.get("points") or []
        if points:
            xs = [x + float(p[0]) for p in points]
            ys = [y + float(p[1]) for p in points]
            return min(xs), min(ys), max(xs), max(ys)
    w = float(element.get("width", 0))
    h = float(element.get("height", 0))
    return x, y, x + w, y + h


def shift_element(element: dict, dx: float, dy: float) -> None:
    element["x"] = round(float(element.get("x", 0)) + dx, 2)
    element["y"] = round(float(element.get("y", 0)) + dy, 2)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    lib_path = repo_root / "dist" / "OCI Icons Master.excalidrawlib"
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    lib = json.loads(lib_path.read_text(encoding="utf-8"))
    items = lib.get("libraryItems", [])

    cols = 8
    tile_w = 620
    tile_h = 620
    pad_x = 40
    pad_y = 40

    all_elements: list[dict] = []

    for idx, item in enumerate(items):
        elements = copy.deepcopy(item.get("elements", []))
        if not elements:
            continue

        bounds = [visible_bounds(e) for e in elements]
        min_x = min(b[0] for b in bounds)
        min_y = min(b[1] for b in bounds)
        max_x = max(b[2] for b in bounds)
        max_y = max(b[3] for b in bounds)
        width = max_x - min_x
        height = max_y - min_y

        row = idx // cols
        col = idx % cols
        cell_x = col * tile_w + pad_x
        cell_y = row * tile_h + pad_y

        dx = cell_x + (tile_w - 2 * pad_x - width) / 2 - min_x
        dy = cell_y + (tile_h - 2 * pad_y - height) / 2 - min_y

        for e in elements:
            shift_element(e, dx, dy)
            all_elements.append(e)

    scene = {
        "type": "excalidraw",
        "version": 2,
        "source": "oci-icons-pack-catalog",
        "elements": all_elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }

    out = docs_dir / "OCI Icons Catalog.excalidraw"
    out.write_text(json.dumps(scene, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Elements: {len(all_elements)}")


if __name__ == "__main__":
    main()
