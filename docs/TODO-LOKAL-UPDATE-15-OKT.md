# TODO tim lokal: deploy update terbaru + tindak lanjut SEO (15 Okt 2026)

Aturan: jangan memasukkan sandi/token/IP ke repo; perubahan di server atau akun pihak ketiga hanya atas persetujuan pemilik. Detail SEO lengkap ada di `docs/TODO-LOKAL-SEO.md` (bagian B-F); daftar ini merangkum yang paling mendesak dan urutannya.

## 1. Ambil dan deploy update terbaru (cabang `staging`)
Perubahan sejak deploy terakhir:
- SEO (`5175d6c`): judul/deskripsi, JSON-LD organisasi, `og:image` per halaman, kategori artikel tipis `noindex` + keluar sitemap, redirect `/program/` dan `/artikel/kategori/`, header `X-Frame-Options`, kait verifikasi/analitik.
- Beranda (`98aa2a8`, `e20ba1a`): bab Alumni dan OJT jadi bab 02 dan berlatar gelap.
- Dokumen: serah terima (`docs/HANDOVER.md`), panduan update kode (`docs/PANDUAN-UPDATE-KODE-DAN-DEPLOY.md` + PDF `docs/Panduan-Update-Situs-MEC-Academy.pdf`).

Langkah:
- [ ] `git pull origin staging`, `npm install`.
- [ ] `npm run check && npm test` (harus bersih, 10 tes lulus).
- [ ] **Pastikan `public/.htaccess` hasil build masih memuat blok PHP handler cPanel** (PHP 8.3). Tanpa itu `/kelola-foto/` kembali 500.
- [ ] `DRY_RUN=1 npm run deploy`, periksa daftar berkas, lalu `npm run deploy`.
- [ ] Segarkan keras beranda: urutan bab hero, Alumni (gelap), Tantangan (terang); cek di HP juga (tanpa animasi pin).
- [ ] Jalankan verifikasi live `docs/TODO-LOKAL-SEO.md` bagian A (301 `/program/`, `X-Frame-Options`, sitemap 37 URL, noindex kategori, `og:image` unik 1200x630, judul beranda ≤ 55 huruf). Bila `.htaccess` baru menimbulkan 500, rollback sesuai `docs/RUNBOOK-ROLLBACK.md`.
- [ ] `/kelola-foto/` masih bisa dibuka dan login; `/alumni/` tetap menampilkan foto.
- [ ] Laporkan hasil (lulus/gagal per butir, tanpa kredensial).

## 2. Keputusan cabang
- [ ] Tanyakan pemilik: gabungkan `staging` ke `main`? Panduan klien menyuruh deploy dari `main`, sedangkan `main` tertinggal dari `staging`. **Jangan merge/push ke `main` tanpa persetujuan.**

## 3. SEO: yang bisa dikerjakan tim lokal (butuh akun/browser)
Urutan prioritas:
1. [ ] **Google Search Console**: properti Domain (TXT di cPanel Zone Editor) atau awalan URL (meta; isi `site.verification.google` di `src/lib/site.ts` lalu deploy). Kirim `sitemap-index.xml`; minta indeks ulang `/` dan `/alumni/`. Pakai akun milik MEC. Panduan: `docs/SEARCH-CONSOLE.md`.
2. [ ] **Google Business Profile**: klaim/periksa profil (nama, alamat Jl. Jatisari No. 07 Plaosan Wonosari, telepon, URL situs, kategori Lembaga pelatihan, jam, foto, tautan WA).
3. [ ] **Bing Webmaster Tools**: impor dari Search Console.
4. [ ] **Analitik** (Plausible atau Umami, pilih 1): isi `site.analytics` di `src/lib/site.ts`, deploy, pastikan peristiwa `WhatsApp` muncul di dasbor.
5. [ ] **Rich Results Test** untuk `/` dan `/program/basic-mechanic-course/` (Organisasi/LocalBusiness dan Course tanpa galat).
6. [ ] **TTFB dari Jakarta** (PageSpeed Insights/WebPageTest). Bila konsisten > 800 ms: cek cache LiteSpeed di cPanel.
7. [ ] **CSP Report-Only** (`docs/REVIEW-HEADERS.md` §2): pasang, amati konsol 1-2 minggu (dialog, galeri, YouTube), baru jadikan enforcing. Persetujuan pemilik dulu.

## 4. Data dari MEC (tanyakan ke pemilik, lalu isi di `src/lib/site.ts`)
- [ ] Jam operasional (`openingHours`), koordinat pin Maps (`geo`), tautan sosial resmi (`social`; konfirmasi Instagram `malangeducation`).
- [ ] Biaya dan jadwal batch bila boleh dipublikasikan (lalu tambahkan `offers`/`hasCourseInstance` di skema Course).
- [ ] Foto asli resolusi tinggi dan logo vektor (`docs/TODO-BAHAN-ASLI.md`), 12 deskripsi modul, ejaan Johan, redaksi SAA (`docs/DRAFT-KONTEN-UNTUK-MEC.md`).
- [ ] Izin alumni/testimoni; isi galeri via `/kelola-foto/`.

## 5. Operasional
- [ ] Cadangan berkala folder `alumni-foto/` ke luar server (trial tanpa cadangan harian).
- [ ] Jawaban tiket Rumahweb soal masa berlaku trial dan jalur pindah ke paket berbayar; laporkan ke pemilik (`docs/TIKET-RUMAHWEB.md`, `docs/RUNBOOK-ROLLBACK.md`).
- [ ] Pastikan staf sudah memindahkan surat lama dari Hostinger (batas 15 Okt) dan DNS bersih dari rujukan Hostinger.
- [ ] Bersama pemilik: jadwalkan transfer repositori ke akun MEC, isi alamat repositori di panduan klien, buat akun FTP deploy untuk pengelola, ganti semua sandi proyek dan aktifkan 2FA saat serah terima (`docs/HANDOVER.md`).

## 6. Yang sengaja tidak dikerjakan
- `lastmod` sitemap (tanggal bangun bukan tanggal ubah), versi bahasa Inggris (belum diputuskan), menulis artikel tanpa data dari MEC.
