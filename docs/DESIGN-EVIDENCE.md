# Design Evidence Brief

Every design decision on this site maps to a published finding. Statistics that could not be traced to an original study or standard were left out.

| # | Finding (paraphrased) | Primary source | Design decision |
|---|---|---|---|
| 1 | People form a reliable visual-appeal judgment of a web page in about 50 ms, and it closely tracks their judgment after longer viewing. | Lindgaard, Fernandes, Dudek & Brown (2006), *Behaviour & Information Technology* 25(2), 115–126. [doi:10.1080/01449290500330448](https://www.tandfonline.com/doi/abs/10.1080/01449290500330448) | One calm hero: brand mark, a single headline (the tagline), a one-line role and three actions. Generous whitespace, one accent color, no carousel or motion. |
| 2 | On unstructured text, readers scan in an F-shape; front-loaded headings and information-carrying first words counter it. | Nielsen Norman Group, "F-Shaped Pattern of Reading on the Web" (2006, updated 2017). [nngroup.com](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) | Left-aligned text. Headings start with the key word ("Problem", "Solution", "Results"). The most important facts go in the first two lines of each section, plus a scannable proof strip. |
| 3 | In an eye-tracking study, recruiters spent an average of 7.4 seconds on the initial resume screen. The best-performing resumes used a simple layout, bold job titles, bulleted accomplishments and a clear summary at the top; multi-column layouts did worse. | Ladders, Inc., *Eye-Tracking Study* (2018). [PDF](https://www.theladders.com/static/images/basicSite/pdfs/TheLadders-EyeTracking-StudyC2.pdf) | Single-column HTML resume: bold employer and title lines, bulleted results, dates right-aligned. The resume and its PDF are one click from every page. The sample size isn't published, so this study is treated as directional. |
| 4 | Credibility rises when a site makes its information easy to verify, shows the real person behind it, highlights expertise, makes contact easy, looks professional, shows recent updates, and avoids errors. | Stanford Persuasive Technology Lab, *Stanford Web Credibility Guidelines* (Fogg, 2002). [credibility.stanford.edu](https://credibility.stanford.edu/guidelines/index.html) | Every project links to its public source. Contact is in the header, footer, a Contact page and a vCard. Every page shows an "Updated" date in the footer. Services copy stays restrained. CI link checking catches broken links. |
| 5 | "Good" Core Web Vitals are LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1, measured at the 75th percentile of page loads. | Google, web.dev "Web Vitals". [web.dev/articles/vitals](https://web.dev/articles/vitals) | Static HTML with near-zero JavaScript. Self-hosted fonts limited to the weights actually used. Images get explicit width and height (no layout shift) and lazy loading. CI fails any page that scores below 95 in Lighthouse. |
| 6 | Normal text needs at least 4.5:1 contrast (SC 1.4.3), UI components and focus indicators at least 3:1 (SC 1.4.11), and pointer targets at least 24×24 CSS px (SC 2.5.8, AA). | W3C, WCAG 2.2. [Understanding 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | The brand teal `#2C9C95` measures 3.0:1, so it's used only for decoration and UI. Text uses darker (light mode) or lighter (dark mode) shades of the same hue. Buttons and icon controls are at least 40 px. Focus rings are 3 px and visible. axe checks run in CI in both themes. |

## Contrast table (WCAG 2.2 AA)

Relative-luminance formula from WCAG 2.2. Calculated by script; the values sit next to the tokens in `src/styles/global.css`.

| Mode | Use | Foreground | Background | Ratio | Required | Result |
|---|---|---|---|---|---|---|
| Light | Body text | `#0B1F33` | `#F7F4ED` | 15.20:1 | 4.5:1 | Pass |
| Light | Secondary text | `#44546A` | `#F7F4ED` | 7.02:1 | 4.5:1 | Pass |
| Light | Links / accent text | `#1D726C` | `#F7F4ED` | 5.20:1 | 4.5:1 | Pass |
| Light | Accent text on cards | `#1D726C` | `#FFFFFF` | 5.71:1 | 4.5:1 | Pass |
| Light | Secondary text on cards | `#44546A` | `#FFFFFF` | 7.71:1 | 4.5:1 | Pass |
| Light | Button label | `#FFFFFF` | `#1D726C` | 5.71:1 | 4.5:1 | Pass |
| Light | Focus ring | `#2F5E8F` | `#F7F4ED` | 6.13:1 | 3.0:1 | Pass |
| Light | Brand teal (decorative/UI only) | `#2C9C95` | `#F7F4ED` | 3.04:1 | 3.0:1 | Pass |
| Dark | Body text | `#F7F4ED` | `#0B1F33` | 15.20:1 | 4.5:1 | Pass |
| Dark | Secondary text | `#A9B8C9` | `#0B1F33` | 8.26:1 | 4.5:1 | Pass |
| Dark | Secondary text on cards | `#A9B8C9` | `#10283F` | 7.43:1 | 4.5:1 | Pass |
| Dark | Links / accent text | `#5EC4BC` | `#0B1F33` | 8.03:1 | 4.5:1 | Pass |
| Dark | Accent text on cards | `#5EC4BC` | `#10283F` | 7.23:1 | 4.5:1 | Pass |
| Dark | Button label | `#0B1F33` | `#5EC4BC` | 8.03:1 | 4.5:1 | Pass |
| Dark | Focus ring | `#8DB4E0` | `#0B1F33` | 7.74:1 | 3.0:1 | Pass |
| Light | Accent text on alt sections | `#1D726C` | `#EFEBE1` | 4.80:1 | 4.5:1 | Pass |
| Light | Secondary text on alt sections | `#44546A` | `#EFEBE1` | 6.48:1 | 4.5:1 | Pass |
| Dark | Accent text on alt sections | `#5EC4BC` | `#16324D` | 6.32:1 | 4.5:1 | Pass |
| Dark | Secondary text on alt sections | `#A9B8C9` | `#16324D` | 6.50:1 | 4.5:1 | Pass |

## Brand system

- **Palette:** Midnight Navy `#0B1F33`, Steel Blue `#3A6EA5`, Serenity Teal `#2C9C95`, Sage `#8FB996`, Platinum Gray `#E5E7EB`, Warm Off-White `#F7F4ED`. Only shade (lightness) changes, never hue, to hit contrast targets.
- **Type:** Poppins 600/700 for display (a geometric sans that matches the wordmark), Inter Variable for body text. Both are self-hosted through Fontsource, with no runtime font CDN. Fluid type scale from `--step--1` to `--step-4` in `global.css`.
- **Mark:** the SS monogram is generated as tapered vector paths by `scripts/make-mark.py`. The navy S turns off-white in dark mode.
- **No employer or carrier logos** appear anywhere on the site. Kasey Osman Insurance and Allstate are named as employers in text only.
