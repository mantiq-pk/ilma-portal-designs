---
name: add-ilma-artifact
description: Add or organize HTML prototypes, Word/PDF references, or screenshots in the ILMA Design Library. Use when a user supplies new ILMA portal design artifacts or asks to move, replace, categorize, or publish them in this repository. Do not use for application code changes in the School CMS, backend, past-papers, or landing-page repositories.
---

# Add an ILMA artifact

Preserve supplied files as source material while making them discoverable in the generated catalog.

## Choose the collection

Use the artifact's intended audience and purpose:

- school admin or super-admin workflow → `projects/admin/super-admin/`
- Mantiq-wide control center, authentication, or platform operation → `projects/admin/control-center/`
- finance manager → `projects/portals/finance/`
- teacher → `projects/portals/teacher/`
- parent → `projects/portals/parent/`
- student → `projects/portals/student/`
- navigation, architecture, product, or technical reference → `projects/reference/navigation/`

Keep meaningful folders supplied by the user. Preserve the original filename and bytes unless the user asks for a specific correction. Do not deduplicate similar files automatically; visual variants can be intentional.

## Add and verify

1. Copy the supplied artifact into the chosen collection.
2. Do not add new files to `migration/source-files.sha256`; it is the immutable pre-consolidation inventory. If replacing an original by explicit request, update its one checksum entry and record the reason in the commit.
3. Run `sha256sum -c migration/source-files.sha256` to prove all other originals remain intact.
4. Run `python3 -m unittest discover -s tests -v`.
5. Run `python3 scripts/build_site.py --output _site` and confirm the new artifact appears in `_site/catalog.json` with the expected collection and title.
6. For HTML, run `npm ci` and `npm run capture-previews -- _site`; confirm its declared preview file exists and is non-empty.

The builder extracts an HTML `<title>` automatically and falls back to a cleaned filename. Improve the original title only when the user requests an edit to that source file.

## New collections

Prefer an existing collection. For a genuinely new audience or product area, add one `sources.json` collection with a unique `path`, a plain display `title`, a short factual `description`, and source provenance when one exists. The path must stay under `projects/`.

Do not create or delete GitHub repositories, publish private material, or change deployment visibility as an implied part of adding an artifact.
