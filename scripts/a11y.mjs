// Runs axe-core (WCAG 2.0/2.1/2.2 A + AA) on every page in light and dark mode.
// Fails the build on any serious or critical violation. Requires the preview server on :4321.
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync } from 'node:fs';
const base = process.env.BASE_URL || 'http://localhost:4321';
const sitemap = readFileSync('dist/sitemap.xml', 'utf8');
const paths = [...sitemap.matchAll(/<loc>https:\/\/forrestswan3\.github\.io([^<]*)<\/loc>/g)].map((m) => m[1]);
paths.push('/404.html');
const browser = await chromium.launch();
let failures = 0;
for (const scheme of ['light', 'dark']) {
  const ctx = await browser.newContext({ colorScheme: scheme });
  const page = await ctx.newPage();
  for (const p of paths) {
    await page.goto(base + p, { waitUntil: 'networkidle' });
    const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
    const bad = r.violations.filter((v) => ['serious', 'critical'].includes(v.impact || ''));
    const minor = r.violations.length - bad.length;
    console.log(`${bad.length ? 'FAIL' : 'ok  '} [${scheme}] ${p}${minor ? ` (${minor} minor)` : ''}`);
    for (const v of r.violations) console.log(`      ${v.impact}: ${v.id}: ${v.help} (${v.nodes.length} node(s))`);
    failures += bad.length;
  }
  await ctx.close();
}
await browser.close();
if (failures) { console.error(`${failures} serious/critical accessibility violation(s)`); process.exit(1); }
console.log('Accessibility: no serious or critical violations');
