export function GET() {
  return new Response('User-agent: *\nAllow: /\n\nSitemap: https://forrestswan3.github.io/sitemap.xml\n', { headers: { 'Content-Type': 'text/plain' } });
}
