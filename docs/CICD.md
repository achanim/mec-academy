# Deploy ke Rumahweb

**Keputusan (15 Okt 2026):** deploy dilakukan **manual lewat cPanel File Manager** (langkah lengkap: `docs/PANDUAN-UPDATE-KODE-DAN-DEPLOY.md` bagian 4). `npm run deploy` (FTPS/lftp) macet lebih dari 25 menit di praktik dan **tidak dipakai lagi**; skripnya disimpan hanya sebagai referensi. Deploy dari GitHub Actions juga tidak mungkin di hosting ini (workflow-nya sudah dihapus):

| Jalur | Hasil |
|---|---|
| FTPS dari GitHub | Login berhasil, tetapi *"Timeout when trying to open data connection"* (port data pasif diblokir firewall untuk IP GitHub) |
| SSH/rsync | Port 22 ditolak (*Connection refused*), 2222/7822 timeout |
| cPanel API Token | Menu *Manage API Tokens* tidak tersedia (juga di akun non-trial) |

## Deploy rutin (manual, cPanel File Manager)
1. `git checkout main && git pull && npm run build`.
2. Zip seluruh `dist/` menjadi satu berkas (batas unggah saat ini 512 MB), unggah dan ekstrak ke `public_html` (rincian dan perintah zip di panduan bagian 4).
3. Pastikan `.htaccess` masih memuat blok PHP 8.3, lalu uji asap (beranda, `/faq/`, `/alumni/`, `/kelola-foto/`).

## Jalur lama: `npm run deploy` (tidak dipakai, referensi)
```bash
git checkout main && git pull
npm run deploy
```
Skrip (`scripts/deploy.sh`):
1. `npm run check` dan `npm test` (lewati dengan `SKIP_CHECKS=1`);
2. `npm run build` (termasuk indeks Pagefind) dan memastikan `dist/index.html` + `dist/.htaccess` ada;
3. mengunggah `dist/` ke `public_html` lewat FTPS (`lftp mirror`, hanya berkas yang lebih baru, 2 koneksi paralel; server membatasi koneksi per IP);
4. uji asap: beranda 200 dan memuat "MEC Academy", lalu status `/faq/` dan `/organisasi/` ditampilkan.

Coba tanpa mengunggah: `DRY_RUN=1 npm run deploy`.

Nilai di `.env.deploy` dibaca sebagai teks, jadi sandi boleh berisi `;`, `#`, `$`. Variabel lingkungan yang diberikan di command line diutamakan.

## Setup jalur lama (tidak dipakai)
1. `brew install lftp`
2. Buat `.env.deploy` di akar repo (sudah diabaikan git lewat `.env*`; jangan di-commit):
   ```
   FTP_HOST=gede.iixcp.rumahweb.net   # hostname server; sertifikat TLS-nya valid. ftp.<domain> TIDAK cocok dengan sertifikat
   FTP_USER=<akun FTP deploy, mis. deploy@malangeducationcenter.com>
   FTP_PASS=<sandi akun tersebut>
   ```
   Opsional: `FTP_DIR` (bawaan `./`, karena akun dibatasi ke `public_html`), `SITE_URL`.
3. Pastikan akun FTP tersebut tetap ada di cPanel (jangan dihapus).

## Perilaku
- Tanpa `--delete`: berkas yang dihapus dari build **tidak** ikut terhapus di server (bersihkan manual bila perlu); berkas non-situs di `public_html` aman.
- Koneksi memaksa TLS (`ftp:ssl-force`). Sertifikat server hanya valid untuk hostname server (`gede.iixcp.rumahweb.net`), bukan `ftp.<domain>`.
- Jalankan dari jaringan yang tidak memblokir port FTP dan data pasif. Bila diblokir (kantor, tethering), pakai jalur cadangan.
- `public/.htaccess` memuat blok handler PHP 8.3 (`# php -- BEGIN cPanel-generated handler`, dari MultiPHP Manager) yang dibutuhkan `/kelola-foto/`. Jangan dihapus: deploy menimpa `.htaccess` server, dan tanpa blok itu domain kembali ke PHP 7.4 (default server) sehingga `/kelola-foto/` memberi 500.
- `public/.htaccess` ikut ter-deploy; error di dalamnya bisa membuat seluruh situs 500, jadi perhatikan uji asap dan rollback segera bila merah.

## Temuan server (11 Okt 2026, dari pemasangan nyata)
1. **PHP bawaan domain 7.4** (diwarisi dari server), sehingga `/kelola-foto/` awalnya memberi 500. Diganti ke **PHP 8.3 (`ea-php83`)** lewat cPanel > *MultiPHP Manager*.
2. cPanel menulis blok `# php -- BEGIN cPanel-generated handler` ke `public_html/.htaccess`. Karena deploy **menimpa** `.htaccess`, blok itu **disalin ke `public/.htaccess` di repo**. **Jangan dihapus**; tanpa blok itu PHP kembali ke 7.4 dan `/kelola-foto/` 500 lagi. Bila versi PHP diganti di MultiPHP Manager, salin blok baru dari `public_html/.htaccess` server ke repo.
3. **Server membatasi 8 koneksi FTP per IP** (`421 Too many connections`). Sesi macet bisa menahan koneksi beberapa menit, jadi skrip memakai maksimal **2 koneksi paralel**.
4. **Hostname FTP harus `gede.iixcp.rumahweb.net`**; sertifikat TLS tidak cocok untuk `ftp.<domain>`.
5. **Batas unggah File Manager** dulu ±10 MB (build dipecah 3 zip), kini 512 MB sehingga cukup **satu zip** yang diekstrak ke `public_html`.
6. Berkas status `FTP-Deploy-Action` (`.ftp-deploy-sync-state.json`) tidak lagi dipakai; blok penolaknya sudah dihapus dari `.htaccess`. Bila berkas itu masih ada di server, hapus lewat File Manager.

## CI dan GitHub Actions
Dicabut pada 18 Okt 2026: folder `.github/workflows/` (`ci.yml` dan `deploy.yml`) dihapus dari `main` dan `staging`. Tidak ada pipeline otomatis; pemeriksaan dilakukan lokal sebelum deploy (`npm run check`, `npm test`, `npm run build`, opsional `npm run audit`).

## Rollback
1. **Cepat:** `git revert <commit>`, `npm run build`, lalu unggah `dist/` lewat File Manager (zip dipecah).
2. **Manual:** `git checkout <commit-lama>`, `npm run build`, lalu unggah `dist/` lewat File Manager dan ekstrak.
3. **Bila akun hilang:** `docs/RUNBOOK-ROLLBACK.md`.
