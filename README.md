# SystemSerenity: forrestswan3.github.io

Personal brand site for **Forrest Swan III**, published at **https://forrestswan3.github.io/**.

*Operational clarity at scale.*

Built with [Astro](https://astro.build) as static HTML with near-zero JavaScript, and deployed to GitHub Pages by GitHub Actions on every push to `main`.

## What's here

| Path | Purpose |
|---|---|
| `src/data/profile.json` | Resume, contact and brand content: the single source for the About, Resume and Contact pages, the resume PDF, the vCard and the structured data |
| `src/data/portfolio.json` | Every project (status, dates, stack, problem/solution/highlights). Drives the Work pages and home-page stats |
| `src/data/services.json` | SystemSerenity service offers and prices |
| `src/pages/` | Pages, plus build-time endpoints: `sitemap.xml`, `robots.txt`, `forrest-swan.vcf`, `qr.svg` |
| `src/styles/global.css` | Design tokens (light and dark) and all styles |
| `scripts/resume-pdf.mjs` | Prints `/resume/` to `resume.pdf` during CI, so the PDF can't drift from the HTML |
| `scripts/a11y.mjs` | axe-core WCAG 2.2 AA checks on every page, in light and dark mode |
| `scripts/make-mark.py` | Regenerates the SS monogram SVGs |
| `docs/DESIGN-EVIDENCE.md` | Research behind the design decisions, plus the contrast table |
| `docs/MAINTAINING.md` | How to update content in under 5 minutes |

## Quality gates (CI)

Every push runs the build, then:

1. Generates `resume.pdf` from the HTML resume
2. axe accessibility checks (fails on any serious or critical issue)
3. Lighthouse on key pages (fails below 95 in Performance, Accessibility, Best Practices or SEO)
4. Link check with lychee (fails on broken links)
5. Secret scan with gitleaks (separate workflow)

Only `main` deploys.

## Local development

```bash
npm install
npm run dev        # http://localhost:4321
npm run build && npm run preview
```

© Forrest Swan III. Published for portfolio review; see `LICENSE`.
