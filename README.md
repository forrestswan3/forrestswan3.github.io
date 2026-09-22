# Portfolio

Source of truth for Forrest Swan III's project portfolio, published at **https://forrestswan3.github.io/**.

- `portfolio.json`: every project (title, status, dates, tags, repo URL, visibility, plus `detail`, `page`, `demo` and `preview` for project pages).
- `scripts/build.py`: renders
  - `site/index.html`: the landing page (deployed by GitHub Actions)
  - `pages/<repo>/index.html`: a project page. Copy it to the root of that repo; GitHub Pages serves it at `https://forrestswan3.github.io/<repo>/`
  - `PROFILE_README.md`: copy into the `forrestswan3/forrestswan3` profile repo as `README.md`
- `assets/previews/<repo>.png`: 1440×900 demo screenshots, used on the landing page. Copy the same image to `docs/preview.png` in that repo.
- `.github/workflows/pages.yml`: rebuilds and deploys the site on every push to `main`.
- `.github/workflows/secret-scan.yml`: runs gitleaks on every push.
- `docs/ADD-A-PROJECT.md`: checklist for adding the next project.
- `docs/COMMIT-GUIDE.md`: commit message convention.

A project only gets a public link once its `visibility` is set to `public` in `portfolio.json`.
