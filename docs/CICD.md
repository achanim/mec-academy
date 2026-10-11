# Deploy ke Rumahweb

**Keputusan:** deploy dilakukan dari mesin lokal dengan `npm run deploy` (FTPS). Deploy dari GitHub Actions tidak mungkin di hosting ini:

| Jalur | Hasil |
|---|---|
| FTPS dari GitHub | Login berhasil, tetapi *"Timeout when trying to open data connection"* (port data pasif diblokir firewall untuk IP GitHub) |
| SSH/rsync | Port 22 ditolak (*Connection refused*), 2222/7822 timeout |
| cPanel API Token | Menu *Manage API Tokens* tidak tersedia (juga di akun non-trial) |

## Deploy rutin
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

## Setup sekali saja
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
- `public/.htaccess` ikut ter-deploy; error di dalamnya bisa membuat seluruh situs 500, jadi perhatikan uji asap dan rollback segera bila merah.

## Jalur cadangan (manual)
Actions > *Build artefak (deploy manual)* > *Run workflow* menghasilkan artefak `dist-zip` (30 hari). Unduh, unggah ke `public_html` lewat File Manager, lalu ekstrak. Atau pakai `dist/` hasil `npm run build` lokal.

## CI
`ci.yml` tetap menjalankan check, test, build, dan audit pada push/PR. `deploy.yml` kini hanya manual dan tidak men-deploy.

## Rollback
1. **Cepat:** `git revert <commit>`, lalu `npm run deploy`.
2. **Manual:** artefak `dist-zip` dari run lama atau `dist/` lokal, unggah lewat File Manager dan ekstrak.
3. **Bila akun hilang:** `docs/RUNBOOK-ROLLBACK.md`.
