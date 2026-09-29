# TODO — MEC Academy

Diperbarui: 2026-09-29 · Branch: `claude/new-repo-infra-tech-stack-e62imy`
Kondisi terakhir: `astro check` 0 error · 9 test lolos · build 44 halaman · Pagefind terindeks

## Selesai

**Fondasi**
- [x] Plan infra & tech stack (`docs/PLAN.md`)
- [x] Scaffold Astro 7 + Tailwind 4 + MDX, CI (check/test/build), vitest
- [x] Ekstraksi aset & konten dari preview (21 MB → gambar master ±7 MB, font woff2) — `npm run extract`
- [x] Font: Nimbus Sans (AGPL, abu-abu untuk web) diganti Archivo + Archivo Narrow (OFL); DejaVu Sans Mono di-subset 147 KB → 8,6 KB. Lisensi di `public/licenses/`

**Beranda & animasi**
- [x] Beranda 12 bab setara preview: layar intro + logo, header/menu, heading dua warna, dot & bar status bab, zoom hero, detail tiap bab
- [x] Animasi scroll: 7 bab di-pin (hero, challenge, journey, machine, learning, character, film), kamera zoom, word-mask, rail horizontal, tab mesin 3D otomatis, wipe karakter, zoom video. Fallback untuk HP, reduced-motion, save-data, layar pendek (`src/scripts/motion.ts`, `home.ts`)
- [x] Scroll dipersingkat: durasi pin dipangkas, bab Alumni tidak di-pin, daftar horizontal di HP (desktop ±24 → ±18 layar)
- [x] Layar intro masuk otomatis (±1,4 dtk), tombol lewati aktif dari awal, dilewati untuk crawler & pengunjung kembali dalam sesi

**Halaman & konten**
- [x] Halaman: BMC, 16 modul (kartu berkelompok, prev/next), tahapan, fasilitas + lightbox, instruktur + profil per orang, industri, sumber, tentang (visi/misi/tim), assessment (langkah + FAQ), kontak (kartu, cara mendaftar, peta), `/faq/`
- [x] Ringkasan FAQ & chip mitra industri di beranda; footer lengkap
- [x] Sistem artikel (MDX, kategori, cover, FAQ/BlogPosting/Breadcrumb JSON-LD), RSS, sitemap, Pagefind
- [x] Menu hamburger grid 2 kolom, muat satu layar

**Kualitas**
- [x] Skeleton loading + error handling (404/500, gambar rusak, video gagal/offline, Pagefind gagal, error JS global, banner offline)
- [x] Responsive diuji di 320/360/390/820/1000/1024/1920 px — tanpa scroll horizontal; target sentuh ≥32px di HP (footer/chip/breadcrumb ≥44px)
- [x] Audit UI/UX (`docs/UIUX-AUDIT.md`): lantai font 12px, titik fokus foto, scrim teks di atas foto, hijau aksen di latar terang, state `:active/:disabled`, judul panjang title case

## Sebagian selesai (butuh keputusan/lanjutan)
- [ ] **Skala tipografi penuh** — token `--fs-*` sudah ada, belum dipakai di semua komponen (audit A2)
- [ ] **Ruang kosong di bab yang di-pin** — mis. bab Tantangan: konten ±45% dari tinggi layar (audit D1). Opsi: perbesar elemen atau tambah foto pendukung
- [ ] **Heading display** masih 72–110px di beberapa bab (audit A5) — sengaja dibiarkan agar sama dengan preview; putuskan mau diturunkan atau tidak
- [ ] **Emas dipakai banyak peran** (audit B3) — eyebrow tetap emas mengikuti preview; putuskan apakah dikurangi
- [ ] **Bukti sosial** (audit E3) — FAQ & chip mitra sudah ada; testimoni & logo mitra belum ada datanya

## Menunggu data / keputusan dari klien
- [ ] Domain final → ganti placeholder `mecacademy.id` di `astro.config.mjs`, `src/lib/site.ts`, `public/robots.txt`
- [ ] **Foto asli resolusi tinggi dari MEC** (foto lebar ≥1600px, potret instruktur ≥600px) — sumber sekarang thumbnail PDF (475–734px), buram di layar retina (audit C2). Setelah masuk: jalankan ulang `npm run extract`/ganti file di `src/assets/images/`
- [ ] Deskripsi/tujuan/materi **12 modul** (baru 4 modul punya deskripsi; sisanya memakai teks umum + tombol "Tanya silabus")
- [ ] Konfirmasi **pengelompokan 16 modul** (Dasar / Sistem penggerak / Kemudi & roda / Perawatan) — ini pengelompokan tim web, bukan dari company profile
- [ ] Konfirmasi ejaan nama instruktur "Johan Winarto/Wiharto"
- [ ] Info **biaya, jadwal, persyaratan** untuk dicantumkan (sekarang FAQ mengarahkan ke tim MEC) dan **jam operasional** untuk halaman Kontak
- [ ] Testimoni alumni & izin memakai logo mitra industri
- [ ] Setuju/tidak dengan intro otomatis dan dilewati untuk crawler (sebelumnya wajib klik)
- [ ] Multi-bahasa (EN)? — putuskan sebelum struktur URL dikunci

## Teknis berikutnya
- [ ] Deploy Cloudflare Pages (connect repo, `NODE_VERSION=22`), DNS, redirect dari domain lama
- [ ] CMS editor artikel (Keystatic/Decap) — butuh keputusan hosting & login GitHub
- [ ] OG image dinamis per artikel (Satori) + OG default yang proper (sekarang crop hero)
- [ ] Riset keyword + kalender editorial; tulis 5–10 artikel awal per pilar topik
- [ ] Analytics (Plausible/Umami) + Google Search Console + submit sitemap
- [ ] Form lead (Cloudflare Worker + Turnstile) bila WhatsApp saja tidak cukup
- [ ] CSP header, Lighthouse CI budget, a11y test (axe) di CI, link-check
- [ ] Simpan skrip audit (font/kontras/gambar/overflow) ke repo (`scripts/`) dan jalankan di CI — sekarang masih skrip sementara
- [ ] Uptime monitoring

## Belum diverifikasi
- [ ] Perangkat fisik: iOS Safari, Android Chrome, landscape di HP (baru Chromium dengan emulasi ukuran layar)
- [ ] Firefox & Safari desktop (animasi pin, `color-mix`, `clip-path`)
- [ ] Lighthouse nyata (LCP/CLS/INP) — angka performa sejauh ini estimasi dari bobot aset, bukan hasil Lighthouse
- [ ] Kontras teks di atas foto diukur per piksel (sekarang hanya ditambah scrim + pengecekan visual)
- [ ] Uji Search Console "Live Test" untuk memastikan intro tidak menutupi konten saat dirender Googlebot
