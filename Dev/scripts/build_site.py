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


THEME_HEAD = r"""
<style id="ilma-theme-styles">
  #ilma-theme-toggle {
    all: initial;
    position: fixed;
    right: max(16px, env(safe-area-inset-right));
    bottom: max(16px, env(safe-area-inset-bottom));
    z-index: 2147483647;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 42px;
    padding: 0 14px;
    border: 1px solid rgba(15, 23, 42, 0.18);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.2);
    color: #0f172a;
    cursor: pointer;
    font: 700 13px/1 system-ui, -apple-system, "Segoe UI", sans-serif;
    -webkit-font-smoothing: antialiased;
    backdrop-filter: blur(12px);
  }
  #ilma-theme-toggle:hover { transform: translateY(-1px); }
  #ilma-theme-toggle:focus-visible { outline: 3px solid #f59e0b; outline-offset: 3px; }
  #ilma-theme-toggle .ilma-theme-icon { font-size: 17px; line-height: 1; }
  html[data-ilma-theme="dark"] { color-scheme: dark; background: #0b1220 !important; }
  html[data-ilma-theme="dark"] body { background: #0b1220 !important; }
  html[data-ilma-theme="dark"] body > :not(#ilma-theme-toggle):not(script):not(style):not(template):not(link) {
    filter: invert(0.88) hue-rotate(180deg);
  }
  html[data-ilma-theme="dark"] body img,
  html[data-ilma-theme="dark"] body video,
  html[data-ilma-theme="dark"] body canvas,
  html[data-ilma-theme="dark"] body iframe {
    filter: invert(1) hue-rotate(180deg);
  }
  html[data-ilma-theme="dark"] #ilma-theme-toggle {
    border-color: rgba(226, 232, 240, 0.25);
    background: rgba(15, 23, 42, 0.96);
    color: #f8fafc;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
  }
  @media (prefers-reduced-motion: no-preference) {
    #ilma-theme-toggle { transition: transform 140ms ease, background-color 140ms ease, color 140ms ease; }
  }
</style>
<script id="ilma-theme-bootstrap">
  (() => {
    const storageKey = "ilma-color-theme";
    const styleText = document.getElementById("ilma-theme-styles").textContent;

    function storedTheme() {
      try { return localStorage.getItem(storageKey) === "dark" ? "dark" : "light"; }
      catch (_) { return "light"; }
    }

    function applyTheme(theme, persist) {
      const dark = theme === "dark";
      document.documentElement.dataset.ilmaTheme = dark ? "dark" : "light";
      const button = document.getElementById("ilma-theme-toggle");
      if (button) {
        button.setAttribute("aria-pressed", String(dark));
        button.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
        button.querySelector(".ilma-theme-icon").textContent = dark ? "☀" : "☾";
        button.querySelector(".ilma-theme-label").textContent = dark ? "Light" : "Dark";
      }
      if (persist) {
        try { localStorage.setItem(storageKey, dark ? "dark" : "light"); } catch (_) {}
      }
    }

    function installTheme() {
      if (!document.head || !document.body) return;
      if (!document.getElementById("ilma-theme-styles")) {
        const style = document.createElement("style");
        style.id = "ilma-theme-styles";
        style.textContent = styleText;
        document.head.appendChild(style);
      }
      let button = document.getElementById("ilma-theme-toggle");
      if (!button) {
        button = document.createElement("button");
        button.id = "ilma-theme-toggle";
        button.type = "button";
        button.setAttribute("aria-pressed", "false");
        button.setAttribute("aria-label", "Switch to dark mode");
        button.innerHTML = '<span class="ilma-theme-icon" aria-hidden="true">☾</span><span class="ilma-theme-label">Dark</span>';
        document.body.appendChild(button);
      }
      if (!button.dataset.ilmaThemeBound) {
        button.dataset.ilmaThemeBound = "true";
        button.addEventListener("click", () => {
          applyTheme(document.documentElement.dataset.ilmaTheme === "dark" ? "light" : "dark", true);
        });
      }
      applyTheme(storedTheme(), false);
    }

    window.__installIlmaTheme = installTheme;
    applyTheme(storedTheme(), false);
    window.addEventListener("load", installTheme);
    window.addEventListener("storage", (event) => {
      if (event.key === storageKey) applyTheme(event.newValue === "dark" ? "dark" : "light", false);
    });
    [0, 100, 500, 1500].forEach((delay) => setTimeout(installTheme, delay));
  })();
</script>
"""


THEME_CONTROL = r"""
<script id="ilma-theme-controller">
  window.__installIlmaTheme();
</script>
"""


def inject_theme_controls(markup: str) -> str:
    """Add the universal, light-first theme control to one generated HTML page."""
    if 'id="ilma-theme-toggle"' in markup:
        return markup
    markup, html_count = re.subn(
        r"<html\b([^>]*)>",
        r'<html\1 data-ilma-theme="light">',
        markup,
        count=1,
        flags=re.IGNORECASE,
    )
    if not html_count:
        return markup
    markup, head_count = re.subn(
        r"</head>", THEME_HEAD + "\n</head>", markup, count=1, flags=re.IGNORECASE
    )
    if not head_count:
        return markup
    markup, body_count = re.subn(
        r"</body>", THEME_CONTROL + "\n</body>", markup, count=1, flags=re.IGNORECASE
    )
    return markup if body_count else markup + THEME_CONTROL


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
    system_root = repo_root / "Dev"
    sources = json.loads((system_root / "sources.json").read_text(encoding="utf-8"))

    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(system_root / "site", output_dir)

    items = []
    collections = []
    for collection in sources["collections"]:
        collection_root = repo_root / collection["path"]
        shutil.copytree(collection_root, output_dir / collection["path"])
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
    for page in output_dir.rglob("*.html"):
        page.write_text(
            inject_theme_controls(page.read_text(encoding="utf-8", errors="replace")),
            encoding="utf-8",
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
