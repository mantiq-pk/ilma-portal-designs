#!/usr/bin/env python3
"""Build the static ILMA design catalog from preserved source artifacts."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote


PUBLISHABLE_KINDS = {
    ".html": "prototype",
    ".docx": "document",
    ".pdf": "document",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
}


def humanize_filename(path: Path) -> str:
    value = path.stem.replace("_", " ").replace("-", " ")
    value = re.sub(r"\b(?:redesign\s+)?mockup\b", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip(" .–—")
    return value or "Untitled artifact"


def html_title(path: Path) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if not match:
        return humanize_filename(path)
    title = re.sub(r"<[^>]+>", "", match.group(1))
    title = re.sub(r"\s+", " ", html.unescape(title)).strip()
    return title or humanize_filename(path)


def artifact_id(relative_path: Path) -> str:
    return hashlib.sha256(relative_path.as_posix().encode("utf-8")).hexdigest()[:16]


def build_site(repo_root: Path, output_dir: Path) -> dict:
    repo_root = Path(repo_root).resolve()
    output_dir = Path(output_dir).resolve()
    sources = json.loads((repo_root / "sources.json").read_text(encoding="utf-8"))

    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(repo_root / "site", output_dir)
    shutil.copytree(repo_root / "projects", output_dir / "projects")

    items = []
    collections = []
    for collection in sources["collections"]:
        collection_root = repo_root / collection["path"]
        count = 0
        for artifact in sorted(collection_root.rglob("*")):
            if not artifact.is_file():
                continue
            kind = PUBLISHABLE_KINDS.get(artifact.suffix.lower())
            if not kind:
                continue
            relative_path = artifact.relative_to(repo_root)
            title = html_title(artifact) if kind == "prototype" else humanize_filename(artifact)
            item = {
                    "id": artifact_id(relative_path),
                    "title": title,
                    "kind": kind,
                    "category": collection["category"],
                    "collection": collection["title"],
                    "collectionPath": collection["path"],
                    "description": collection["description"],
                    "filename": artifact.name,
                    "url": quote(relative_path.as_posix(), safe="/"),
                }
            if kind == "prototype":
                item["preview"] = f"previews/{item['id']}.webp"
            items.append(item)
            count += 1
        collections.append({**collection, "artifactCount": count})

    kind_order = {"prototype": 0, "image": 1, "document": 2}
    items.sort(
        key=lambda item: (
            kind_order[item["kind"]],
            item["title"].casefold(),
            item["url"],
        )
    )
    catalog = {
        "schemaVersion": 1,
        "collections": collections,
        "items": items,
        "stats": {
            "collections": len(collections),
            "artifacts": len(items),
            "prototypes": sum(item["kind"] == "prototype" for item in items),
            "documents": sum(item["kind"] == "document" for item in items),
            "images": sum(item["kind"] == "image" for item in items),
        },
    }
    (output_dir / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("_site"))
    args = parser.parse_args()
    catalog = build_site(args.repo_root, args.output)
    print(
        f"Built {catalog['stats']['artifacts']} artifacts "
        f"from {catalog['stats']['collections']} collections."
    )


if __name__ == "__main__":
    main()
