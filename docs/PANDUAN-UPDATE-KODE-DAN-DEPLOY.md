# Panduan: mengubah kode situs sampai tayang (manual)

Untuk pengelola situs MEC Academy. Tanpa kredensial di dokumen ini: sandi diberikan terpisah (pengelola sandi).
Alur singkat: **ambil kode → ubah → lihat di komputer → periksa → simpan (commit) → unggah (deploy) → cek situs**.

> Perubahan **teks artikel/foto alumni** tidak perlu cara ini: foto alumni lewat `/kelola-foto/` (lihat `docs/ALUMNI-ADMIN.md`).

## 0. Persiapan sekali saja
1. Pasang **Node.js 22 LTS** (nodejs.org) dan **Git**. Mac: `brew install lftp`. Windows: pakai **WSL (Ubuntu)** lalu `sudo apt install lftp` (skrip deploy memakai `lftp`).
2. Ambil kode: `git clone <alamat-repositori> mec-academy` lalu `cd mec-academy` dan `npm install`.
3. Buat berkas **`.env.deploy`** di folder utama (tidak ikut git, jangan dibagikan):
   ```
   FTP_HOST=gede.iixcp.rumahweb.net
   FTP_USER=<akun FTP deploy>
   FTP_PASS=<sandi akun FTP>
   ```
   Akun FTP dibuat di cPanel Rumahweb (Akun FTP, dibatasi ke `public_html`). Detail: `docs/CICD.md`.

## 1. Setiap kali mengubah
1. Ambil versi terbaru: `git pull`
2. Buat cabang kerja (disarankan): `git checkout -b perubahan-nama-singkat`
3. Jalankan situs lokal: `npm run dev` lalu buka **http://localhost:4321**. Setiap simpan berkas langsung terlihat.

### Di mana mengubah apa
| Yang ingin diubah | Berkas |
|---|---|
| Nomor WA, email, alamat, jam buka, medsos, deskripsi situs | `src/lib/site.ts` |
| Isi beranda (12 bab) | `src/pages/index.astro` |
| Halaman lain (Tentang, Kontak, Fasilitas, dst.) | `src/pages/…` |
| Artikel blog | `src/content/articles/*.mdx` (salin artikel lama sebagai contoh; isi `title`, `description`, `publishedAt`, `category`, `cover`) |
| Gambar | `src/assets/images/` (JPG/PNG, idealnya < 500 KB) |
| Warna, jarak, tampilan | `src/styles/global.css` |
| Aturan alamat lama/redirect, cache | `public/.htaccess` (**jangan hapus blok PHP handler cPanel**) |

Tips: ubah **satu hal per kali**, lihat hasilnya di localhost, baru lanjut.

## 2. Periksa sebelum tayang
```
npm run check     # cek kesalahan penulisan/tipe
npm test          # uji otomatis (harus 10 lulus)
npm run build     # buat folder dist/ (harus tanpa error)
npm run preview   # lihat hasil build di http://localhost:4321
```
Kalau ada yang merah, **jangan deploy**. Baca pesan error (biasanya menyebut berkas dan baris), perbaiki, ulangi. Opsional: `npm run audit` (kontras warna dan Lighthouse).

## 3. Simpan perubahan (commit)
```
git add -A
git commit -m "Ubah nomor WA dan jam buka"
git push -u origin perubahan-nama-singkat
```
Lalu gabungkan ke cabang utama (`main`) lewat Pull Request di GitHub, atau `git checkout main && git merge perubahan-nama-singkat && git push`.
Yang di-deploy adalah **isi komputer Anda**, jadi pastikan sedang di cabang `main` yang sudah mutakhir sebelum langkah 4: `git checkout main && git pull`.

## 4. Deploy (unggah ke Rumahweb)
```
npm run deploy
```
Skrip otomatis: cek, uji, build, lalu unggah `dist/` lewat FTPS. Latihan tanpa mengunggah: `DRY_RUN=1 npm run deploy`.
Catatan: berkas yang **dihapus** dari kode tidak otomatis hilang di server (sengaja, agar folder `alumni-foto/` aman). Untuk menghapus halaman lama, hapus lewat cPanel File Manager.

## 5. Cek hasilnya
1. Buka https://malangeducationcenter.com dan segarkan keras (Ctrl+Shift+R / Cmd+Shift+R).
2. Cek halaman yang diubah, tombol WhatsApp, dan satu halaman lain (HP dan laptop).
3. Jika perubahan belum tampak: tunggu 1-2 menit (cache), coba jendela penyamaran.
4. Daftar uji lengkap: `docs/TODO-LOKAL-SEO.md` bagian A.

## 6. Kalau ada masalah
| Gejala | Tindakan |
|---|---|
| `lftp: command not found` | pasang lftp (langkah 0) |
| Login FTP gagal | cek `.env.deploy` (host, user, sandi); sandi bisa diganti di cPanel |
| Situs error / halaman putih setelah deploy | kembalikan ke versi sebelumnya: `git checkout <commit-lama>` lalu `npm run deploy` (lihat `docs/RUNBOOK-ROLLBACK.md`) |
| `/kelola-foto/` error 500 | pastikan PHP **8.3** di cPanel (MultiPHP Manager) |
| Ragu / buntu | berhenti, jangan deploy; hubungi pengembang |

## 7. Aturan aman
- Jangan commit `.env.deploy`, sandi, atau data pribadi ke GitHub.
- Selalu `npm run build` sukses sebelum deploy; satu perubahan, satu deploy.
- Simpan cadangan: folder `alumni-foto/` dan salinan `dist/` terakhir.
- Aktifkan 2FA di Rumahweb, GitHub, Google; ganti sandi bila ada staf keluar.
