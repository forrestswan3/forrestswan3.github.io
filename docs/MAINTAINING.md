# Maintaining the site

Most content comes from JSON files in `src/data/`; longer page copy (home, About, Services intro) lives in `src/pages/*.astro`. Pushes to `main` rebuild and redeploy the site in about 3 minutes; the Actions tab shows progress and any failed check.

## Project status and case studies come from the tracker

`src/data/portfolio.json` is **generated**. Do not edit it by hand. Project status, dates, highlights and the
status-driven numbers on the home and About pages all come from the private `forrestswan3/portfolio-tracker`
repo (`projects.yaml` → `scripts/build_portfolio.py`). Its `HOW-TO-UPDATE.md` has the three-step routine.
The one exception: non-agency entries that the tracker does not know (for example the SystemSerenity business
projects) are kept as they are in the file, so they can still be edited here.

Status values (set in the tracker): `Maintained` (in production, still being improved — shown with a live dot),
`Shipped` (delivered and stable), `In Progress` / `Blocked` (not yet live, hollow dot). `Idea`, `Scoped` and
`Retired` projects are never published. Cards are grouped by `category` on the Work page.

## Common updates

**New job title, bullet or skill:** edit `src/data/profile.json`. The About page, the HTML resume, the PDF resume, the vCard and the search-engine data all update from this file.

**New or updated project:** edit `projects.yaml` in the tracker repo and run its generators (see above).
- Optional screenshot: add `public/previews/<name>.webp` (960×600) and set `"preview": "docs/preview.png"` and `"preview_img": "<name>"` on the project in the tracker.

**Prices or service details:** edit `src/data/services.json`.

**Colors or fonts:** edit the tokens at the top of `src/styles/global.css`. If you change a color, re-check its contrast (see `docs/DESIGN-EVIDENCE.md`); the accessibility check in CI will also flag failures.

## If a check fails

- **Accessibility (axe):** the log names the page, theme and rule. The usual cause is color contrast after a token change.
- **Lighthouse:** usually a large new image. Convert it to WebP at 960 px wide or smaller.
- **Links (lychee):** a URL in one of the JSON files is wrong or the target page moved.
- **Sensitive-data scan:** a private IP, SID or a term from the `PII_PATTERNS` secret reached the built site. Fix the source in the tracker, regenerate, push again.

## Rules

- No employer or carrier logos, and no client data.
- Staff names in any project copy must be fictional (see the sanitization notes in each repo).
- Commits use the GitHub noreply email.
