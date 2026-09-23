# Maintaining the site

Most content comes from three JSON files in `src/data/`; longer page copy (home, About, Services intro) lives in `src/pages/*.astro`. Edit a file on GitHub (pencil icon), commit to `main`, and the site rebuilds and redeploys in about 3 minutes. The Actions tab shows progress and any failed check.

## Common updates

**New job title, bullet or skill:** edit `src/data/profile.json`. The About page, the HTML resume, the PDF resume, the vCard and the search-engine data all update from this file.

**New or updated project:** edit `src/data/portfolio.json`.
- Copy an existing project block and change `name` (the repo name), `title`, `status` (`Shipped`, `In production` or `In progress`), `shipped` (YYYY-MM-DD), `tagline`, `topics`, `repo` and `detail`.
- A project appears only when `"visibility": "public"`.
- Optional screenshot: add `public/previews/<name>.webp` (960×600) and set `"preview": "docs/preview.png"`.

**Prices or service details:** edit `src/data/services.json`.

**Colors or fonts:** edit the tokens at the top of `src/styles/global.css`. If you change a color, re-check its contrast (see `docs/DESIGN-EVIDENCE.md`); the accessibility check in CI will also flag failures.

## If a check fails

- **Accessibility (axe):** the log names the page, theme and rule. The usual cause is color contrast after a token change.
- **Lighthouse:** usually a large new image. Convert it to WebP at 960 px wide or smaller.
- **Links (lychee):** a URL in one of the JSON files is wrong or the target page moved.

## Rules

- No employer or carrier logos, and no client data.
- Staff names in any project copy must be fictional (see the sanitization notes in each repo).
- Commits use the GitHub noreply email.
