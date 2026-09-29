#!/usr/bin/env node
// Audit situs otomatis (Playwright): overflow, heading, alt, gambar, ukuran font, kontras, target sentuh, error JS.
//   npm run build && npm run audit:site
// Hasil: reports/site-audit.md. Exit code 1 bila ada pelanggaran (bukan sekadar peringatan).
import { mkdirSync, writeFileSync } from 'node:fs';
import { chromium } from 'playwright-core';
import { BASE, PAGES, ensureServer, findChrome } from './lib/browser.mjs';

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900, opts: {} },
  { name: 'laptop', width: 1024, height: 768, opts: {} },
  { name: 'tablet', width: 820, height: 1180, opts: { isMobile: true, hasTouch: true } },
  { name: 'mobile', width: 390, height: 844, opts: { isMobile: true, hasTouch: true } },
  { name: 'small', width: 320, height: 640, opts: { isMobile: true, hasTouch: true } },
];
const MIN_FONT = 12;        // px — lantai ukuran teks
const MIN_TOUCH = 24;       // px — WCAG 2.2 AA (2.5.8) target minimum; tautan inline dalam paragraf dikecualikan
const pages = process.env.AUDIT_PAGES ? process.env.AUDIT_PAGES.split(',') : PAGES;

// Dijalankan di dalam halaman
function inPage({ minFont, minTouch, touch }) {
  const parse = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const a = m[1].split(',').map(parseFloat); return { rgb: a.slice(0, 3), a: a.length > 3 ? a[3] : 1 }; };
  const lum = (c) => { const [r, g, b] = c.map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const bgOf = (el) => {
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e); const c = parse(cs.backgroundColor);
      if (c && c.a > 0.6) return { rgb: c.rgb };
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !cs.backgroundImage.includes('url')) {
        const g = cs.backgroundImage.match(/rgba?\([^)]+\)|#[0-9a-f]{6}/gi); const q = g && parse(g[Math.floor(g.length / 2)]); if (q) return { rgb: q.rgb };
      }
      if ([...e.children].some((ch) => ch.matches?.('.depth-photo,.prayer-photo,.page-hero-photo'))) return { photo: true };
    }
    return { rgb: [6, 31, 35] };
  };
  const small = [], contrast = [], seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement; if (seen.has(el)) continue; seen.add(el);
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (el.closest('[hidden],.sr-only,script,style,noscript,#loader,.loader,dialog:not([open])')) continue;
    const size = parseFloat(cs.fontSize); const cls = (el.tagName.toLowerCase() + '.' + String(el.className).split(' ')[0]).slice(0, 40);
    if (size < minFont) small.push({ cls, size, t: n.textContent.trim().slice(0, 30) });
    const col = parse(cs.color), bg = bgOf(el);
    if (col && bg.rgb) {
      const large = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700); const need = large ? 3 : 4.5; const rr = ratio(col.rgb, bg.rgb);
      if (rr < need) contrast.push({ cls, t: n.textContent.trim().slice(0, 30), ratio: +rr.toFixed(2), need });
    }
  }
  const imgs = [...document.images].filter((i) => i.getBoundingClientRect().width > 0 && i.currentSrc && !i.closest('dialog:not([open])') && !i.classList.contains('page-hero-photo'));
  const broken = imgs.filter((i) => i.complete && i.naturalWidth === 0 && !i.classList.contains('img-failed')).map((i) => i.currentSrc.split('/').pop());
  const noAlt = [...document.images].filter((i) => i.getAttribute('alt') === null).length;
  const crops = imgs.map((i) => { const r = i.getBoundingClientRect(); const fit = getComputedStyle(i).objectFit; if (fit !== 'cover' || !i.naturalWidth) return null; const sc = Math.max(r.width / i.naturalWidth, r.height / i.naturalHeight); const lost = 1 - (r.width / (i.naturalWidth * sc)) * (r.height / (i.naturalHeight * sc)); return { src: i.currentSrc.split('/').pop().slice(0, 30), lost: Math.round(lost * 100), dpr: +(i.naturalWidth / r.width).toFixed(2) }; }).filter(Boolean);
  const targets = touch ? [...document.querySelectorAll('a,button')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (r.width < minTouch || r.height < minTouch) && e.offsetParent !== null && !e.classList.contains('sr-only') && !(e.closest('p') && getComputedStyle(e).display === 'inline'); }).map((e) => `${e.tagName.toLowerCase()}.${String(e.className).split(' ')[0]} ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`) : [];
  return { over: document.documentElement.scrollWidth - innerWidth, h1: document.querySelectorAll('h1').length, noAlt, broken, small, contrast, crops, targets };
}

