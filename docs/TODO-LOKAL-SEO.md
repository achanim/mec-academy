# TODO untuk Claude lokal / pemilik: SEO dan audit (butuh akses akun, browser, atau data MEC)

Disusun 13 Okt 2026 setelah audit (`docs/AUDIT-SEO-2026-10-13.md`). Perbaikan yang bisa dikerjakan di kode **sudah dikerjakan** di `staging`; daftar ini hanya sisanya. Aturan umum: jangan memasukkan sandi, token, atau data pribadi ke repo; perubahan di server atau akun pihak ketiga hanya atas persetujuan pemilik.

## A. Segera setelah `git pull` (perlu `npm run deploy`)
- [ ] `git pull`, `npm install`, `DRY_RUN=1 npm run deploy`, lalu `npm run deploy`.
- [ ] Verifikasi live (publik, tanpa login):
  - `curl -sI https://malangeducationcenter.com/program/` → 301 ke `/program/basic-mechanic-course/` (sebelumnya 403); `/artikel/kategori/` → 301 ke `/artikel/`.
  - `curl -sI https://malangeducationcenter.com/ | grep -i x-frame` → `SAMEORIGIN`.
  - `https://malangeducationcenter.com/sitemap-0.xml` berisi **37 URL** (tanpa `/artikel/kategori/*`); halaman kategori memuat `noindex`.
  - Judul beranda ≤ 55 huruf (`MEC Academy: Pelatihan Mekanik Alat Berat di Malang`); judul `/alumni/`, `/fasilitas/`, `/tentang/`, `/instruktur/` memuat "Malang".
  - `og:image` tiap halaman konten berbeda dan 1200×630 (cek `curl -s https://malangeducationcenter.com/alumni/ | grep og:image`).
  - Uji asap deploy lolos; bila `.htaccess` baru membuat 500, rollback segera (`docs/CICD.md`).

## B. Akun dan alat (hanya pemilik/MEC yang bisa)
- [ ] **Google Search Console**: buat properti (Domain, TXT di cPanel Zone Editor, atau awalan URL dengan meta). Bila memakai meta, isi `site.verification.google` di `src/lib/site.ts` (nilai `content=` dari Google), deploy, lalu Verifikasi. Kirim `sitemap-index.xml`, minta indeks ulang beranda dan `/alumni/`. Panduan: `docs/SEARCH-CONSOLE.md`. Catat siapa pemilik akunnya.
- [ ] **Bing Webmaster Tools**: impor dari Search Console (atau isi `site.verification.bing`).
- [ ] **Google Business Profile**: klaim atau periksa profil MEC Academy (nama, alamat Jl. Jatisari No. 07 Plaosan Wonosari, telepon, URL `https://malangeducationcenter.com/`, kategori "Lembaga pelatihan", jam operasional, foto, tautan WhatsApp).
- [ ] **Analitik**: pilih penyedia ramah privasi (Plausible atau Umami; cukup 1), buat akun, lalu isi `site.analytics` di `src/lib/site.ts` (contoh Plausible sudah ada di komentar). Klik WhatsApp otomatis tercatat sebagai peristiwa `WhatsApp` (kode di `src/scripts/ui.ts`; tidak aktif bila analitik kosong). Beri tahu pengunjung bila perlu (kebijakan privasi singkat). Verifikasi peristiwa muncul di dasbor setelah deploy.

## C. Data dari MEC yang membuka perbaikan kode (semua kolom sudah disiapkan di `src/lib/site.ts`, tinggal diisi)
- [ ] **Jam operasional**, isi `site.openingHours` (data terstruktur LocalBusiness).
- [ ] **Koordinat**, isi `site.geo` (ambil dari pin Google Maps profil bisnis).
- [ ] **Tautan sosial resmi** (Facebook, LinkedIn, YouTube, TikTok bila ada), tambahkan ke `site.social` (Instagram `malangeducation` sudah dimasukkan dari situs lama; konfirmasi akunnya resmi).
- [ ] **Biaya dan jadwal batch** (bila boleh dipublikasikan) → halaman/FAQ; setelah ada, tambahkan `offers` dan `hasCourseInstance` pada skema `Course` (`src/pages/program/basic-mechanic-course/index.astro`).

## D. Konten dan foto (butuh orang/data, bukan kode)
- [ ] **Artikel awal 5–10 buah** mengikuti `docs/RENCANA-KONTEN-SEO.md` (kata kunci, kerangka, data yang dibutuhkan). Setiap kategori baru diindeks otomatis setelah punya ≥ 3 artikel (`MIN_ARTICLES`).
- [ ] **Foto resolusi tinggi dan logo vektor**: `docs/TODO-BAHAN-ASLI.md`. Setelah itu `og-default.jpg` (sekarang crop hero) bisa diganti gambar berbagi yang dirancang.
- [ ] **12 deskripsi modul**, redaksi SAA, ejaan Johan, jam operasional: `docs/DRAFT-KONTEN-UNTUK-MEC.md`.
- [ ] **Isi galeri alumni** lewat `/kelola-foto/` (sekarang 0 foto, tampil 2 foto bawaan); pastikan izin alumni.
- [ ] **Testimoni alumni dan logo mitra** (izin tertulis).

## E. Pengukuran dan keamanan lanjutan
- [ ] **TTFB dari Indonesia**: PageSpeed Insights atau WebPageTest (lokasi Jakarta). Dari lingkungan audit TTFB 1,2–2,1 dtk (belum tentu mewakili). Bila konsisten > 800 ms: cek cache LiteSpeed di cPanel atau pakai CDN gratis.
- [ ] **Rich Results Test** (search.google.com/test/rich-results) untuk beranda dan `/program/basic-mechanic-course/`: pastikan Organisasi/LocalBusiness dan Course terbaca tanpa galat.
- [ ] **CSP Report-Only** (`docs/REVIEW-HEADERS.md` §2): tambahkan header, amati konsol browser 1–2 minggu (dialog, galeri, video YouTube), baru beralih ke `Content-Security-Policy`. Sengaja belum dipasang karena butuh pengamatan di browser nyata.
- [ ] **Cadangan berkala** folder `alumni-foto/` (akun trial tanpa cadangan harian) dan jadwal mengingatkan masa berlaku trial setelah tiket Rumahweb dijawab.

## F. Strategis (opsional)
- [ ] Backlink lokal: direktori pendidikan/pelatihan, profil LinkedIn lembaga dan instruktur, kerja sama industri yang menyebut dan menaut MEC.
- [ ] Versi bahasa Inggris (belum ada keputusan).
- [ ] Sitemap `lastmod`: **sengaja tidak ditambahkan**; tanggal bangun bukan tanggal ubah konten, dan Google mengabaikan `lastmod` yang tidak akurat. Tambahkan bila nanti ada tanggal ubah per halaman yang tepercaya.
