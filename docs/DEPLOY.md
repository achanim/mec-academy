# Rencana deploy — malangeducationcenter.com ke Rumahweb

Diperbarui: 2026-10-01. Status: rencana (belum dijalankan).

## Temuan
- **Situs sekarang** `malangeducationcenter.com`: dibuat dengan **Hostinger Website Builder (Zyro)** dan dilayani dari Hostinger (header `x-powered-by: HostingerWebsiteBuilder`), bukan Rumahweb. Tidak ada blog. `www` sudah 301 ke tanpa-www.
- **Alamat lama** (dari sitemap): `/`, `/organisasi`, `/galeri`, `/alumni`, `/hubungi-kami`, `/assessment`, `/learning`. Alamat ini sudah punya riwayat di Google, jadi harus dialihkan (301) ke alamat baru.
- **Rumahweb** (dari halaman promo; harga promo, cek ulang saat checkout): cPanel, SSL gratis (Let's Encrypt), backup mingguan. Entry Rp 180 rb/th (1 GB SSD), Small Rp 99 rb/th (promo), Medium Rp 199 rb/th (SSH/Git/Node.js), Large Rp 299 rb/th. Harga promo biasanya hanya tahun pertama; cek harga perpanjangan.
- **Situs baru** statis: `dist/` ±15 MB, tidak butuh PHP/Node di server, jadi paket terkecil sudah cukup.

## Yang disesuaikan di repo
| Hal | Sebelumnya | Sekarang |
|---|---|---|
| Domain di config, sitemap, robots | placeholder `mecacademy.id` | `malangeducationcenter.com` |
| `_headers`, `_redirects` | khusus Cloudflare/Netlify, tidak jalan di cPanel | tetap ada, ditambah `public/.htaccess` (HTTPS, www→apex, redirect alamat lama, 404/500, gzip, cache, header keamanan) |
| Deploy | rencana Cloudflare Pages | workflow manual `deploy-rumahweb.yml` (FTPS ke `public_html/`) |
| Judul beranda | "Kursus Mekanik Alat Berat di Malang" | memuat "Pelatihan Teknik Alat Berat di Malang \| Malang Education Center" agar dekat dengan judul lama di Google |

Peta redirect alamat lama (perlu dikonfirmasi):
`/organisasi`→`/tentang/` · `/galeri`→`/fasilitas/` · `/alumni`→`/industri/` · `/hubungi-kami`→`/kontak/` · `/learning`→`/program/basic-mechanic-course/` · `/assessment`→`/assessment/`

## Langkah (urutan aman, tanpa downtime)
1. **Pilih paket.** Entry/Small cukup (tanpa SSH). Pakai FTPS dari GitHub Actions; kalau ambil Medium+, bisa pakai SSH/rsync.
2. **Cek dulu situasi domain.** Siapa registrar (Hostinger? Rumahweb?), dan apakah ada **email di domain ini** (MX). Kalau ada email, catat record MX/SPF/DKIM supaya tidak putus saat DNS dipindah.
3. **Tambahkan domain ke cPanel Rumahweb** (Addon/Primary Domain) **tanpa mengubah DNS dulu**. Uji lewat URL sementara atau file `hosts`.
4. **Build dan unggah:** jalankan workflow *Deploy ke Rumahweb* (atau unggah isi `dist/` ke `public_html/` lewat File Manager/FTP). Pastikan `.htaccess` ikut terunggah (berkas tersembunyi).
5. **Uji di Rumahweb:** semua halaman terbuka, `www`→apex, HTTP→HTTPS, redirect alamat lama, halaman 404, pencarian (Pagefind), gambar dan font, galeri, tombol WhatsApp.
6. **Pastikan SSL aktif** (AutoSSL Let's Encrypt di cPanel) sebelum DNS dipindah.
7. **Cutover DNS:** turunkan TTL ke 300 detik sehari sebelumnya; arahkan A record (atau nameserver) ke Rumahweb; salin record email jika ada. Biarkan paket Hostinger aktif 1–2 minggu sebagai cadangan.
8. **Search Console:** tambahkan properti, kirim `sitemap-index.xml`, periksa Coverage dan 404 selama 2–4 minggu. Karena domainnya sama, tidak perlu Change of Address.
9. **Setelah stabil:** matikan paket Hostinger. Jalankan `AUDIT_URL=https://malangeducationcenter.com npm run audit:lh` untuk Lighthouse di situs online.

## Risiko dan hal yang perlu dikonfirmasi
- **Email di domain** (lihat langkah 2): kalau ada dan DNS dipindah tanpa menyalin MX, email bisa berhenti.
- **Portal assessment** tetap di `malangeducationcentreacademy.my.id/assessment/`; tidak ikut dipindah.
- **Hosting dibeli atas nama MEC**, bukan pribadi, supaya kepemilikan jelas.
- Server Rumahweb umumnya LiteSpeed (kompatibel `.htaccess`); kalau ternyata Nginx murni, aturan redirect/cache perlu dipindah ke konfigurasi lain.
- `/alumni` dialihkan ke `/industri/` karena belum ada halaman alumni sendiri; ganti bila ingin tujuan lain.
- Batas "unlimited" pada paket murah umumnya ada kebijakan pemakaian wajar; situs statis ringan jauh di bawah batas itu.