const browser = await chromium.launch({ executablePath: findChrome(), args: ['--no-sandbox'] });
const stop = await ensureServer();
const violations = [], warnings = [];
const summary = [];

for (const vp of VIEWPORTS) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, ...vp.opts });
  // lewati intro & matikan animasi pin supaya semua konten terlihat & terukur
  await ctx.addInitScript(() => { try { sessionStorage.setItem('mec-intro', '1'); localStorage.setItem('mec-calm', '1'); } catch {} });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('response', (r) => { if (r.status() >= 400 && !r.url().includes('/pagefind/') && !r.url().endsWith('/nonexistent/')) errors.push(`HTTP ${r.status()} ${r.url().replace(BASE, '')}`); });
  let n = 0;
  for (const path of pages) {
    errors.length = 0;
    await page.goto(BASE + path, { waitUntil: 'networkidle' });
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < h; y += 700) { await page.evaluate((v) => scrollTo({ top: v, behavior: 'instant' }), y); await page.waitForTimeout(60); }
    await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(250);
    const d = await page.evaluate(inPage, { minFont: MIN_FONT, minTouch: MIN_TOUCH, touch: !!vp.opts.hasTouch });
    const where = `${vp.name} ${path}`;
    if (d.over > 1) violations.push(`${where}: scroll horizontal ${d.over}px`);
    if (d.h1 !== 1) violations.push(`${where}: jumlah <h1> = ${d.h1}`);
    if (d.noAlt) violations.push(`${where}: ${d.noAlt} gambar tanpa alt`);
    if (d.broken.length) violations.push(`${where}: gambar rusak ${d.broken.join(', ')}`);
    if (d.small.length && (vp.name === 'desktop' || vp.name === 'mobile')) violations.push(`${where}: ${d.small.length} teks < ${MIN_FONT}px (mis. ${d.small.slice(0, 2).map((s) => `${s.cls} ${s.size}px "${s.t}"`).join('; ')})`);
    if (d.contrast.length && vp.name === 'desktop') violations.push(`${where}: ${d.contrast.length} pasangan warna gagal kontras (mis. ${d.contrast.slice(0, 2).map((c) => `${c.cls} ${c.ratio}<${c.need}`).join('; ')})`);
    if (d.targets.length && vp.name === 'mobile') violations.push(`${where}: target sentuh kecil ${[...new Set(d.targets)].slice(0, 3).join(', ')}`);
    if (errors.length) violations.push(`${where}: error ${errors.slice(0, 2).join(' | ')}`);
    if (vp.name === 'desktop') for (const c of d.crops.filter((c) => c.lost > 40)) warnings.push(`${path}: ${c.src} terpotong ${c.lost}%`);
    if (vp.name === 'desktop') for (const c of d.crops.filter((c) => c.dpr < 1)) warnings.push(`${path}: ${c.src} di-upscale (${c.dpr}× piksel per CSS px)`);
    n++;
  }
  summary.push(`${vp.name} (${vp.width}×${vp.height}): ${n} halaman`);
  await ctx.close();
}
await browser.close(); stop();

mkdirSync('reports', { recursive: true });
const uniq = (a) => [...new Set(a)];
const md = ['# Hasil audit situs', '', `Dijalankan: ${new Date().toISOString().slice(0, 10)} · ${summary.join(' · ')}`, '',
  `Pemeriksaan: overflow horizontal, satu <h1>, alt gambar, gambar rusak, teks < ${MIN_FONT}px, kontras WCAG AA (latar polos), target sentuh < ${MIN_TOUCH}px (WCAG 2.2) di HP, error JS/HTTP.`, '',
  `## Pelanggaran (${violations.length})`, ...(violations.length ? violations.map((v) => `- ${v}`) : ['Tidak ada.']), '',
  `## Peringatan (${uniq(warnings).length})`, ...(uniq(warnings).length ? uniq(warnings).map((w) => `- ${w}`) : ['Tidak ada.']), ''];
writeFileSync('reports/site-audit.md', md.join('\n'));
console.log(md.join('\n'));
process.exit(violations.length ? 1 : 0);
