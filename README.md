# Portfolio

Source of truth for Forrest Swan III's project portfolio.

- `portfolio.json` — every project: title, status, dates, tags, repo URL, visibility.
- `scripts/build.py` — renders `site/index.html` (GitHub Pages) and `PROFILE_README.md` (copy into the `forrestswan3/forrestswan3` profile repo).
- `.github/workflows/pages.yml` — rebuilds and deploys the site on every push to `main`.
- `.github/workflows/secret-scan.yml` — gitleaks on every push.
- `docs/ADD-A-PROJECT.md` — checklist for adding the next project.
- `docs/COMMIT-GUIDE.md` — commit message convention.

A project only gets a public link once its `visibility` is set to `public` in `portfolio.json`.
