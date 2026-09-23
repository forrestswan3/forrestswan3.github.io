// Prints /resume/ to dist/resume.pdf so the PDF is always generated from the same data as the HTML resume.
// Requires the preview server (npm run preview) to be running on :4321.
import { chromium } from 'playwright';
const base = process.env.BASE_URL || 'http://localhost:4321';
const browser = await chromium.launch();
const page = await browser.newPage();
await page.emulateMedia({ media: 'print', colorScheme: 'light' });
await page.goto(`${base}/resume/`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: 'dist/resume.pdf', format: 'Letter', printBackground: true, margin: { top: '0.5in', bottom: '0.5in', left: '0.55in', right: '0.55in' } });
await browser.close();
console.log('Wrote dist/resume.pdf');
