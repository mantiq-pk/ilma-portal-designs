# ILMA Design Library

One organized home for Usman's ILMA portal prototypes and product documents.

**Preview site:** <https://mantiq-pk.github.io/ilma-portal-designs/>

The library keeps the original files unchanged. HTML prototypes open in the browser, Word documents download normally, and the home page adds search, categories, and screenshot previews.

## Add a file without using code

1. Open the right folder on GitHub under [`projects`](projects): `admin`, `portals`, or `reference`.
2. Choose **Add file → Upload files**, drag in the HTML or Word file, then choose **Commit changes**.
3. Wait a few minutes. GitHub checks the upload and refreshes the preview site automatically.

You do not need to edit the home page. It finds new `.html`, `.docx`, `.pdf`, and image files automatically. If you are unsure where a file belongs, [open an “Add artifacts” request](https://github.com/mantiq-pk/ilma-portal-designs/issues/new?template=add-artifacts.yml) and attach it there.

## Where things go

| Folder | Use it for |
| --- | --- |
| `projects/admin/super-admin` | School admin and super-admin screens |
| `projects/admin/control-center` | Mantiq control-center and platform screens |
| `projects/portals/finance` | Finance manager screens |
| `projects/portals/teacher` | Teacher portal screens |
| `projects/portals/parent` | Parent portal screens |
| `projects/portals/student` | Student portal screens |
| `projects/reference/navigation` | Navigation, architecture, and product documents |

## For maintainers

```bash
python3 -m unittest discover -s tests -v
sha256sum -c migration/source-files.sha256
python3 scripts/build_site.py --output _site
npm ci
npx playwright install chromium
npm run capture-previews -- _site
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

The original import is also protected by [`migration/source-files.sha256`](migration/source-files.sha256). New uploads may be added, but changing an imported file makes the verification check fail.
