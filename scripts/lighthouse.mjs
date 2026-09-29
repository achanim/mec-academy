#!/usr/bin/env node
// Jalankan Lighthouse (mobile + desktop) ke halaman-halaman utama dan cek ambang batas.
//   npm run build && npm run audit:lh            # semua halaman
//   AUDIT_PAGES=/,/faq/ npm run audit:lh         # halaman tertentu
// Hasil: reports/lighthouse-summary.md (+ JSON mentah di reports/lighthouse/, tidak di-commit)
import { mkdirSync, writeFileSync } from 'node:fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';
import { BASE, PAGES, ensureServer, findChrome } from './lib/browser.mjs';

// Ambang batas: turun di bawah ini => exit code 1 (dipakai CI)
const BUDGET = {
  mobile: { performance: 90, accessibility: 95, 'best-practices': 95, seo: 95, lcp: 2500, cls: 0.1, tbt: 200 },
  desktop: { performance: 95, accessibility: 95, 'best-practices': 95, seo: 95, lcp: 2000, cls: 0.1, tbt: 200 },
};
const pages = (process.env.AUDIT_PAGES ? process.env.AUDIT_PAGES.split(',') : PAGES);
mkdirSync('reports/lighthouse', { recursive: true });
process.env.CHROME_PATH = findChrome();
const stop = await ensureServer();
const rows = [], fails = [];

for (const preset of ['mobile', 'desktop']) {
  for (const path of pages) {
    const chrome = await launch({ chromePath: process.env.CHROME_PATH, chromeFlags: ['--headless=new', '--no-sandbox'] });
    try {
      const flags = { port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'] };
      const config = preset === 'desktop' ? (await import('lighthouse/core/config/desktop-config.js')).default : undefined;
      const { lhr } = await lighthouse(BASE + path, flags, config);
      const sc = (k) => Math.round((lhr.categories[k]?.score ?? 0) * 100);
      const m = { performance: sc('performance'), accessibility: sc('accessibility'), 'best-practices': sc('best-practices'), seo: sc('seo'),
        lcp: Math.round(lhr.audits['largest-contentful-paint'].numericValue), cls: +lhr.audits['cumulative-layout-shift'].numericValue.toFixed(3), tbt: Math.round(lhr.audits['total-blocking-time'].numericValue) };
      const b = BUDGET[preset];
      const bad = [];
      for (const k of ['performance', 'accessibility', 'best-practices', 'seo']) if (m[k] < b[k]) bad.push(`${k} ${m[k]}<${b[k]}`);
      if (m.lcp > b.lcp) bad.push(`LCP ${m.lcp}>${b.lcp}`);
      if (m.cls > b.cls) bad.push(`CLS ${m.cls}>${b.cls}`);
      if (m.tbt > b.tbt) bad.push(`TBT ${m.tbt}>${b.tbt}`);
      rows.push({ preset, path, ...m, bad });
      if (bad.length) fails.push(`${preset} ${path}: ${bad.join(', ')}`);
      writeFileSync(`reports/lighthouse/${preset}${path.replace(/\W+/g, '_')}.json`, JSON.stringify(lhr));
      console.log(`${bad.length ? '✗' : '✓'} ${preset.padEnd(7)} ${path.padEnd(58)} perf ${m.performance} a11y ${m.accessibility} bp ${m['best-practices']} seo ${m.seo} | LCP ${m.lcp}ms CLS ${m.cls} TBT ${m.tbt}ms`);
    } finally { await chrome.kill(); }
  }
}
stop();

const md = ['# Ringkasan Lighthouse', '', `Dijalankan: ${new Date().toISOString().slice(0, 10)} · build produksi lokal · Lighthouse ${(await import('lighthouse/package.json', { with: { type: 'json' } })).default.version}`,
  '', 'Catatan: Lighthouse melewati layar intro (user-agent headless dianggap crawler). Angka lab (throttling simulasi), bukan data pengguna nyata.', '',
  '| Perangkat | Halaman | Perf | A11y | BP | SEO | LCP (ms) | CLS | TBT (ms) | Status |', '|---|---|---|---|---|---|---|---|---|---|',
  ...rows.map((r) => `| ${r.preset} | \`${r.path}\` | ${r.performance} | ${r.accessibility} | ${r['best-practices']} | ${r.seo} | ${r.lcp} | ${r.cls} | ${r.tbt} | ${r.bad.length ? '✗ ' + r.bad.join('; ') : '✓'} |`),
  '', `Ambang: mobile perf ≥ ${BUDGET.mobile.performance}, desktop perf ≥ ${BUDGET.desktop.performance}; a11y/BP/SEO ≥ 95; LCP ≤ ${BUDGET.mobile.lcp}/${BUDGET.desktop.lcp} ms; CLS ≤ ${BUDGET.mobile.cls}; TBT ≤ ${BUDGET.mobile.tbt} ms.`];
writeFileSync('reports/lighthouse-summary.md', md.join('\n') + '\n');
console.log(fails.length ? `\n${fails.length} halaman melewati ambang:\n- ${fails.join('\n- ')}` : '\nSemua halaman memenuhi ambang batas.');
process.exit(fails.length ? 1 : 0);
