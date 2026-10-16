# ILMA Portal Designs

## Scope

This repository is a preserved design and documentation library for Usman's ILMA artifacts. It is not the School CMS frontend, backend, past-papers archive, or Mantiq landing page.

Never modify, archive, rename, transfer, or delete these protected repositories while working here:

- `mantiq-pk/ilma-school-management-system`
- `mantiq-pk/ilama-mantaq-backend`
- `mantiq-pk/past-papers`
- `mantiq-pk/mantiq-website`

## Simple repository layout

Keep everyday artifacts under `All Files`, using its seven obvious subfolders: `Super Admin`, `Control Center`, `Finance`, `Teacher`, `Parent`, `Student`, and `Documents`. Do not create deeper folders inside them.

`Old Dumb` is a browseable safety copy of all seven deleted repositories. Do not edit its contents. `Dev` contains build, test, migration, and deployment internals; nontechnical users should not need it.

## Validation

After catalog or artifact changes, run:

```bash
python3 -m unittest discover -s Dev/tests -v
python3 Dev/scripts/build_site.py --output _site
```

When preview behavior changes, also run `npm --prefix Dev ci` and `npm --prefix Dev run capture-previews -- "$PWD/_site"`. Use `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/google-chrome` on the configured Linux workstation.

The generated `_site/` directory is not committed. GitHub Actions builds and deploys it.
