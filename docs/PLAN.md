# MEC Academy — Plan Infra & Tech Stack

Status: **disetujui — Fase 0–1 selesai, Fase 2 berikutnya** · Dasar: `MEC_UI_Preview.html` (V5.1) + Company Profile MEC Academy 2026

## 1. Hasil analisis preview

Preview saat ini satu file HTML 21 MB. Isinya:

| Aspek | Temuan | Konsekuensi |
|---|---|---|
| Ukuran | ~21 MB, hampir semuanya gambar & 4 font di-embed base64 (±55 gambar) | Tidak bisa dipakai production. Harus jadi file terpisah, AVIF/WebP, responsive `srcset`, font woff2 |
| Konten | Ada di JS (`mecContent`, `mecResearch`, `mecGallery`) dan dirender via modal | Google tidak melihat konten sebagai halaman. **Harus jadi halaman HTML sungguhan** |
| Routing | Satu halaman, `#assessment` via `location.hash` + `pushState` | Tidak ada URL yang bisa di-index. Perlu real routes |
| Motion | Scroll-choreography custom (`MECMotion`, pinned scene, rail, zoom portal), tanpa WebGL/CDN, ada mode `calm`/reduced-motion | Bagus & sudah pure-function → bisa dipindah utuh sebagai modul kecil (JS ringan) |
| Tampilan | Bahasa ID, palet hijau tua `#265154` / gold `#CDBE86` / paper `#F3F0E4`, font display/body/mono (kini Archivo Narrow, Archivo, DejaVu Sans Mono) | Jadi design tokens |
| CTA | Semua konversi lewat WhatsApp `wa.me/6282229985588` + link ke portal assessment eksternal | Tidak butuh backend auth/payment sekarang |
| Video | YouTube (nocookie) di modal | Lazy-load facade (jangan load iframe sebelum klik) |

Konten yang sudah terstruktur (bisa langsung jadi data): 16 modul, 7 komponen, tahapan seleksi/training, 6 instruktur, fasilitas, 7 sektor industri, 8+ event industri, 20 foto galeri, tim, sejarah 2018→2025, legalitas, kontak.

**Kesimpulan:** ini bukan web app, ini **situs konten/marketing dengan animasi berat + blog artikel yang SEO-driven**. Prioritas: HTML statis cepat, SEO, dan kemudahan menulis artikel.

## 2. Rekomendasi tech stack

### Framework: **Astro 5** (+ TypeScript)
- Static-first, HTML siap crawl, JS hanya di "island" yang butuh (motion, galeri, modal) → Core Web Vitals terbaik.
- **Content Collections + MDX**: artikel, instruktur, modul, event = file/data bertipe (Zod schema). Ini fondasi scalable untuk ratusan artikel.
- Image pipeline bawaan (`astro:assets`): AVIF/WebP, responsive, lazy — langsung menyelesaikan masalah 21 MB.
- Sitemap, RSS, view transitions tersedia sebagai integrasi resmi.

Kenapa bukan Next.js: kita tidak butuh React runtime di halaman marketing/artikel; bundle lebih besar, SEO sama tapi CWV lebih sulit dijaga. Kalau nanti ada portal siswa/dashboard, itu **aplikasi terpisah** (subdomain), bukan alasan membebani situs publik.

### Lapisan lain
| Kebutuhan | Pilihan | Alasan |
|---|---|---|
| Styling | Tailwind CSS v4 + CSS variables dari token preview | Cepat, konsisten; animasi scroll tetap CSS var (`--p`, `--reveal-y`) seperti preview |
| Motion | Port `MECMotion` (vanilla TS) + `IntersectionObserver`; CSS `animation-timeline: scroll()` sebagai progressive enhancement | Sudah ada, tanpa dependensi; hormati `prefers-reduced-motion` |
| Interaktif | Vanilla / Astro islands; Preact hanya jika perlu (assessment guide, filter artikel) | Minim JS |
| Artikel | MDX di repo (Content Collections) → **Keystatic** atau **Decap CMS** untuk editor non-teknis (commit ke Git) | Tanpa DB, versioned, gratis. Upgrade path: Sanity/Payload bila tim editor membesar |
| Search artikel | **Pagefind** (index statis saat build) | Tanpa server |
| Form/lead | Fase 1: tetap WhatsApp (sudah bekerja). Fase 2: Cloudflare Worker + D1/KV + Turnstile | Tanpa server sendiri |
| Analytics | Plausible/Umami (privacy) + Google Search Console + GA4 opsional | |
| Test/QA | Vitest (unit `MECMotion` — sudah pure functions), Playwright (smoke + a11y axe), Lighthouse CI | |
| Lint | ESLint, Prettier, `astro check` | |

## 3. Infra

