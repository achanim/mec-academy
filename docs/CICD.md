# CI/CD: deploy `staging` → Rumahweb

**Status:** FTPS dari GitHub Actions **gagal** (login berhasil, tetapi *"Timeout when trying to open data connection"*: port data pasif diblokir firewall Rumahweb; SFTP/SSH 22/2222 tertutup). Rancangan baru memakai **cPanel API lewat HTTPS (port 2083)**. Belum diuji di server Rumahweb: anggap **eksperimental** sampai satu run berhasil.

## Cara kerja (`.github/workflows/deploy.yml`)
Push ke `staging` → `build` (astro check, tes, build, buat `dist.zip`, simpan sebagai artefak `dist-zip` 30 hari) → `deploy` (bila secret lengkap):
1. cek koneksi + token (`Fileman/list_files`), gagal cepat bila port 2083 tertutup atau token salah;
2. unggah `dist.zip` ke `public_html/_deploy-dist.zip` (`Fileman/upload_files`);
3. ekstrak di server (API2 `Fileman::fileop op=extract`) dan hapus zip (`op=unlink`);
4. uji asap: beranda 200 dan memuat "MEC Academy", `/organisasi/` 301, zip sisa 404.

**Tanpa secret**, job `deploy` hanya mencatat pesan di ringkasan run dan berakhir hijau. Artefak `dist-zip` tetap tersedia = **jalur manual yang sudah terbukti** (unduh, unggah lewat File Manager, ekstrak ke `public_html`).

## Setup (pemilik; ±10 menit)
1. cPanel > **Security > Manage API Tokens > Create**: nama `github-deploy`, **isi tanggal kedaluwarsa** (mis. 90 hari). **Token tampil sekali**: salin langsung.
2. GitHub > Settings > Secrets and variables > Actions, tambahkan:
   - `CPANEL_HOST`: hostname cPanel server trial (tanpa `https://` dan tanpa port; sama seperti di URL cPanel)
   - `CPANEL_USER`: username cPanel akun trial
   - `CPANEL_TOKEN`: token dari langkah 1
3. (Disarankan) Settings > Environments > `production` > **Required reviewers**: tiap deploy menunggu persetujuan.
4. Jalankan: push kecil ke `staging`, atau (setelah `deploy.yml` ada di `main`) Actions > *Run workflow*.

> **Trade-off keamanan:** token cPanel mewarisi hak penuh akun (berkas, email, database), lebih luas daripada akun FTP terbatas. Karena itu: kedaluwarsa wajib, simpan hanya di GitHub Secrets, aktifkan reviewer pada environment `production`, cabut dari *Manage API Tokens* bila ragu. Jika trial berpindah paket/server, ganti `CPANEL_HOST`/`CPANEL_USER` dan buat token baru.

## Tombol "Run workflow" tidak muncul
`workflow_dispatch` hanya tampil bila berkas workflow ada di **branch default** (sekarang `main`, hanya "Initial commit"). Pilihan (keputusan pemilik): (a) gabungkan `staging` ke `main` lewat PR, atau (b) biarkan; deploy tetap otomatis lewat push ke `staging`, dan run ulang bisa lewat Actions > run lama > *Re-run all jobs*.

## Jika langkah cPanel API gagal
Setiap kegagalan menyebut langkahnya di log. Penyebab yang mungkin: port 2083 diblokir dari IP GitHub; `dir` upload menolak jalur absolut (ganti `dir` menjadi `public_html`); API2 `fileop` dinonaktifkan di server. **Fallback:** artefak `dist-zip` + unggah manual. Alternatif berikutnya bila diperlukan: cPanel *Git Version Control* (cabang `deploy` berisi hasil build, ditarik cPanel).

## Perilaku
- Ekstraksi **menimpa** berkas; berkas yang dihapus dari build **tidak** ikut terhapus di server (bersihkan manual bila perlu). `public_html` tidak dikosongkan, jadi berkas non-situs aman.
- Satu deploy dalam satu waktu (`concurrency`), tanpa pemotongan.
- `public/.htaccess` ikut ter-deploy; error di dalamnya bisa membuat seluruh situs 500, jadi tonton run pertama dan rollback segera bila uji asap merah.

## Rollback
1. **Cepat:** `git revert <commit>` lalu push ke `staging` → build lama tayang lagi (otomatis bila CI/CD aktif).
2. **Manual:** unduh artefak `dist-zip` dari run lama (tab Actions, 30 hari) atau pakai `dist/` lokal; unggah ke `public_html` lewat File Manager, ekstrak.
3. **Bila trial/akun hilang:** `docs/RUNBOOK-ROLLBACK.md`.
