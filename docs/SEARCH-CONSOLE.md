# Google Search Console: verifikasi ulang dan sitemap

Domain tetap `malangeducationcenter.com`, tetapi DNS dan server berganti, jadi properti lama (jika ada) mungkin kehilangan verifikasinya. Tidak ada TXT verifikasi Google di zona lama.

**Pertanyaan terbuka:** siapa pemegang akun Google yang dulu memverifikasi situs (atau apakah pernah ada)? Tanpa itu, buat properti baru dengan akun MEC dan catat siapa pemiliknya.

## Langkah (±15 menit)
1. https://search.google.com/search-console > **Tambahkan properti** > **Domain** > `malangeducationcenter.com`.
2. Google memberi record **TXT** (`google-site-verification=...`). Di cPanel > **Zone Editor** > Manage domain > **Add record**: type TXT, nama `malangeducationcenter.com.` (apex), isi persis dari Google. Tunggu beberapa menit, klik **Verifikasi**.
   - Alternatif bila TXT bermasalah: properti **Awalan URL** `https://malangeducationcenter.com/` dengan **berkas HTML**: unduh `googleXXXX.html`, taruh di `public/` repo, deploy.
3. **Sitemaps** > tambahkan `sitemap-index.xml` > Kirim. (File ada di `https://malangeducationcenter.com/sitemap-index.xml`.)
4. **Inspeksi URL** beranda > **Minta pengindeksan**.
5. Tambahkan pemilik cadangan (email kedua MEC) di *Setelan > Pengguna dan izin*.

## Pantau 2–4 minggu
- Laporan **Halaman**: URL lama (mis. `/organisasi`, `/galeri`, halaman templat toko) seharusnya berubah menjadi "Dialihkan" (301) atau "Tidak ditemukan/410"; ini normal. Halaman templat Hostinger (`classic-cap-…`, `face-serum-…` dll.) sengaja dibuat 410 agar keluar dari indeks.
- Periksa **Pengalaman halaman** dan **Core Web Vitals** setelah data terkumpul.
- Perbarui URL situs di **Google Business Profile** dan bio media sosial (domain sama; cek tautan).
- Karena domain sama, **tidak perlu** alat *Perubahan alamat*.
