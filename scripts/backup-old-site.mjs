// Cadangkan situs lama (Hostinger Website Builder) sebelum layanan dimatikan.
// Usage: node scripts/backup-old-site.mjs [https://malangeducationcenter.com] [folder-keluaran]
// Menyimpan: HTML tiap halaman (dari sitemap), teks polos tiap halaman, dan semua gambar/berkas asli di assets.zyrosite.com.
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';

const BASE = (process.argv[2] ?? 'https://malangeducationcenter.com').replace(/\/$/, '');
const OUT = process.argv[3] ?? 'backup/hostinger-site';
mkdirSync(join(OUT, 'pages'), { recursive: true });
mkdirSync(join(OUT, 'files'), { recursive: true });

const get = async (u) => { const r = await fetch(u, { headers: { 'user-agent': 'Mozilla/5.0 backup' } }); if (!r.ok) throw new Error(`${u} -> ${r.status}`); return r; };
const decode = (s) => s.replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/\\u002F/g, '/');

const sitemap = await (await get(`${BASE}/sitemap.xml`)).text();
writeFileSync(join(OUT, 'sitemap.xml'), sitemap);
const urls = [...new Set([BASE + '/', ...[...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1])])];
const fileUrls = new Set();
const report = [];

for (const u of urls) {
  try {
    const html = await (await get(u)).text();
    const slug = new URL(u).pathname.replace(/^\/|\/$/g, '') || 'index';
    writeFileSync(join(OUT, 'pages', `${slug}.html`), html);
    const text = decode(html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, '\n')).replace(/\n\s*\n+/g, '\n').trim();
    writeFileSync(join(OUT, 'pages', `${slug}.txt`), text);
    for (const m of decode(html).matchAll(/https:\/\/(?:assets|cdn)\.zyrosite\.com\/[^\s"'\\)<>]+/g)) {
      // buang segmen resize cdn-cgi/image/<opsi>/ agar mendapat berkas asli
      const orig = m[0].replace(/\/cdn-cgi\/image\/[^/]+\//, '/');
      if (/\.(jpe?g|png|webp|gif|svg|pdf|mp4|ico|txt)$/i.test(orig)) fileUrls.add(orig);
    }
    report.push(`ok   ${u}`);
  } catch (e) { report.push(`GAGAL ${u} ${e.message}`); }
}

let saved = 0;
for (const f of fileUrls) {
  const name = f.split('/zyrosite.com/')[1]?.replace(/[^\w.-]+/g, '_') ?? basename(f);
  const p = join(OUT, 'files', name);
  if (existsSync(p)) continue;
  try { const r = await get(f); writeFileSync(p, Buffer.from(await r.arrayBuffer())); saved++; report.push(`file ${f}`); }
  catch (e) { report.push(`GAGAL ${f} ${e.message}`); }
}
writeFileSync(join(OUT, 'LAPORAN.txt'), report.join('\n') + '\n');
console.log(`Halaman: ${urls.length} · berkas unik: ${fileUrls.size} · tersimpan baru: ${saved}\nLihat ${OUT}/LAPORAN.txt (baris GAGAL = unduh manual)`);
