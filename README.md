# MEC Academy

Situs MEC Academy (Basic Mechanic Course) — Astro + Tailwind, static, SEO-first, dengan blog artikel (MDX).
Rencana lengkap: [`docs/PLAN.md`](docs/PLAN.md).

## Menjalankan di komputer sendiri
Butuh Node.js 22+ (https://nodejs.org).
```bash
git clone https://github.com/achanim/mec-academy.git
cd mec-academy
git checkout claude/new-repo-infra-tech-stack-e62imy
npm install
npm run dev            # buka http://localhost:4321
```
Untuk melihat versi production (termasuk pencarian artikel): `npm run build && npm run start`, lalu buka http://localhost:4321.

## Deploy (Cloudflare Pages, gratis)
1. Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git → pilih repo ini.
2. Build command: `npm run build` · Output directory: `dist` · Node version: `22` (env `NODE_VERSION=22`).
3. Setiap PR otomatis dapat URL preview; merge ke `main` = production.
4. Ganti domain placeholder `mecacademy.id` di `astro.config.mjs`, `src/lib/site.ts`, `public/robots.txt`.

## Perintah
```bash
npm install
npm run dev        # dev server
npm run check      # typecheck
npm test           # vitest
npm run build      # output ke dist/
npm run extract -- path/ke/MEC_UI_Preview.html   # ekstrak aset & konten dari preview (sekali jalan)
```

## Struktur
- `src/data/*.json` — konten hasil ekstraksi preview (modul, instruktur, fasilitas, dst.)
- `src/content/articles/` — artikel MDX (schema di `src/content.config.ts`)
- `src/assets/` — gambar & font woff2
- `public/_headers`, `_redirects`, `robots.txt` — konfigurasi Cloudflare Pages

Menambah artikel: buat file `.mdx` di `src/content/articles/`, isi frontmatter, commit.
