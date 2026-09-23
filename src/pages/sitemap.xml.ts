import portfolio from '../data/portfolio.json';
const SITE = 'https://forrestswan3.github.io';
export function GET() {
  const paths = ['/', '/about/', '/work/', '/services/', '/resume/', '/links/', '/contact/',
    ...portfolio.projects.filter((p) => p.visibility === 'public').map((p) => `/work/${p.name}/`)];
  const today = new Date().toISOString().slice(0, 10);
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths.map((p) => `  <url><loc>${SITE}${p}</loc><lastmod>${today}</lastmod></url>`).join('\n')}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
