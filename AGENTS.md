# ILMA Portal Designs

## Scope

This repository is a preserved design and documentation library for Usman's ILMA artifacts. It is not the School CMS frontend, backend, past-papers archive, or Mantiq landing page.

Never modify, archive, rename, transfer, or delete these protected repositories while working here:

- `mantiq-pk/ilma-school-management-system`
- `mantiq-pk/ilama-mantaq-backend`
- `mantiq-pk/past-papers`
- `mantiq-pk/mantiq-website`

## Source preservation

Files already listed in `migration/source-files.sha256` are imported originals. Do not reformat, rename, deduplicate, or edit them unless the user explicitly supplies a replacement for that exact artifact. New artifacts may be added without changing the original checksum inventory.

Place new work in the matching existing collection under `projects/`. Add a `sources.json` entry only for a genuinely new collection.

## Validation

After catalog or artifact changes, run:

```bash
sha256sum -c migration/source-files.sha256
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py --output _site
```

When preview behavior changes, also run `npm ci` and `npm run capture-previews -- _site`. Use `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/google-chrome` on the configured Linux workstation.

The generated `_site/` directory is not committed. GitHub Actions builds and deploys it.
