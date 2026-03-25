#!/usr/bin/env python3
"""Generate markdown and JSON catalogs from OCI Icons Master library."""

from __future__ import annotations

import json
from pathlib import Path


def split_name(raw: str) -> tuple[str, list[str]]:
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    if not parts:
        return raw.strip(), []
    return parts[0], parts[1:]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    lib_path = repo_root / "dist" / "OCI Icons Master.excalidrawlib"
    docs_dir = repo_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    lib = json.loads(lib_path.read_text(encoding="utf-8"))
    items = lib.get("libraryItems", [])

    catalog: list[dict[str, object]] = []
    for idx, item in enumerate(items, start=1):
        raw_name = str(item.get("name", "")).strip()
        canonical, aliases = split_name(raw_name)
        catalog.append(
            {
                "index": idx,
                "canonical_name": canonical,
                "aliases": aliases,
                "raw_name": raw_name,
                "element_count": len(item.get("elements", [])),
                "id": item.get("id"),
            }
        )

    json_out = docs_dir / "catalog.json"
    json_out.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# OCI Icons Catalog",
        "",
        f"- Total icons: **{len(catalog)}**",
        "- Source library: `dist/OCI Icons Master.excalidrawlib`",
        "",
        "| # | Icon Name | Aliases |",
        "|---:|---|---|",
    ]
    for entry in catalog:
        aliases = ", ".join(entry["aliases"]) if entry["aliases"] else "-"
        icon_name = str(entry["canonical_name"]).replace("|", "\\|")
        aliases = aliases.replace("|", "\\|")
        lines.append(f"| {entry['index']} | {icon_name} | {aliases} |")

    md_out = docs_dir / "CATALOG.md"
    md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {md_out}")
    print(f"Wrote {json_out}")


if __name__ == "__main__":
    main()
