# Usman repository consolidation report

Completed on 2026-10-16.

## Consolidated destination

- Repository: [mantiq-pk/ilma-portal-designs](https://github.com/mantiq-pk/ilma-portal-designs) (`1422149296`)
- Preview site: [ILMA Design Library](https://mantiq-pk.github.io/ilma-portal-designs/)
- Backup release: [Pre-consolidation backup — 2026-10-16](https://github.com/mantiq-pk/ilma-portal-designs/releases/tag/pre-consolidation-backup-2026-10-16)

The root now has three clear working areas: `All Files` for nontechnical daily use, `Old Dumb` for untouched copies of all seven old repositories, and `Dev` for automation. `All Files` is flat within seven plainly named subfolders and removes duplicate copies and empty placeholder files from the daily view. Its generated catalog exposes 38 live HTML prototypes, 39 Word documents, and one source screenshot.

`Old Dumb` contains all 99 original files byte-for-byte. The backup release remains the authoritative full-history recovery copy. GitHub Actions validates the backup shape, tests the catalog, and deploys the Pages site.

## Deleted source repositories

Each repository was attributed to Usman from its first commit author, `mianusmanghani053-del`. All seven returned HTTP 404 after deletion.

| Repository | Original GitHub ID | Preserved HEAD |
| --- | ---: | --- |
| `ILMA-Artifacts-Super-Admin-and-Admin` | `1415746852` | `60873afee43c872c98b400acce117d4c35faf042` |
| `Al-Mantiq-Control-Center-Admin-Portal-` | `1415759624` | `a53079a2fa910dab5f5adeec8e5eca697e6657be` |
| `Main-Modules-of-ILMA-Users-Navigation` | `1415929013` | `1bced7b42cb9b64d55b5b90a7699bc809ede04d8` |
| `ILMA-Artifacts-Finance-Manager` | `1421691458` | `4f9b4b300cffda71a11ddca5fdb9daa716593826` |
| `ILMA-Teacher-Portal` | `1421695928` | `09ed8b04af194a8b8d3991744fa639e853ac996d` |
| `ILMA-Parent-Portal` | `1421698362` | `b1f52536eeefcda560c88e1a026a2d4c042e42fe` |
| `ILMA-Student-Portal` | `1421700554` | `5b106eb21bf0bbbedcc8807c460ba8da4547299e` |

## Protected repositories verified unchanged

| Repository | GitHub ID |
| --- | ---: |
| `ilma-school-management-system` | `1391258335` |
| `ilama-mantaq-backend` | `1393485462` |
| `past-papers` | `1392820084` |
| `mantiq-website` | `1391207666` |

The organization contained exactly these four protected repositories plus `ilma-portal-designs` after deletion.

## Backup verification

The release contains ten assets:

- a plain ZIP of all seven default-branch working trees under their original repository names;
- seven full-history Git bundles;
- a ZIP of repository settings, issues, pull requests, releases, branches, and tags as JSON; and
- `SHA256SUMS.txt`.

All release assets were downloaded into a fresh directory and passed SHA-256 verification. Both ZIPs passed integrity checks. Every bundle cloned successfully, restored HEADs and commit counts matched the source repositories, every default-branch working tree matched the plain ZIP byte-for-byte, and all metadata files parsed as valid JSON.

## Final verification

- GitHub Pages returned HTTP 200.
- The backup release remained accessible with all ten assets.
- All seven deleted repository API URLs returned HTTP 404.
- The consolidated repository and all four protected repositories remained accessible.
