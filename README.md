# MEC Academy

Situs MEC Academy (Basic Mechanic Course) — Astro + Tailwind, static, SEO-first, dengan blog artikel (MDX).
Rencana lengkap: [`docs/PLAN.md`](docs/PLAN.md).

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
