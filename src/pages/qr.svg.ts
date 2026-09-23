import QRCode from 'qrcode';
// QR code for the site root, generated at build time (no runtime JS).
export async function GET() {
  const svg = await QRCode.toString('https://forrestswan3.github.io/', {
    type: 'svg', errorCorrectionLevel: 'M', margin: 1, color: { dark: '#0B1F33', light: '#FFFFFF' },
  });
  return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml' } });
}
