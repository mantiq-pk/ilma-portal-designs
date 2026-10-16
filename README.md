# ILMA Design Library

Usman's simple home for ILMA screens and documents.

**Preview site:** <https://mantiq-pk.github.io/ilma-portal-designs/>

HTML screens open in the browser. Word documents download normally. The preview website adds search and picture previews.

## Add a file without using code

1. Open one of the simple folders below.
2. Choose **Add file → Upload files**, drag in the HTML or Word file, then choose **Commit changes**.
3. Wait a few minutes. GitHub checks the upload and refreshes the preview site automatically.

You do not need to edit the home page. It finds new `.html`, `.docx`, `.pdf`, and image files automatically. If you are unsure where a file belongs, [open an “Add artifacts” request](https://github.com/mantiq-pk/ilma-portal-designs/issues/new?template=add-artifacts.yml) and attach it there.

## Only three folders

| Folder | Use it for |
| --- | --- |
| [`All Files`](All%20Files) | The easy everyday area: Super Admin, Control Center, Finance, Teacher, Parent, Student, and Documents |
| [`Old Dumb`](Old%20Dumb) | Untouched folders from all seven old repositories; keep as a backup |
| [`Dev`](Dev) | Technical automation; Usman can ignore it |

Usman only needs **All Files**. Open its matching subfolder and upload there.

## For maintainers

```bash
python3 -m unittest discover -s Dev/tests -v
python3 Dev/scripts/build_site.py --output _site
npm --prefix Dev ci
npx --prefix Dev playwright install chromium
npm --prefix Dev run capture-previews -- "$PWD/_site"
```

On systems where Playwright cannot install Chromium, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` to a local Chrome executable before the final command.

The repository-local `add-ilma-artifact` skill explains the safe import workflow for Codex and other compatible agents.

## Backups and recovery

The GitHub release named `pre-consolidation-backup-2026-10-16` contains:

- a plain ZIP of all seven original repositories;
- one full-history Git bundle for each original repository;
- exported GitHub metadata; and
- `SHA256SUMS.txt` for verification.

To restore a repository from a bundle:

```bash
git clone ILMA-Teacher-Portal.bundle ILMA-Teacher-Portal
```

To check downloaded backups:

```bash
sha256sum -c SHA256SUMS.txt
```

The browseable [`Old Dumb`](Old%20Dumb) folder and the release both preserve the original seven repositories.
