---
name: add-ilma-artifact
description: Add or organize HTML prototypes, Word/PDF references, or screenshots in the ILMA Design Library. Use when a user supplies new ILMA portal design artifacts or asks to move, replace, categorize, or publish them in this repository. Do not use for application code changes in the School CMS, backend, past-papers, or landing-page repositories.
---

# Add an ILMA artifact

Preserve supplied files as source material while making them discoverable in the generated catalog.

## Choose the collection

Use the artifact's intended audience and purpose:

- school admin or super-admin screen → `All Files/Super Admin/`
- Mantiq-wide control center, authentication, or platform screen → `All Files/Control Center/`
- finance screen → `All Files/Finance/`
- teacher screen → `All Files/Teacher/`
- parent screen → `All Files/Parent/`
- student screen → `All Files/Student/`
- any Word/PDF product or technical document → `All Files/Documents/`

Do not create deeper subfolders. Preserve the original filename and bytes unless the user asks for a specific correction. Do not put new work in `Old Dumb` or `Dev`.

## Add and verify

1. Copy the supplied artifact into the chosen collection.
2. Run `python3 -m unittest discover -s Dev/tests -v`.
3. Run `python3 Dev/scripts/build_site.py --output _site` and confirm the new artifact appears in `_site/catalog.json` with the expected collection and title.
4. For HTML, run `npm --prefix Dev ci` and `npm --prefix Dev run capture-previews -- "$PWD/_site"`; confirm its declared preview file exists and is non-empty.

The builder extracts an HTML `<title>` automatically and falls back to a cleaned filename. Improve the original title only when the user requests an edit to that source file.

## New collections

Prefer an existing collection. For a genuinely new audience or product area, add one `Dev/sources.json` collection with a unique path under `All Files`, a plain display title, and a short factual description.

Do not create or delete GitHub repositories, publish private material, or change deployment visibility as an implied part of adding an artifact.
