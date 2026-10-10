# CI/CD: auto-deploy `staging` → Rumahweb

Alur: **push ke `staging`** → GitHub Actions menjalankan `astro check`, tes, dan build → mengunggah `dist/` lewat **FTPS** ke `public_html/` akun Rumahweb → uji asap pada situs hidup (beranda 200 dan redirect lama 301).
Workflow: `.github/workflows/deploy.yml` (tombol manual juga ada: Actions > *Deploy (staging → Rumahweb)* > Run workflow).
Branch lain (`dev`, `main`, PR) hanya menjalankan CI (`ci.yml`), tidak deploy.

## Setup sekali (±10 menit, hanya pemilik repo)
1. **Buat akun FTP khusus** di cPanel trial (*FTP Accounts*), **bukan** kata sandi cPanel utama:
   - Username mis. `deploy@malangeducationcenter.com`, kata sandi acak kuat.
   - **Directory: `public_html`** (agar akun ini hanya bisa menyentuh folder situs, tidak `arsip/`, email, atau berkas lain).
   - Buka *Configure FTP Client* di baris akun itu: catat **hostname server FTP** (pakai hostname, bukan IP, supaya sertifikat FTPS cocok).
2. Di GitHub: **Settings > Secrets and variables > Actions > New repository secret**, tambahkan:
   - `FTP_SERVER` = hostname FTP dari langkah 1
   - `FTP_USERNAME` = nama akun FTP
   - `FTP_PASSWORD` = kata sandinya
3. (Opsional, disarankan) **Settings > Environments > `production` > Required reviewers**: deploy menunggu persetujuanmu. Tanpa ini, setiap push ke `staging` langsung tayang.
4. Uji: Actions > *Deploy (staging → Rumahweb)* > *Run workflow* (branch `staging`). Hasil yang benar: ketiga job hijau, langkah "Uji asap" lolos.

Jika unggahan gagal di tahap koneksi/sertifikat: cek hostname FTP; bila Rumahweb memakai sertifikat yang tidak cocok, tambahkan `security: loose` pada langkah FTP (kurang aman; lebih baik perbaiki hostname).

## Perilaku yang perlu diketahui
- Aksi FTP menyimpan `.ftp-deploy-sync-state.json` di `public_html/` dan hanya mengunggah berkas yang berubah. `.htaccess` memblokir akses publik ke berkas itu. **Jangan menghapusnya** dari server (kalau hilang, unggahan berikutnya mengirim ulang semua; tidak merusak).
- Berkas yang **dihapus dari repo/build** ikut dihapus dari `public_html/` (hanya yang tercatat di berkas status). Berkas lain di `public_html/` yang bukan dari build tidak disentuh.
- Konkurensi: satu deploy dalam satu waktu (antrian, tidak saling memotong).
- Artefak `dist` setiap build disimpan 14 hari di tab Actions (bisa diunduh untuk unggah manual).
- Pekerjaan `quality` di `ci.yml` (Playwright + Lighthouse) belum pernah berjalan di GitHub; bila gagal di tahap Chrome, itu tidak menghentikan deploy karena workflow deploy terpisah.

## Rollback
- **Cepat:** `git revert <commit>` lalu push ke `staging` → build lama otomatis tayang lagi.
- **Manual:** unduh artefak `dist` dari run lama (tab Actions) dan unggah lewat File Manager/FTP.
- **Darurat:** salinan lokal `dist/` dan arsip situs lama ada di laptop; unggah manual ke `public_html/`.

## Keamanan
- Kata sandi FTP hanya ada di GitHub Secrets (tidak muncul di log). Ganti bila pernah bocor.
- Akun FTP dibatasi ke `public_html`. Jika akun trial berhenti/pindah paket, **hostname dan akun FTP harus diperbarui**, lalu secret diganti.
- Repo ini hanya berisi kode situs: tidak ada email, arsip, `.env`, atau kredensial.
