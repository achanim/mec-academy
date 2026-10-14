# Serah terima ke MEC Academy (daftar periksa dan bahan penjelasan)

Disusun 14 Okt 2026. Tanpa kredensial: sandi diserahkan lewat pengelola sandi/kanal terpisah, bukan repo.

## 1. Sebelum menyerahkan (pengembang)
- [ ] **Email**: 9 kotak surat bisa kirim/terima dua arah (Gmail, Outlook), skor mail-tester wajar, sertifikat `mail.`/`webmail.` valid; staf sudah memindahkan surat lama dari Hostinger (batas 15 Okt).
- [ ] **DNS bersih**: tidak ada rujukan Hostinger (`NS`, `MX`, `TXT`, `CNAME`), lihat `docs/MIGRASI-HOSTINGER-KE-RUMAHWEB.md` §5.
- [ ] **Deploy terakhir** dari `main` (`npm run deploy`), uji asap lolos; `docs/TODO-LOKAL-SEO.md` bagian A dijalankan.
- [ ] **Cadangan final** tersimpan di luar server: `dist.zip` terakhir, folder `alumni-foto/`, arsip situs lama, arsip `admin.` dan `belajar.` (terenkripsi AES-256, salinan di Drive MEC; sandi arsip dikirim terpisah).
- [ ] **Ganti semua sandi yang pernah dipakai selama proyek** (cPanel, akun FTP deploy, 9 kotak surat sementara, sandi `/kelola-foto/`, akun registrar bila dibagikan) dan **cabut sesi/akses otomasi** (izin ekstensi browser, token GitHub, akun FTP yang tidak dipakai lagi). Aktifkan **2FA** di Rumahweb, GitHub, dan Google.
- [ ] Audit akhir: `npm run audit` (0 pelanggaran, Lighthouse hijau) dan pemeriksaan SEO `docs/AUDIT-SEO-2026-10-13.md`.
- [ ] Putuskan nasib branch: `main` = live (`staging` sama); `dev` (versi satu halaman) arsip atau hapus.

## 2. Kepemilikan dan akses yang diserahkan
| Item | Pemilik akhir | Kondisi sekarang | Tindakan |
|---|---|---|---|
| Domain `malangeducationcenter.com` | MEC (akun Rumahweb) | aktif s.d. 23 Agu 2028, **auto-renew OFF**, harga .COM naik per 15 Okt 2026 | MEC aktifkan auto-renew / catat tanggal; simpan kontak pemulihan |
| **Hosting situs** | MEC | **masih akun trial gratis**: tidak bisa di-upgrade, masa berlaku tak tertulis, tanpa cadangan harian. Situs dan 9 email bergantung padanya | **Keputusan MEC:** pindah ke paket berbayar (mis. Unlimited M) sesuai `docs/RUNBOOK-ROLLBACK.md`; jawaban tiket Rumahweb (`docs/TIKET-RUMAHWEB.md`) |
| Hosting portal assessment (`.my.id`) | MEC | jatuh tempo **19 Nov 2026**, auto-renew OFF | aktifkan auto-renew atau bayar sebelum tanggal itu |
| Email 9 kotak surat | MEC | di cPanel trial | sandi ke masing-masing staf; panduan `docs/PANDUAN-EMAIL-STAF.md` |
| cPanel dan akun FTP deploy | MEC (pemilik akun) | akun FTP deploy dibatasi `public_html` | serahkan; atau pertahankan akun FTP bila pengembang masih merawat |
| Kode sumber (repositori GitHub) | MEC setelah pelunasan (proposal Bagian 6.5) | repositori di akun pengembang | **transfer repositori ke akun/organisasi MEC**, atau serahkan arsip kode (`git bundle`/zip) + `docs/` |
| Pengelola foto alumni `/kelola-foto/` | admin MEC | sandi dibuat pemilik | dokumentasi `docs/ALUMNI-ADMIN.md`; ganti sandi saat ada admin berhenti |
| Google Search Console, Business Profile, Analitik | MEC | **belum terpasang** | buat dengan akun milik MEC (bukan pribadi pengembang), tambahkan pengembang sebagai pengguna bila perlu |
| Arsip situs lama, `admin.`, `belajar.` | MEC | tersimpan terenkripsi | serahkan lokasi dan cara membuka |
| Lisensi skrip komersial `belajar.` | pemegang lisensi (belum jelas) | diarsipkan, tidak dipindah | MEC konfirmasi pemegang lisensi dan bukti beli |
| Lisensi pihak ketiga | n/a | font Archivo (OFL), pustaka MIT/lainnya | salinan di `public/licenses/` |