```
GitHub (achanim/mec-academy)
  └─ PR → GitHub Actions: lint, typecheck, test, build, Lighthouse CI, link-check
        ├─ Preview deploy per PR (Cloudflare Pages)
        └─ merge main → Production deploy
Cloudflare
  ├─ Pages (static hosting, global CDN, HTTP/3, Brotli)  ← situs
  ├─ R2 (opsional: aset besar/foto asli, video)          ← bila galeri membesar
  ├─ Workers + D1/KV (form lead, redirect, API kecil)     ← fase 2
  ├─ DNS + SSL + WAF/Bot + Turnstile
  └─ Web Analytics / Plausible
```

**Kenapa Cloudflare Pages:** gratis untuk skala ini, CDN Indonesia/Asia baik, preview per PR, edge function bila perlu, dan bisa tumbuh ke Workers/D1/R2 tanpa ganti vendor. (Alternatif setara: Vercel/Netlify — tidak ada yang wajib.)

**Domain:** sekarang `malangeducationcenter.com` dan `malangeducationcentreacademy.my.id/assessment` (portal ujian, tetap eksternal). Rekomendasi: satu domain utama untuk situs baru (mis. `mecacademy.id`), `www` → apex 301, portal assessment tetap di subdomain/URL sekarang sampai ada rencana migrasi.

**Environments:** `main` = production, PR = preview, `staging` opsional. Secrets di Cloudflare/GitHub Secrets, tidak di repo.

## 4. Arsitektur situs & URL (SEO-ready)

```
/                          Beranda (12 bab preview jadi section landing)
/program/basic-mechanic-course/          Halaman Course utama (BMC)
/program/basic-mechanic-course/modul/    16 modul
/program/basic-mechanic-course/modul/[slug]/   mis. diesel-engine, hydraulic-system
/program/on-the-job-training/
/tahapan-seleksi/          Assessment → In-class → OJT
/fasilitas/                + galeri 20 foto
/instruktur/  /instruktur/[slug]/
/tentang/                  Sejarah ETTC→MEC→MEC Academy, visi misi, legalitas
/industri/                 Kemitraan & kunjungan industri (event)
/alumni/
/assessment/               Panduan + link login (portal eksternal)
/artikel/                  Index + pagination
/artikel/[slug]/           Artikel
/artikel/kategori/[kat]/   Hub kategori
/artikel/tag/[tag]/        (noindex jika tipis)
/kontak/  /faq/
/sitemap-index.xml  /rss.xml  /robots.txt  /404
```
Aturan URL: huruf kecil, tanpa tanggal di slug, trailing slash konsisten, canonical selalu absolut, 301 dari URL lama.

## 5. Strategi SEO & artikel

**Teknis (semua otomatis dari layout, bukan manual per halaman):**
- `<title>`, meta description, canonical, OG/Twitter, OG image dinamis per artikel (Satori/`@vercel/og` di build).
- **JSON-LD:** `EducationalOrganization` + `LocalBusiness` (alamat Malang, telp, jam), `Course` (BMC), `Article`/`BlogPosting`, `FAQPage`, `BreadcrumbList`, `Person` (instruktur), `VideoObject`.
- Sitemap otomatis (dengan `lastmod`), RSS, `robots.txt`, breadcrumb, internal linking otomatis (related articles, modul ↔ artikel).
- CWV target: LCP < 2.0 s, CLS < 0.05, INP < 200 ms, Lighthouse ≥ 95 (mobile). Hero image preload, font `woff2` subset + `font-display: swap`, animasi berat hanya desktop non-reduced-motion (seperti logika `motionAllowed` di preview).
- Aksesibilitas (WCAG AA): sudah bagus di preview (skip link, focus, `dialog`) — pertahankan; jalankan axe di CI.
- Konten kritis **tidak boleh** bergantung JS; mode `noscript` sudah dipikirkan di preview.

**Konten artikel (ada dari awal, bukan tambahan):**
- Content Collection `articles`: `title, description, slug, publishedAt, updatedAt, author (→ instruktur), category, tags, cover, faq[], relatedModules[], draft`.
- Pilar topik (usulan): *Karier mekanik alat berat*, *Pengetahuan teknis* (engine, hydraulic, power train, electrical), *K3 & budaya kerja*, *Industri & pertambangan*, *Info BMC/OJT*, *Cerita alumni*.
- Model **topic cluster**: 1 halaman pilar (mis. modul Hydraulic) ↔ banyak artikel pendukung, saling link.
- Keyword riset dulu (Search Console + Ahrefs/Ubersuggest): "kursus mekanik alat berat Malang", "cara jadi mekanik alat berat", "gaji mekanik alat berat", "pelatihan alat berat Jawa Timur" dll.
- Author = instruktur berpengalaman industri (E-E-A-T), `updatedAt` ditampilkan, sumber dikutip (seperti `sourceNote` di preview).
- Workflow editor: Keystatic UI → PR otomatis → preview → merge → publish. Jadwal publish via `publishedAt` + rebuild terjadwal.

