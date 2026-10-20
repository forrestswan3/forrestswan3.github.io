import posts from '../data/posts.json';
import profile from '../data/profile.json';
const SITE = 'https://forrestswan3.github.io';
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export function GET() {
  const items = [...posts.posts].sort((a, b) => b.date.localeCompare(a.date));
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>${esc(profile.brand.name)} · Writing by ${esc(profile.name)}</title>
  <link>${SITE}/writing/</link>
  <atom:link href="${SITE}/rss.xml" rel="self" type="application/rss+xml" />
  <description>Technical write-ups from building and running agency systems: root cause analyses, Windows and networking gotchas, least-privilege rollouts.</description>
  <language>en-us</language>
  <lastBuildDate>${new Date(items[0].date + 'T12:00:00Z').toUTCString()}</lastBuildDate>
${items.map((p) => `  <item>
    <title>${esc(p.title)}</title>
    <link>${SITE}/writing/${p.slug}/</link>
    <guid isPermaLink="true">${SITE}/writing/${p.slug}/</guid>
    <pubDate>${new Date(p.date + 'T12:00:00Z').toUTCString()}</pubDate>
    <description>${esc(p.summary)}</description>${p.tags.map((t) => `\n    <category>${esc(t)}</category>`).join('')}
  </item>`).join('\n')}
</channel>
</rss>
`;
  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
