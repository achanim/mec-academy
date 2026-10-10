# Panduan email staf MEC (pindah dari Hostinger ke Rumahweb)

Dokumen ini untuk dibagikan ke staf. Tidak memuat sandi: sandi diberikan terpisah oleh pemilik.

## 1. Pengumuman (salin dan kirim)
> **Pemberitahuan penting: email @malangeducationcenter.com pindah server**
>
> Layanan email lama (Hostinger) **berhenti 15 Oktober 2026**. Email kita sudah dipindah ke server baru. Yang perlu Anda lakukan:
> 1. **Mulai sekarang pakai kotak surat baru** dengan pengaturan di bawah. Alamat email Anda **tidak berubah**; sandi baru diberikan terpisah.
> 2. **Pindahkan surat lama yang penting sendiri sebelum 15 Oktober** (panduan di bawah). Surat yang masih ada di server lama setelah tanggal itu **hilang dan tidak bisa dipulihkan**.
> 3. Selama ±4 jam pertama, sebagian surat masuk bisa masih tiba di server lama. Cek kedua tempat hari ini dan besok.
> 4. Bila ada kendala, hubungi admin sebelum 14 Oktober.

## 2. Pengaturan aplikasi email (Thunderbird, Outlook, HP)
| | Nilai |
|---|---|
| Nama pengguna | alamat email lengkap (mis. `nama@malangeducationcenter.com`) |
| Sandi | sandi baru dari admin |
| Server masuk (IMAP) | `mail.malangeducationcenter.com`, port **993**, SSL/TLS |
| Server keluar (SMTP) | `mail.malangeducationcenter.com`, port **465**, SSL/TLS, autentikasi sama |
| Webmail | https://malangeducationcenter.com:2096 |

Hapus akun lama (server `imap.hostinger.com` / `smtp.hostinger.com`) dari aplikasi **hanya setelah** surat penting selesai dipindah. Kuota tiap kotak surat 1 GB.

## 3. Memindahkan surat lama (Thunderbird, ±10–30 menit per orang)
1. Pasang Thunderbird, tambahkan **dua akun**: akun **lama** (IMAP `imap.hostinger.com`, port 993, SSL/TLS, sandi lama) dan akun **baru** (tabel di atas).
2. Biarkan akun lama selesai sinkron (lihat bilah status; folder besar butuh waktu).
3. Di akun lama, buka folder yang penting (Inbox, Terkirim, folder lain). Pilih semua pesan (**Ctrl+A**), lalu **seret** ke folder yang sama di akun baru (atau klik kanan > *Salin ke*; pilih **salin**, bukan pindah).
4. Cek: jumlah pesan di folder baru sama dengan folder lama.
5. Opsional (cadangan di komputer): klik kanan akun lama > **Salin ke** > *Folder Lokal*.
6. Alternatif cepat untuk sedikit surat: **teruskan (forward)** surat penting ke alamat baru, atau simpan lampiran pentingnya.
7. Kontak: ekspor dari buku alamat lama bila ada, impor ke yang baru.

## 4. Jika sandi lupa atau tidak bisa masuk
Hubungi admin untuk atur ulang sandi lewat cPanel. Jangan membagikan sandi lewat grup chat.

## 5. Catatan admin
- Sandi sementara dibuat di cPanel dan diberikan lewat kanal terpisah; minta staf menggantinya setelah masuk pertama.
- Jangan simpan sandi atau daftar kotak surat di repositori.
- Uji kirim/terima dua arah (Gmail dan Outlook) dan cek skor di mail-tester.com setelah MX stabil (Selasa 13 Okt).
