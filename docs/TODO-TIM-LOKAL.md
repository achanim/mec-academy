# TODO tim lokal (Claude in Chrome): cek dan eksekusi migrasi Hostinger → Rumahweb

Konteks lengkap: `docs/MIGRASI-HOSTINGER-KE-RUMAHWEB.md` (inventaris, aturan DNS, jadwal, verifikasi). Dokumen ini hanya daftar kerja untuk sesi lokal yang bisa membuka hPanel Hostinger dan client zone/cPanel Rumahweb lewat browser.
Batas: Hostinger berakhir **15 Okt**, pakai **Selasa 14 Okt** sebagai batas aman, target selesai **13 Okt**.

## Aturan main (baca dulu)
1. **Baca-saja dulu.** Bagian A dan B hanya melihat/mencatat. Perubahan apa pun (bagian C) **menunggu persetujuan eksplisit dari pemilik proyek, satu per satu**.
2. **Jangan simpan rahasia di repo atau chat tim:** tanpa sandi, token, isi `.env`, nama kotak surat staf, atau dump database. Laporan boleh berisi jumlah, ukuran, status, dan nama teknis publik.
3. **Jangan buka `.env` maupun isi dump database.** Arsip cukup diunduh dan diperiksa ukurannya.
4. **Dilarang tanpa persetujuan:** menghapus, membatalkan, terminate, mengubah nameserver, mengubah record DNS, membuat/menghapus akun email, membayar, atau menekan tombol "Register"/"Order"/"Upgrade". Halaman pembayaran: berhenti dan serahkan ke pemilik.
5. Berhenti dan tanya bila ada CAPTCHA, 2FA, atau pesan peringatan yang tidak dikenal.
6. Setiap temuan dicatat sebagai: *apa yang dilihat → di menu mana → status (OK / perlu keputusan / blokir)*.

## A. Cek Rumahweb (baca-saja)
Client zone `new.clientzone.rumahweb.com` dan cPanel hosting.
- [ ] **A1. Trial** (`Unlimited M (Trial)`, domain `.com`): buka Info/detail layanan; catat masa aktif, batas resource, apakah boleh dipakai produksi, dan syarat pindah ke berbayar.
- [ ] **A2. Upgrade trial:** Actions → Upgrade Services (hanya lihat, jangan lanjut): catat paket dan **harga** (bulanan vs tahunan).
- [ ] **A3. `Unlimited M` berbayar** (portal `.my.id`): di cPanel catat **kuota Addon Domains** (terpakai/batas), kuota disk, pilihan versi PHP, dan apakah akun punya akses SSH/Git.
- [ ] **A4. Apakah `.com` bisa dipasang sebagai addon domain** di `Unlimited M` selagi masih terdaftar di akun trial? Cukup cari jawabannya di dokumentasi/halaman bantuan Rumahweb atau lihat apakah form Addon Domains menolak; **jangan membuat addon**. Jika perlu tiket, catat saja.
- [ ] **A5. Nameserver Setting** domain `malangeducationcenter.com` (client zone → Domain → Nameserver Setting): catat NS aktif sekarang dan NS Rumahweb yang tersedia untuk hosting (harapannya `ns1/ns2.rumahweb.com`, `ns3/ns4.rumahweb.net`).
- [ ] **A6. IP server** hosting (cPanel → General Information/Shared IP) untuk akun yang akan dipakai.
- [ ] **A7. Domain:** status auto-renew (sekarang OFF), tanggal habis (23 Agu 2028), dan **harga perpanjangan `.COM` setelah 15 Okt 2026**.
- [ ] **A8. Email di cPanel Rumahweb:** daftar akun email yang sudah ada, hostname server mail, port IMAP/SMTP yang direkomendasikan, kuota per kotak surat.
- [ ] **A9. Portal assessment:** konfirmasi jatuh tempo **19 Nov 2026** dan harga perpanjangan; catat apakah Auto Renew bisa diaktifkan (jangan diaktifkan sebelum diminta).

## B. Cek Hostinger (baca-saja)
hPanel paket Business (3 situs: utama, `admin.`, `belajar.`).
- [ ] **B1. Email:** jumlah kotak surat (9), ukuran masing-masing, plus **forwarder, alias, autoresponder, catch-all**. Laporkan jumlah dan ukuran, bukan alamat lengkapnya.
- [ ] **B2. DNS Zone:** pastikan daftar record lengkap (CNAME DKIM, www, autodiscover/autoconfig, ALIAS `@` dan `admin`, MX, TXT SPF, `_dmarc`); catat bila ada record lain (TXT verifikasi, CAA, subdomain lain).
- [ ] **B3. Situs utama (builder):** apakah ada **formulir** dengan kiriman tersimpan, integrasi analitik, Google Search Console/Business, domain terhubung lain.
- [ ] **B4. Penagihan:** tanggal berakhir persis (15 Okt), auto-renew nonaktif, dan apakah masa aktif bisa **diperpanjang 1 bulan** (jaring pengaman untuk email). Hanya dicatat; jangan membeli.
- [ ] **B5. Akses ke `belajar.`** (skrip komersial): catat versi PHP aktif dan pilihan PHP yang tersedia; jangan mengubah.

## C. Eksekusi (HANYA setelah persetujuan eksplisit per langkah)
Urutan dan alasannya ada di dokumen migrasi §4. Tiap langkah: minta persetujuan → kerjakan → bukti (screenshot/keluaran) → centang.

