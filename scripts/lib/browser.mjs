// Util bersama untuk skrip audit: cari Chrome, jalankan/hentikan server preview.
import { existsSync, readdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { join } from 'node:path';

export function findChrome() {
  const env = process.env.CHROME_PATH;
  if (env && existsSync(env)) return env;
  const roots = [process.env.PLAYWRIGHT_BROWSERS_PATH, '/opt/pw-browsers', join(process.env.HOME ?? '', '.cache/ms-playwright')].filter(Boolean);
  for (const r of roots) {
    if (!existsSync(r)) continue;
    for (const d of readdirSync(r).filter((x) => x.startsWith('chromium')).sort().reverse()) {
      for (const sub of ['chrome-linux/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium', 'chrome-win/chrome.exe']) {
        const p = join(r, d, sub);
        if (existsSync(p)) return p;
      }
    }
  }
  for (const p of ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']) if (existsSync(p)) return p;
  throw new Error('Chrome tidak ditemukan. Set CHROME_PATH ke biner Chrome/Chromium.');
}

export const BASE = process.env.AUDIT_URL ?? 'http://localhost:4399';

async function up(url) { try { return (await fetch(url)).ok; } catch { return false; } }

/** Pastikan situs (hasil `npm run build`) tersaji di BASE. Mengembalikan fungsi stop(). */
export async function ensureServer() {
  if (process.env.AUDIT_URL || (await up(BASE))) return () => {};
  const port = new URL(BASE).port || '4399';
  const child = spawn('npx', ['astro', 'preview', '--port', port], { stdio: 'ignore', detached: false });
  for (let i = 0; i < 40; i++) { if (await up(BASE)) return () => child.kill(); await new Promise((r) => setTimeout(r, 500)); }
  child.kill();
  throw new Error('Server preview tidak naik. Jalankan `npm run build` dulu.');
}

export const PAGES = [
  '/', '/program/basic-mechanic-course/', '/program/basic-mechanic-course/modul/', '/program/basic-mechanic-course/modul/basic-safety/',
  '/tahapan-seleksi/', '/fasilitas/', '/instruktur/', '/instruktur/chandra-choirulyanto/', '/industri/', '/sumber/', '/tentang/',
  '/assessment/', '/kontak/', '/faq/', '/artikel/', '/artikel/tahapan-belajar-basic-mechanic-course/',
];
