# Halaman Alumni dan pengelola foto (khusus admin MEC)

## Dua halaman
| Halaman | Alamat | Keterangan |
|---|---|---|
| **Alumni** (publik) | `/alumni/` | Teks, ±600 alumni / BMC 55, galeri, kegiatan bersama perusahaan. Ada di menu dan sitemap. |
| **Kelola foto** (tersembunyi) | `/kelola-foto/` | Hanya untuk admin MEC: unggah, beri keterangan, urutkan, hapus foto. **Tidak ditautkan di situs mana pun, tidak masuk sitemap, `noindex`**, dan dilindungi kata sandi. |

Galeri `/alumni/` membaca `/alumni-foto/manifest.json`. Bila belum ada foto yang diunggah (atau JavaScript mati), halaman menampilkan 2 foto bawaan.

## Cara kerja (singkat)
- Pengelola adalah satu berkas PHP (`public/kelola-foto/index.php`) yang ikut ter-deploy bersama situs.
- Foto tersimpan di `public_html/alumni-foto/` (`img/` besar, `thumb/` kecil, `manifest.json`). Folder ini **tidak ada di repo/build**, jadi **tidak tertimpa atau terhapus saat deploy** (`npm run deploy` memakai `mirror` tanpa `--delete`).
- Kata sandi disimpan sebagai **hash** di `public_html/kelola-foto/config.php` (dibuat di server, tidak ada di repo).
- Server harus: **PHP 8.1+**, ekstensi **GD** (semua paket cPanel Rumahweb umumnya sudah). Ekstensi `exif` opsional (memutar foto sesuai orientasi kamera).

## Penyiapan pertama (sekali, ±3 menit; pemilik/pengembang)
1. Deploy situs seperti biasa (`npm run deploy` atau unggah `dist/`), sehingga `public_html/kelola-foto/index.php` ada.
2. Di cPanel > **File Manager** > `public_html/kelola-foto/` buat **berkas kosong bernama `BUAT-SANDI.txt`**.
3. Buka `https://malangeducationcenter.com/kelola-foto/` > isi kata sandi (minimal 12 karakter) dua kali > Simpan. Berkas `BUAT-SANDI.txt` terhapus otomatis dan `config.php` terbentuk.
4. Masuk dengan kata sandi itu. Simpan di pengelola sandi dan bagikan hanya ke admin yang berwenang.
5. Disarankan: ganti nama folder `kelola-foto` lewat File Manager menjadi nama yang tidak mudah ditebak (mis. `foto-mec-7x2k`), lalu pakai alamat barunya. Aplikasi tetap berfungsi karena tidak menyimpan namanya. Catatan: deploy berikutnya akan membuat folder `kelola-foto` baru lagi dari repo (hanya berisi `index.php`; tanpa `config.php` ia hanya menampilkan "Belum disiapkan"); hapus saja bila tidak dipakai.

## Memakai (admin)
- **Tambah foto:** pilih satu atau banyak foto (JPG/PNG/WebP, ≤ 15 MB, maksimal 20 per unggahan) > Unggah. Foto otomatis diperkecil (sisi terpanjang 2000 px) dan dibuat thumbnail; metadata (lokasi GPS, dll.) dihapus.
- **Foto iPhone (HEIC):** ubah dulu ke JPG (Pengaturan > Kamera > Format > *Paling Kompatibel*).
- **Keterangan:** isi di kolom lalu *Simpan keterangan* (maks. 140 karakter; dipakai juga sebagai teks alternatif untuk pembaca layar).
- **Urutan:** tombol *Naik/Turun*. Urutan di sini sama dengan di halaman Alumni.
- **Hapus:** tombol *Hapus* (ada konfirmasi); berkas fisik ikut terhapus.
- Perubahan terlihat di `/alumni/` setelah halaman dimuat ulang. Maksimal 80 foto.
- Pastikan alumni yang tampil **sudah memberi izin**.

## Keamanan (ringkas)
- Kata sandi: `password_hash` (bcrypt/argon), sesi `HttpOnly` + `SameSite=Strict` + `Secure`, keluar otomatis setelah 2 jam tak aktif, **dikunci 15 menit setelah 5 kali salah**, token CSRF di setiap aksi.
- Unggahan: hanya JPG/PNG/WebP yang benar-benar gambar (diperiksa isi, bukan nama), batas ukuran dan resolusi, **dienkode ulang** (muatan tersembunyi hilang), nama berkas acak 16 heksadesimal; folder foto menolak eksekusi skrip.
- Keluaran di-escape; `noindex`, `no-store`, `X-Frame-Options: DENY`, CSP ketat pada halaman admin.
- Sandi tidak ada di repo; `config.php`, `data/`, dan `BUAT-SANDI.txt` ditolak oleh `.htaccess` dari akses web.
- Risiko tersisa: satu kata sandi bersama (tanpa akun per orang), dan keamanan bergantung pada server PHP dan kerahasiaan sandi. Ganti sandi bila ada admin yang berhenti (hapus `config.php`, buat `BUAT-SANDI.txt`, ulangi penyiapan).

## Cadangan dan pemulihan
- Foto ada hanya di server. **Unduh `public_html/alumni-foto/` berkala** (File Manager > Compress > unduh), terutama karena akun trial tidak punya cadangan harian (`docs/RUNBOOK-ROLLBACK.md`).
- Lupa sandi: hapus `config.php` lewat File Manager, buat `BUAT-SANDI.txt`, muat `/kelola-foto/`, buat sandi baru. Foto tidak terpengaruh.

## Pengujian yang sudah dilakukan (lokal, PHP 8.4 + GD)
Penyiapan dan penolakan sandi pendek; login salah/benar, pengunci 5 kali, CSRF; unggah JPG besar, PNG transparan, WebP; **penolakan** berkas PHP berkedok `.jpg`, GIF, `.php`, dan gambar terlalu kecil; keterangan berisi `<script>` ditampilkan sebagai teks; urutan, hapus, id berbahaya (`../`) ditolak; sesi tanpa login tidak berefek. Galeri `/alumni/` memuat foto dari manifest dan lightbox bekerja (desktop dan 390 px, tanpa scroll horizontal). **Belum diuji di server Rumahweb** (versi PHP, batas `upload_max_filesize`/`post_max_size`, `.htaccess`).
