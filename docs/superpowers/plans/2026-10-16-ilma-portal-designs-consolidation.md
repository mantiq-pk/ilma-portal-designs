# ILMA Portal Designs Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate Usman's seven static artifact repositories into one preserved, searchable, previewable GitHub Pages library with verified backups.

**Architecture:** Preserve source files under categorized collection folders and generate a static catalog from `sources.json` plus filesystem discovery. A Python build copies only publishable content and emits catalog metadata; Playwright captures HTML thumbnails; GitHub Actions deploys the result. Full-history bundles and a plain ZIP live as verified release assets rather than in Git history.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 standard library, Node.js + Playwright, GitHub Actions, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-10-16-ilma-portal-designs-consolidation-design.md`

## Global Constraints

- Only the seven repositories listed in the spec are in scope.
- Never mutate `ilma-school-management-system`, `ilama-mantaq-backend`, `past-papers`, or `mantiq-website`.
- Preserve imported source artifact bytes and filenames.
- Do not delete a source repository until fresh-clone, release-backup, checksum, and Pages verification all pass.
- GitHub Pages publication requires a clean credential scan.

## Review Focus

- Unicode and spaces in filenames must produce valid, clickable preview URLs.
- Repeated artifact filenames in different collections must not overwrite each other or their screenshots.
- A malformed or missing HTML `<title>` must fall back to a readable filename.
- Adding a supported file to an existing collection must require no catalog edit.
- Build output must not include Git bundles, metadata backups, tests, or repository administration files.

---

### Task 1: Preserve and import the seven sources

**Files:**
- Create: `sources.json`
- Create: `projects/admin/super-admin/**`
- Create: `projects/admin/control-center/**`
- Create: `projects/portals/{finance,teacher,parent,student}/**`
- Create: `projects/reference/navigation/**`
- Create: `migration/source-files.sha256`

**Interfaces:**
- Consumes: the seven verified source worktrees and mirror repositories
- Produces: categorized source folders and `sources.json` entries consumed by the site builder

- [ ] Copy default-branch files without renaming or transforming them.
- [ ] Record each original repository, source HEAD, destination, category, title, and description in `sources.json`.
- [ ] Generate SHA-256 inventory entries for every imported artifact and verify them against the source worktrees.
- [ ] Commit the preserved source import.

### Task 2: Build the catalog generator with TDD

**Files:**
- Create: `tests/test_build_site.py`
- Create: `scripts/build_site.py`
- Create: `site/index.html`
- Create: `site/styles.css`
- Create: `site/app.js`

**Interfaces:**
- Consumes: `sources.json`, `projects/**`, and `site/**`
- Produces: `build_site(repo_root: Path, output_dir: Path) -> dict` and `_site/catalog.json`

- [ ] Write failing tests for Unicode URL encoding, title fallback, unique preview names, automatic file discovery, and publishable-file filtering.
- [ ] Run `python -m unittest discover -s tests -v` and verify the failures describe the missing builder.
- [ ] Implement the minimal Python builder and catalog data required by the tests.
- [ ] Run the full test suite and verify it passes.
- [ ] Build the intentional ILMA library shell in `site/`, keeping source artifacts unchanged.
- [ ] Re-run tests and commit the catalog builder and shell.

### Task 3: Generate visual previews

**Files:**
- Create: `package.json`
- Create: `package-lock.json`
- Create: `scripts/capture-previews.mjs`
- Modify: `tests/test_build_site.py`

**Interfaces:**
- Consumes: `_site/catalog.json` and `_site/projects/**/*.html`
- Produces: `_site/previews/<stable-path-hash>.webp`

- [ ] Add a failing builder test asserting the stable preview path for each HTML artifact.
- [ ] Run the focused test and verify it fails for missing preview metadata.
- [ ] Implement stable preview metadata, then add the Playwright capture script.
- [ ] Run tests, build `_site`, capture every preview, and assert every HTML catalog item has a non-empty WebP.
- [ ] Commit preview automation.

### Task 4: Make maintenance approachable

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `.agents/skills/add-ilma-artifact/SKILL.md`
- Create: `.github/ISSUE_TEMPLATE/add-artifacts.yml`
- Create: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: repository layout and build commands
- Produces: plain-language upload guidance, agent instructions, a validated repository-local skill, and pull-request checks

- [ ] Write the three-step GitHub-web upload guide and recovery notes.
- [ ] Add repository scope rules and the narrow artifact-import skill.
- [ ] Validate the skill with `quick_validate.py`.
- [ ] Add CI that verifies source checksums, runs tests, builds the catalog, and checks preview mappings.
- [ ] Run all validations locally and commit the maintenance layer.

### Task 5: Deploy the Pages site

**Files:**
- Create: `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: `main`, Python builder, Node dependencies, and GitHub Pages
- Produces: public Pages deployment for `mantiq-pk/ilma-portal-designs`

- [ ] Scan imported text and expanded DOCX XML for credentials and block publication on credible findings.
- [ ] Create the public GitHub repository, push `main`, and enable Actions-based Pages.
- [ ] Add and run the Pages workflow with build, Playwright capture, artifact upload, and deployment jobs.
- [ ] Verify the workflow conclusion is `success` and fetch the Pages URL with HTTP 200.
- [ ] Visually inspect desktop and mobile screenshots, repair defects, and commit any fixes.

### Task 6: Create and independently verify backups

**Files:**
- Create: release `pre-consolidation-backup-2026-10-16` assets

**Interfaces:**
- Consumes: seven full mirrors, seven default-branch worktrees, and GitHub API metadata
- Produces: plain ZIP, seven Git bundles, metadata ZIP, and `SHA256SUMS.txt`

- [ ] Export repository settings, issues, pulls, releases, branches, and tags to per-repository JSON.
- [ ] Create the plain ZIP using original repository names and one `--all` Git bundle per mirror.
- [ ] Verify ZIP integrity, run `git bundle verify` for every bundle, and generate checksums.
- [ ] Upload all assets to the backup release.
- [ ] In a fresh temporary directory, download all release assets, verify checksums, inspect the ZIP, and clone each bundle.
- [ ] Record the verification results in the release notes.

### Task 7: Delete only verified source repositories

**Files:**
- Modify: GitHub organization repository state only

**Interfaces:**
- Consumes: successful Task 5 deployment and Task 6 independent backup verification
- Produces: one consolidated Usman repository with the seven old repositories removed

- [ ] Query and save the pre-deletion organization repository list.
- [ ] Re-check that the deletion set exactly matches the seven source names and excludes all four protected repositories.
- [ ] Delete the seven source repositories.
- [ ] Query the organization again and assert `ilma-portal-designs` plus all four protected repositories exist and all seven source repositories do not.
- [ ] Open the Pages URL and backup release once more, then record final repository IDs and URLs in the migration report.
