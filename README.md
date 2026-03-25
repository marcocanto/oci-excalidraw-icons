# OCI Excalidraw Icon Pack

Single-file OCI icon library for Excalidraw.

## Contents

- `dist/OCI Icons Master.excalidrawlib`: Master icon library (all icons).
- `docs/CATALOG.md`: Searchable catalog with canonical names and aliases.
- `docs/OCI Icons Catalog.png`: Visual catalog image.

## Catalog Preview

![OCI Icons Catalog](docs/OCI%20Icons%20Catalog.png)

## Use In Obsidian Excalidraw

1. Open any Excalidraw canvas.
2. Open the Library panel.
3. Import `dist/OCI Icons Master.excalidrawlib`.
4. Search by icon name or aliases shown in `docs/CATALOG.md`.

## Update Catalog

Run from repo root:

```bash
python3 scripts/generate_catalog.py
python3 scripts/generate_catalog_canvas.py
```

Optional PNG render (requires local Excalidraw skill renderer):

```bash
cd /Users/mcanto/.codex/skills/excalibur/references
uv run python render_excalidraw.py \
  "/Users/mcanto/Vault/system/OCI-icons/oci-icons-pack-repo/docs/OCI Icons Catalog.excalidraw" \
  --output "/Users/mcanto/Vault/system/OCI-icons/oci-icons-pack-repo/docs/OCI Icons Catalog.png" \
  --width 1200 \
  --scale 1
```
