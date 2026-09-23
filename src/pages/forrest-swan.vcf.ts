import profile from '../data/profile.json';
// vCard 3.0 (widest phone/Outlook support). Lines must end in CRLF.
export function GET() {
  const lines = [
    'BEGIN:VCARD', 'VERSION:3.0',
    'N:Swan III;Forrest;;;', `FN:${profile.name}`,
    `TITLE:${profile.title}`, `ORG:${profile.employer}`,
    `EMAIL;TYPE=INTERNET,PREF:${profile.email}`,
    `TEL;TYPE=CELL:${profile.phone}`,
    'ADR;TYPE=WORK:;;;Melbourne;FL;;USA',
    `URL:${profile.site}/`,
    `X-SOCIALPROFILE;TYPE=linkedin:${profile.social.linkedin}`,
    `NOTE:${profile.brand.name} · ${profile.brand.tagline}`,
    'END:VCARD', '',
  ];
  return new Response(lines.join('\r\n'), { headers: { 'Content-Type': 'text/vcard; charset=utf-8' } });
}
