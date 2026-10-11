# Tinjauan `.htaccess` dan header keamanan (usulan; belum diterapkan, tidak di-deploy)

Kondisi sekarang (`public/.htaccess`; `_headers` hanya untuk Cloudflare/Netlify dan diabaikan di cPanel):
HTTPS + www→apex, redirect alamat lama, 404/500, gzip, cache (HTML selalu divalidasi, `_astro/` 1 tahun immutable), `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, HSTS `max-age=31536000; includeSubDomains`.

## 1. HSTS
- `includeSubDomains` **boleh dipertahankan** selama semua subdomain yang dipakai bersertifikat valid (`mail.`, `webmail.` sudah valid). Konsekuensi: subdomain yang kelak tidak punya HTTPS (mis. `belajar.` jika dihidupkan lagi) tidak bisa dibuka di browser yang pernah mengunjungi situs utama selama setahun.
- **Jangan menambah `preload`** (permanen dan sulit dibatalkan).
- Bila ingin lebih longgar saat masih berpindah-pindah server: turunkan ke `max-age=86400` selama minggu-minggu pertama, naikkan lagi setelah stabil.

## 2. Content-Security-Policy (CSP): usul, mulai dari *Report-Only*
Inventaris dari build: 4 `<script>` inline dan 2 skrip eksternal (milik situs sendiri), sekitar 100 atribut `style=""` dan 1 `<style>`, font dan gambar dari domain sendiri, video YouTube lewat iframe `youtube-nocookie.com`, tautan keluar `wa.me` (hanya tautan, bukan sumber).
Karena ada inline script/style, kebijakan ketat bergantung `'unsafe-inline'` (atau hash per skrip).

Usulan (tambahkan **Report-Only** dulu, amati konsol browser 1–2 minggu, baru ganti ke `Content-Security-Policy`):
```apache
Header set Content-Security-Policy-Report-Only "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; frame-src https://www.youtube-nocookie.com; connect-src 'self'; media-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
```
Catatan: `frame-ancestors 'none'` menggantikan `X-Frame-Options` (boleh keduanya). Bila nanti memakai analitik/Google Tag, tambahkan hostnya. Uji dialog, galeri/lightbox, dan video setelah CSP aktif.

## 3. Header lain (aman ditambahkan)
```apache
Header always set X-Frame-Options "DENY"
Header always set Cross-Origin-Opener-Policy "same-origin"
```
`Permissions-Policy` sudah menutup kamera, mikrofon, geolokasi. Hindari `Cross-Origin-Embedder-Policy` (merusak iframe YouTube).

## 4. Hal lain di `.htaccess`
- Blok `.ftp-deploy-sync-state.json` sudah dihapus (FTP-Deploy-Action tidak dipakai lagi). **Blok handler PHP dari cPanel harus dipertahankan.**
- Tambahkan penolakan berkas tersembunyi/sensitif (jaring pengaman bila ada yang terunggah tak sengaja):
```apache
<FilesMatch "^\.(?!well-known)|\.(env|log|sql|bak|zip)$">
  Require all denied
</FilesMatch>
```
  **Hati-hati:** pola ini juga menolak `.htaccess` itu sendiri dari web (memang seharusnya) dan `.zip` (artefak unggahan CI/CD `_deploy-dist.zip` dihapus setelah ekstraksi). Uji di staging sebelum produksi, karena sintaks salah bisa membuat seluruh situs 500.
- `/program/` mengembalikan 403 karena folder tanpa `index.html`; tidak ada tautan ke sana. Opsional: redirect `/program/` → `/program/basic-mechanic-course/`.
- Kompresi: tambahkan `application/xml` dan `text/plain` bila perlu; gambar sudah terkompresi.
- Hindari `Options -MultiViews` bila server mengabaikannya; sudah dipakai dan situs berjalan baik.

## 5. Yang sebaiknya tidak dilakukan sekarang
Tidak ada perubahan header di server hidup sebelum diuji di salinan; CSP ketat tanpa masa *Report-Only* berisiko memutus video/galeri.