## 6. Performa & aset

- Semua gambar → `/src/assets`, diproses AVIF/WebP, ukuran per breakpoint, `width/height` eksplisit; galeri lazy.
- Font: ekstrak 4 font dari base64 → `woff2`, self-host, preload 1–2 yang di atas fold. **Cek lisensi font MEC** sebelum publish.
- Video: facade (thumbnail + klik load `youtube-nocookie`).
- JS budget: < 60 KB gz di halaman artikel, < 120 KB gz di beranda.
- Cache: aset hashed `immutable`, HTML `s-maxage` + purge saat deploy.

## 7. Keamanan & operasional

- Header: CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` via `_headers`.
- Turnstile pada form, rate limit pada Worker; WhatsApp/telepon jangan di-hardcode di banyak tempat → satu `site.config`.
- Backup = Git. Monitoring: uptime (UptimeRobot/Better Stack), Search Console alert, Lighthouse CI budget.
- Privasi: banner hanya jika pakai cookie analytics; Plausible/Umami tanpa cookie.

## 8. Struktur repo (usulan)

```
mec-academy/
├─ src/
│  ├─ content/            # articles/, instructors/, modules/, events/ (MDX/JSON + schema)
│  ├─ components/         # Header, Footer, SEO, JsonLd, Gallery, VideoFacade, ...
│  ├─ layouts/
│  ├─ pages/
│  ├─ scripts/motion/     # port dari MECMotion (+ unit test)
│  ├─ styles/tokens.css   # warna, font, spacing dari preview
│  └─ assets/            # gambar & font hasil ekstraksi
├─ public/  (robots.txt, _headers, _redirects, favicon)
├─ scripts/extract-preview.mjs   # ekstrak gambar/font/konten dari preview HTML
├─ tests/  (vitest, playwright)
├─ .github/workflows/ci.yml
├─ docs/PLAN.md
└─ astro.config.mjs, tsconfig.json, package.json
```

## 9. Roadmap

| Fase | Isi | Hasil |
|---|---|---|
| 0 — Fondasi (½ minggu) | Init Astro+TS+Tailwind, tokens, CI, deploy preview Cloudflare, domain/DNS | Repo hidup, deploy otomatis |
| 1 — Ekstraksi (½ minggu) | Script ekstrak gambar/font/konten dari preview → `assets` + `content` (JSON/MDX), kompres | Aset & data bersih, ukuran normal |
| 2 — Beranda (1 minggu) | Port 12 bab + motion, header/footer, CTA WhatsApp, video facade | Beranda setara preview, Lighthouse ≥ 90 |
| 3 — Halaman inti (1–1,5 minggu) | BMC, modul (16), tahapan, fasilitas, instruktur, tentang, industri, assessment, kontak/FAQ | Semua URL indexable |
| 4 — SEO & Artikel (1 minggu) | Layout artikel, kategori, related, JSON-LD, sitemap/RSS, OG image, Pagefind, CMS Keystatic, 3–5 artikel awal | Blog siap produksi |
| 5 — Launch (½ minggu) | Redirect, Search Console, analytics, QA a11y/perf, uptime | Go-live |
| 6 — Growth | Publikasi artikel rutin, cluster, backlink, ukur & iterasi; form lead/Worker bila perlu | Trafik organik |

Estimasi total sampai launch: **± 4–5 minggu** satu developer.

## 10. Biaya (perkiraan)
Cloudflare Pages/DNS: gratis · Domain: ±Rp150–250rb/th · Plausible: ±$9/bln (atau self-host/Umami gratis) · Keystatic/Decap: gratis · Tools SEO: opsional. **Infra ≈ hanya biaya domain** di awal.

## 11. Keputusan yang perlu dikonfirmasi
1. Domain final yang dipakai? (dan apakah `malangeducationcenter.com` di-redirect)
2. Setuju Astro + Cloudflare Pages (vs Vercel/Next.js)?
3. Siapa yang menulis artikel & butuh editor UI (Keystatic) atau cukup menulis Markdown?
4. Lisensi font display/body/mono (kini Archivo Narrow, Archivo, DejaVu Sans Mono) — boleh dipakai web?
5. Perlu form pendaftaran sendiri, atau WhatsApp saja cukup?
6. Portal assessment tetap eksternal?
7. Perlu multi-bahasa (EN) di kemudian hari? (memengaruhi struktur URL sejak awal)
8. Catatan editorial di data preview: ejaan nama instruktur "Johan Wiharto/Winarto" belum konsisten — perlu konfirmasi.
