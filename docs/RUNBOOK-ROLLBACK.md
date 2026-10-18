# Runbook: jika akun trial Rumahweb berhenti

Situs `malangeducationcenter.com` dan 9 kotak surat berjalan di akun **Free Account (trial)** yang tidak bisa di-upgrade, tanpa jatuh tempo tertulis, daily backup mati. Dokumen ini langkah memulihkan layanan di paket lain.
Hostinger tidak lagi menjadi cadangan (berakhir 15 Okt 2026, tidak diperpanjang).

## Persiapan SEKARANG (murah, memperpendek pemulihan nanti)
- [ ] **Turunkan TTL record `A @`, `www`, dan `MX` di zona cPanel ke 300 detik** supaya perpindahan nanti merata dalam menit, bukan jam.
- [ ] **Simpan salinan konfigurasi** (di luar repo): isi zona DNS (screenshot Zone Editor), daftar 9 kotak surat (jumlah dan kuota; sandi di pengelola sandi), pengaturan `.htaccess`.
- [ ] Simpan salinan **`dist/` terbaru** (zip) di luar server.
- [ ] **Cadangkan email berkala:** tiap staf salin surat ke *Folder Lokal* Thunderbird; atau minta tiket Rumahweb mengaktifkan daily backup (`docs/TIKET-RUMAHWEB.md`).
- [ ] Catat tanggal berakhir trial begitu Rumahweb menjawab tiket.
- [ ] Kalender: ingatkan 7 hari sebelum tanggal berakhir.

## Opsi hosting pengganti
| Opsi | Kapan dipilih |
|---|---|
| **A. Addon domain di `Unlimited M` (portal `.my.id`)** | tercepat dan tanpa biaya tambahan; kuota addon tidak terbatas; satu paket dengan portal (jatuh tempo bersama; aktifkan Auto Renew). Domain `.com` harus **dilepas dari akun trial** lebih dulu (tiket) |
| **B. Paket baru lewat Order** (Rumahweb) | bila ingin terpisah dari portal; ada biaya baru |

## Langkah pemulihan (±2–4 jam kerja + propagasi)
1. **Tentukan paket pengganti** (A atau B) dan siapkan akses cPanel-nya.
2. **Pasang situs:** tambahkan domain (addon atau domain utama paket baru), unggah isi `dist/` ke `public_html` (lewat File Manager, zip dipecah; lihat `docs/CICD.md`). Uji lewat file `hosts` ke IP server baru.
3. **Buat ulang kotak surat** (9 buah) dengan sandi baru; atur ulang aplikasi email staf (`docs/PANDUAN-EMAIL-STAF.md`). **Isi surat lama tidak otomatis ikut**; pulihkan dari Folder Lokal Thunderbird staf atau backup bila ada.
4. **Bangun zona DNS di paket baru:** `A @` ke IP server baru, `www` CNAME ke `@`, `MX` ke `mail.<domain>` (prioritas 0) dengan `A mail`, SPF `v=spf1 +a +mx +ip4:<IP baru> ~all`, DKIM dari cPanel (Email Deliverability), DMARC `v=DMARC1; p=none`, tanpa AAAA.
5. **Ganti nameserver** di client zone Rumahweb ke nameserver hosting baru (bila server berbeda dan zona dikelola di paket baru). Bila server sama/DNS tetap, cukup ubah record.
6. Setelah domain mengarah ke server baru: **Run AutoSSL** (cPanel > SSL/TLS Status). HSTS situs memakai `includeSubDomains`, jadi pastikan `mail.`/`webmail.` ikut bersertifikat valid.
7. **PHP:** di server baru pilih **PHP 8.1+** (MultiPHP Manager) dan salin blok `# php -- BEGIN cPanel-generated handler` baru dari `.htaccess` server ke `public/.htaccess` repo sebelum deploy; tanpa itu `/kelola-foto/` 500. Pulihkan folder `alumni-foto/` dari cadangan dan buat ulang sandi admin (`docs/ALUMNI-ADMIN.md`).
8. Verifikasi: `https://malangeducationcenter.com/` 200, redirect lama 301, kirim/terima email dua arah, mail-tester. Perbarui `.env.deploy` (FTP_HOST/USER/PASS) untuk `npm run deploy`.

**Estimasi:** kerja aktif 2–4 jam; dengan TTL 300 detik, propagasi biasanya <1 jam; resolver bandel hingga 4 jam; delegasi nameserver bisa sampai 48 jam bila NS berganti.

## Jawaban tiket (isi setelah ada)
- Boleh produksi? …
- Masa berakhir? …
- Dampak ke email/DNS? …
- Bisa dijadikan berbayar tanpa ganti server? …
