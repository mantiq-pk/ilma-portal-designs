# ILMA Portal Designs Consolidation

## Intent

Usman's seven small repositories are a design library, not seven independently deployed applications. Consolidate them into one approachable repository that preserves every original artifact, makes every HTML mockup easy to browse, and can grow without Usman needing to understand a build system.

## Scope

Only repositories whose first commits were authored by GitHub user `mianusmanghani053-del` are in scope:

- `ILMA-Artifacts-Super-Admin-and-Admin`
- `Al-Mantiq-Control-Center-Admin-Portal-`
- `Main-Modules-of-ILMA-Users-Navigation`
- `ILMA-Artifacts-Finance-Manager`
- `ILMA-Teacher-Portal`
- `ILMA-Parent-Portal`
- `ILMA-Student-Portal`

The following repositories are explicitly protected and must not be modified, archived, renamed, transferred, or deleted:

- `ilma-school-management-system`
- `ilama-mantaq-backend`
- `past-papers`
- `mantiq-website`

## Outcome

Create `mantiq-pk/ilma-portal-designs` as the single home for Usman's work. Import the default-branch files into seven clearly named collection folders, retain original filenames and bytes, and add a generated GitHub Pages catalog with screenshots, search, category filters, and direct links to the untouched HTML mockups and documents.

## Information Architecture

```text
projects/
  admin/super-admin/
  admin/control-center/
  portals/finance/
  portals/teacher/
  portals/parent/
  portals/student/
  reference/navigation/
```

`sources.json` records the original repository URL, source commit, destination folder, category, display name, and description for each collection. Imported files are immutable source artifacts: improvements belong in the catalog shell, not in the original HTML.

## Preview Experience

The master page is a quiet, searchable library rather than another dashboard mockup. It uses an ink/navy and paper-blue palette drawn from ILMA's existing prototypes, a practical humanist sans-serif, a slim collection rail, and large preview canvases that let the artifacts carry the visual interest.

- Base ink: `#102A43`
- Deep navy: `#0B1F33`
- Paper: `#F4F8FC`
- White: `#FFFFFF`
- ILMA blue: `#2563EB`
- Focus gold: `#E3A008`
- Type: `Manrope` when available, with a system sans-serif fallback
- Layout: left-aligned title and controls, responsive collection grid, landscape screenshot thumbnails
- Memorable element: a contact-sheet-style preview wall of the actual prototypes

The site reads a generated `catalog.json`. Each HTML file becomes a preview card with an automatically generated screenshot and an "Open preview" link. Word documents become download cards. Search covers artifact title, collection, category, and filename. Filters cover Admin, Portals, and Reference.

## Maintenance

Usman can use GitHub's web UI to upload a file into the relevant folder under `projects/`; deployment discovers HTML and Word files automatically. No manifest edit is needed for files added to an existing collection. A short README gives three plain-language steps. A repository-local `add-ilma-artifact` skill gives future agents the exact placement, preservation, build, and validation rules.

Adding a genuinely new collection requires one entry in `sources.json`; the catalog derives everything else. Unknown folders and filenames are converted into readable labels automatically.

## Deployment

GitHub Actions builds `_site`, captures thumbnails with Playwright, uploads the Pages artifact, and deploys on every push to `main`. Because the organization is on GitHub Free, GitHub Pages requires the consolidated repository to be public. A credential scan must pass before repository publication. The Pages artifact contains the catalog and imported project files, but not backup bundles or migration metadata.

## Backup and Deletion Safety

Before deleting any source repository:

1. Create a plain ZIP containing all seven default-branch working trees under their original repository names.
2. Create one Git bundle per repository from a full mirror so all branches, tags, and commit history can be restored.
3. Export available GitHub metadata (repository settings, issues, pull requests, releases, branches, and tags) to JSON.
4. Generate SHA-256 checksums and verify the ZIP and every bundle.
5. Attach all backup files to a release in the consolidated repository.
6. Clone the consolidated repository afresh, download the release assets, verify checksums, and confirm the Pages deployment succeeds.
7. Delete only the seven named source repositories, then query the organization repository list to confirm the four protected repositories remain.

GitHub Actions secrets and other write-only settings cannot be exported; discovery found these repositories to be static artifact stores with no application configuration.

## Non-goals

- Do not merge these prototypes into the School CMS application.
- Do not change behavior or styling inside the original HTML mockups.
- Do not deduplicate repeated mockups; repeated files are part of the preserved source state.
- Do not rewrite Word documents.
- Do not alter the protected frontend, backend, past-papers, or landing-page repositories.

## Success Criteria

- All seven source HEADs and every default-branch file are represented in `sources.json` and the imported inventory.
- Original imported files match their source SHA-256 hashes.
- Every HTML artifact opens directly and has a generated thumbnail.
- Every Word document is available for download.
- Catalog search and category filters work on desktop and mobile with keyboard-visible focus.
- The public Pages URL is live.
- Backup ZIP, Git bundles, metadata export, and checksum file are downloadable from a release and independently verified.
- Only after those checks, the seven source repositories are deleted and the four protected repositories remain unchanged.
