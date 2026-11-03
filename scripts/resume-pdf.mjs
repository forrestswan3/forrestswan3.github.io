// Optional, manual only: prints the /resume/ page to dist/resume-web.pdf for a print preview.
// CI no longer runs this. The published /resume.pdf is the master file in public/resume.pdf,
// the same file posted on LinkedIn and Linktree. Replace that file to update the download.
// Requires the preview server (npm run preview) to be running on :4321.
import { chromium } from 'playwright';
const base = process.env.BASE_URL || 'http://localhost:4321';
const browser = await chromium.launch();
const page = await browser.newPage();
await page.emulateMedia({ media: 'print', colorScheme: 'light' });
await page.goto(`${base}/resume/`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: 'dist/resume-web.pdf', format: 'Letter', printBackground: true, margin: { top: '0.5in', bottom: '0.5in', left: '0.55in', right: '0.55in' } });
await browser.close();
console.log('Wrote dist/resume-web.pdf');