## 3. Yang perlu disampaikan ke MEC (naskah awam)
1. **Yang sudah jadi:** situs baru di malangeducationcenter.com (beranda 12 bagian, 16 modul, tahapan, instruktur, fasilitas, industri, **halaman Alumni**, FAQ, kontak, blog), tombol WhatsApp yang menyebut asal situs, SEO dasar, dan **pengelola foto alumni** yang bisa diisi sendiri.
2. **Yang berubah/pindah:** situs lama (Hostinger) berhenti 15 Okt. **Email sudah pindah ke server baru**; kata sandi baru dibagikan terpisah. **Surat lama di Hostinger yang belum dipindah hilang setelah 15 Okt.**
3. **Cakupan:** proposal yang ditandatangani adalah Paket Ringkas (satu halaman), tetapi yang ditayangkan lebih luas (multi-halaman, blog, halaman Alumni + pengelola foto). Sampaikan eksplisit dan sepakati tertulis apakah itu bonus atau tambahan (harga/jangka garansi).
4. **Risiko hosting:** situs dan email masih di akun gratis percobaan Rumahweb. **Saran: pindah ke paket berbayar** (biaya ± seperti paket portal, sekitar Rp110.000/bulan; konfirmasi Rumahweb). Tanpa itu, situs/email bisa berhenti kapan saja tanpa cadangan harian.
5. **Biaya berjalan:** perpanjangan domain (±Rp211.000/tahun; naik per 15 Okt 2026), hosting (portal Rp110.000/bulan, plus hosting situs bila dipindah), email ikut hosting, analitik berbayar bila dipilih. Pemeliharaan opsional: Rp500.000/bulan (proposal) atau Rp900.000 per hari kerja untuk perubahan di luar lingkup.
6. **Garansi:** perbaikan kesalahan fungsi gratis 14 hari sejak tayang (proposal); tidak mencakup perubahan konten/desain atau gangguan layanan pihak ketiga.
7. **Yang masih menunggu MEC:** foto asli resolusi tinggi dan logo vektor; deskripsi 12 modul; persyaratan/biaya/jadwal/jam operasional yang resmi; ejaan nama instruktur; tautan sosial resmi; izin alumni dan testimoni (`docs/KEBUTUHAN-DARI-KLIEN.md`, `docs/DRAFT-KONTEN-UNTUK-MEC.md`).
8. **SEO realistis:** tampil di Google butuh minggu sampai bulan; tidak ada jaminan peringkat. Yang membantu: Search Console dan Google Business Profile (dibuat MEC), artikel rutin, foto asli, ulasan. Panduan `docs/SEARCH-CONSOLE.md`, `docs/RENCANA-KONTEN-SEO.md`.
9. **Keamanan:** sandi di pengelola sandi, jangan dibagikan lewat grup, aktifkan 2FA (Rumahweb, Google, GitHub), ganti sandi saat ada staf keluar.
10. **Siapa yang mengubah apa:** lihat §4.

## 4. Siapa mengubah apa (setelah serah terima)
| Perubahan | Siapa | Cara |
|---|---|---|
| Foto galeri Alumni | **admin MEC sendiri** | `/kelola-foto/` (`docs/ALUMNI-ADMIN.md`) |
| Email: tambah/hapus akun, ganti sandi | admin MEC | cPanel > Email Accounts |
| Teks, foto situs, modul, instruktur, artikel | **pengembang** (atau penerus teknis) | ubah file di repositori, `npm run deploy` (butuh Node 22 dan `lftp`; langkah di `docs/CICD.md`) |
| Perpanjangan domain/hosting | pemilik akun | Rumahweb client zone |
| Perbaikan darurat/rollback | pengembang | `docs/RUNBOOK-ROLLBACK.md`, `docs/CICD.md` |
Catatan: situs statis, jadi **tidak ada panel pengelola konten** selain pengelola foto alumni. Bila MEC ingin staf menulis artikel sendiri, tawarkan CMS (add-on di proposal: editor artikel Rp3.500.000).

## 5. Hal teknis yang harus diketahui penerus
- Cabang: `main` (live) = `staging`; `dev` versi satu halaman (arsip).
- Deploy lokal saja (GitHub Actions tidak bisa menjangkau Rumahweb): `npm run deploy` dengan `.env.deploy` (tidak masuk git); hostname FTP `gede.iixcp.rumahweb.net`; maksimal 2 koneksi paralel; `.htaccess` berisi blok handler PHP 8.3 dari cPanel yang **tidak boleh dihapus**.
- `public/kelola-foto/` butuh PHP 8.1+ dan GD; foto ada di `public_html/alumni-foto/` (di luar build, **jangan dihapus saat deploy**; cadangkan berkala).
- Kait yang tinggal diisi (`src/lib/site.ts`): verifikasi Search Console/Bing, analitik, koordinat, jam buka, tautan sosial.
- Indeks dokumentasi: `docs/` (PLAN, TODO, CICD, MIGRASI, RUNBOOK, ALUMNI-ADMIN, AUDIT-SEO, TODO-LOKAL-SEO, REVIEW-HEADERS, PANDUAN-EMAIL-STAF, TIKET-RUMAHWEB, SEARCH-CONSOLE, KEBUTUHAN-DARI-KLIEN, DRAFT-KONTEN-UNTUK-MEC, RENCANA-KONTEN-SEO).

## 6. Paket dokumen yang diserahkan
1. Berkas ini (ringkasan serah terima) dan `docs/KEBUTUHAN-DARI-KLIEN.md`.
2. Lembar kredensial (di pengelola sandi, **bukan** berkas teks).
3. `docs/PANDUAN-EMAIL-STAF.md` dan `docs/ALUMNI-ADMIN.md` (untuk staf/admin).
4. `docs/RUNBOOK-ROLLBACK.md`, `docs/CICD.md`, `docs/MIGRASI-HOSTINGER-KE-RUMAHWEB.md` (untuk penerus teknis).
5. Laporan: `docs/AUDIT-SEO-2026-10-13.md`, `reports/lighthouse-summary.md`, `reports/site-audit.md`, `docs/Laporan-Audit-MEC-Academy.pdf`.
6. Proposal yang ditandatangani (PDF, di luar repo) dan bukti pembayaran/pelunasan.
7. Arsip: kode sumber (transfer repo atau zip), `dist.zip` terakhir, cadangan `alumni-foto/`, arsip situs lama (lokasi, bukan isinya).
