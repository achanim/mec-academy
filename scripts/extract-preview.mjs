// Ekstrak gambar, font, dan konten dari MEC_UI_Preview.html.
// Usage: node scripts/extract-preview.mjs <path-to-preview.html>
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import sharp from 'sharp';

const src = process.argv[2] ?? 'MEC_UI_Preview.html';
const html = readFileSync(src, 'utf8');
const out = (p) => join(new URL('..', import.meta.url).pathname, p);
mkdirSync(out('src/assets/images'), { recursive: true });
mkdirSync(out('src/assets/fonts'), { recursive: true });
mkdirSync(out('src/data'), { recursive: true });

// ---- fonts ----
const fontRe = /@font-face\{font-family:'(MEC\w+)';src:url\('data:([^;]+);base64,([A-Za-z0-9+/=]+)'\)/g;
const extMap = { 'font/woff2': 'woff2', 'font/woff': 'woff', 'font/ttf': 'ttf', 'font/otf': 'otf', 'application/font-woff2': 'woff2', 'application/font-woff': 'woff', 'application/x-font-ttf': 'ttf', 'application/octet-stream': 'bin' };
for (const [, name, mime, b64] of html.matchAll(fontRe)) {
  const buf = Buffer.from(b64, 'base64');
  const magic = buf.subarray(0, 4).toString('latin1');
  const ext = magic === 'wOF2' ? 'woff2' : magic === 'wOFF' ? 'woff' : magic === 'OTTO' ? 'otf' : extMap[mime] ?? 'ttf';
  writeFileSync(out(`src/assets/fonts/${name}.${ext}`), buf);
  console.log('font', name, ext, buf.length);
}

// ---- images ----
const imgBlock = html.match(/const mecImages=\{(.*?)\};/s)[1];
const imgRe = /"([a-z0-9-]+)":"data:image\/(\w+);base64,([A-Za-z0-9+/=]+)"/g;
let total = 0;
for (const [, name, type, b64] of imgBlock.matchAll(imgRe)) {
  const buf = Buffer.from(b64, 'base64');
  if (name === 'logo' || type === 'png') {
    // logo & potret instruktur (png): simpan lossless-ish sebagai webp
    const o = await sharp(buf).webp({ quality: 88, alphaQuality: 95 }).toBuffer();
    writeFileSync(out(`src/assets/images/${name}.webp`), o);
    total += o.length;
  } else {
    // sumber jpeg: simpan master jpg (Astro akan membuat AVIF/WebP responsif saat build)
    const o = await sharp(buf).resize({ width: 2400, withoutEnlargement: true }).jpeg({ quality: 82, mozjpeg: true }).toBuffer();
    writeFileSync(out(`src/assets/images/${name}.jpg`), o);
    total += o.length;
  }
}
console.log('images total KB', Math.round(total / 1024));

// ---- content ----
const grab = (name) => {
  const m = html.match(new RegExp(`const ${name}=(\\[|\\{)`));
  const start = m.index + m[0].length - 1;
  const open = html[start], close = open === '{' ? '}' : ']';
  let depth = 0, inStr = false, esc = false;
  for (let i = start; i < html.length; i++) {
    const c = html[i];
    if (inStr) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') inStr = false; continue; }
    if (c === '"') inStr = true;
    else if (c === open) depth++;
    else if (c === close && --depth === 0) return JSON.parse(html.slice(start, i + 1));
  }
};
for (const [v, file] of [['mecContent', 'content'], ['mecGallery', 'gallery'], ['mecResearch', 'research']]) {
  writeFileSync(out(`src/data/${file}.json`), JSON.stringify(grab(v), null, 2) + '\n');
  console.log('data', file);
}