**C0. Arsip (sudah disetujui pemilik, lakukan lebih dulu, batas 13 Okt)**
- [ ] Unduh berkas + ekspor database **`admin.`** dan **`belajar.`** sebagai arsip terenkripsi, simpan **di luar repo** (Drive MEC/disk lokal terenkripsi). Periksa ukuran; **jangan buka `.env`**. Jangan dipindah dan jangan dimatikan sebelum diperintahkan.
- [ ] Jalankan `node scripts/backup-old-site.mjs` → `backup/hostinger-site/` (folder ini di `.gitignore`); salin ke Drive; periksa `LAPORAN.txt`.

**C1. Hosting (keputusan pemilik 11 Okt)**
- [x] Situs `.com` tetap di akun **trial**; **tanpa addon** di `Unlimited M`. Jangan menutup/menghapus trial.
- [ ] Buka tiket Rumahweb: apakah Free Account boleh dipakai produksi, kapan berakhir, apa konsekuensinya untuk email.

**C2. Situs**
- [x] Build branch **`staging`** terpasang di trial dan lolos uji via IP. Perbarui dengan `git pull` + build ulang karena `staging` kini memuat persyaratan peserta, unggah isi `dist/` ke `public_html/` domain `.com` (termasuk `.htaccess`, berkas tersembunyi).
- [ ] Uji lewat file `hosts` (IP server → domain) tanpa menyentuh DNS: semua dialog, tautan WhatsApp, redirect lama.

**C3. Email tahap 1 (persiapan)**
- [ ] Buat 9 kotak surat yang sama di cPanel Rumahweb (sandi sementara, diberikan lewat kanal aman, bukan repo).

**C4. DNS tahap 1 dan nameserver: SELESAI Sab 10 Okt ±16.00–16.20 WIB** (NS Rumahweb aktif di 1.1.1.1 dan 8.8.8.8; A `.com` → server trial; MX/SPF/DKIM masih Hostinger; AutoSSL terbit, berlaku s.d. 8 Jan 2027; redirect dan 410 lolos). Propagasi NS bisa sampai 48 jam: sebagian resolver masih bisa melihat situs lama di Hostinger. **Jangan biarkan Hostinger lapse sebelum 14 Okt.**
- [x] Zone Editor cPanel: `A @` → IP server, `www` CNAME → `@`, tanpa AAAA; salin MX, SPF, `_dmarc`, 3 CNAME DKIM, `autodiscover`, `autoconfig` persis seperti Hostinger (dokumen §3). `admin` tidak dibuat (rencana: dimatikan).
- [x] Cocokkan zona baru dengan hasil B2, baris per baris, **sebelum** mengganti NS.
- [x] Ganti nameserver (Nameserver Setting) ke NS Rumahweb; catat waktunya.
- [x] Segera **Run AutoSSL** (cPanel → SSL/TLS Status) sampai gembok hijau (situs lama mengirim HSTS).

**C5. Email tahap 2 (Senin 12 Okt)**
- [ ] Salin isi semua kotak surat via IMAP (sumber `imap.hostinger.com:993`) ke server mail Rumahweb. **Syarat lanjut:** jumlah pesan per folder sama di ke-9 kotak surat.
- [ ] Ubah MX ke server mail Rumahweb; SPF baru `v=spf1 +a +mx +ip4:<IP server> ~all`; aktifkan DKIM; hapus CNAME DKIM/autodiscover/autoconfig Hostinger.
- [ ] Uji kirim/terima dua arah (Gmail, Outlook); cek skor mail-tester; bantu staf mengatur ulang klien email.

**C6. Penutupan (Selasa 13 Okt)**
- [ ] Sinkron IMAP susulan; ekspor terakhir dari Hostinger (formulir, forwarder, analitik).
- [ ] Search Console: verifikasi ulang (TXT via zona Rumahweb), kirim `sitemap-index.xml`.
- [ ] `admin.` dimatikan hanya setelah arsip terkonfirmasi dan atas perintah pemilik.

## D. Verifikasi akhir ("tidak ada yang tersisa")
Perintah publik (tanpa login), semua harus bersih dari Hostinger:
```
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=NS"
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=MX"
curl -sI https://malangeducationcenter.com/ | grep -i "hcdn\|hostinger\|zyro"   # harus kosong
curl -sI http://malangeducationcenter.com/ | head -3                             # 301 ke https
curl -sI https://www.malangeducationcenter.com/ | head -3                         # 301 ke apex
curl -sI https://malangeducationcenter.com/organisasi/ | head -3                  # 301 ke /#about
AUDIT_URL=https://malangeducationcenter.com npm run audit:lh
```
- [ ] NS, MX, A, TXT = Rumahweb; tak ada rujukan `hostinger`/`hstgr` di DNS.
- [ ] 9 kotak surat lengkap dan klien email staf berfungsi.
- [ ] Arsip `admin.`, `belajar.`, dan situs lama tersimpan dan tercatat lokasinya (tanpa kredensial).
- [ ] Pertanyaan terbuka dicatat untuk MEC: `belajar.` masih dipakai? Siapa pemegang lisensi skrip komersialnya? (arsip dulu, jangan dipindah).

## E. Format laporan ke pemilik proyek (tempel di chat, bukan repo)
```
Tugas: <kode, mis. A3>
Dilihat: <apa, di menu mana>
Hasil: <angka/status; tanpa nama kotak surat, sandi, isi .env>
Status: OK | perlu keputusan | blokir
Butuh persetujuan: <langkah C berikutnya + alasan>
```
