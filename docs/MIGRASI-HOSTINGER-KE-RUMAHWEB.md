# Rencana migrasi Hostinger → Rumahweb (batas aman: Selasa 14 Okt 2026)

Direvisi: 2026-10-11 berdasarkan pengecekan hPanel Hostinger dan client zone Rumahweb (read-only).
Layanan hosting dan email Hostinger **berakhir 15 Okt** (hPanel: "4 hari lagi", auto-renew nonaktif). Pakai **14 Okt** sebagai batas aman, target selesai **Selasa 13 Okt** (H-1).
Prinsip: **tidak ada yang tersisa di Hostinger** (situs, email, DNS, berkas, dan pihak ketiga yang bergantung padanya).

> DNS ikut mati bersama Hostinger, jadi **nameserver wajib dipindah ke Rumahweb** sebelum batas. Saran lama "ubah A record di Hostinger" tidak berlaku.

## 1. Inventaris (hasil cek hPanel)

| # | Komponen | Kondisi | Tindakan |
|---|---|---|---|
| 1 | **Situs utama** `malangeducationcenter.com` (AI/Website Builder) | 20 URL di sitemap: 8 halaman asli (`/`, `/organisasi`, `/galeri`, `/alumni`, `/hubungi-kami`, `/assessment`, `/learning`, `/syarat-in-class`) + 12 halaman contoh bawaan templat yang ikut terindeks | Cadangkan, ganti situs baru, redirect/410 (`public/.htaccess`) |
| 2 | **Subdomain `admin.`** | WordPress (PHP 8.3, dibuat Feb 2026), hanya "Default page"; ada database dan backup harian. DNS: ALIAS ke `connect.hostinger.com` | **Rencana: arsipkan backup, lalu matikan**; hapus `admin` dari zona baru (menunggu konfirmasi MEC) |
| 3 | **Subdomain `belajar.`** | Skrip LMS/sekolah **komersial** (CodeIgniter 4) yang dipasang Jul 2026; **HTTP 500** (kemungkinan PHP 7.4 terlalu rendah, belum terverifikasi); tidak ada record DNS-nya (tidak pernah tayang publik); ada database + backup harian. `.env` sudah diblokir dari web (403) | **Rencana: arsipkan berkas + database (jangan dibuka, jangan ke git), jangan dipindah.** Pindah hanya bila MEC memastikan akan dipakai dan lisensinya jelas; itu bisa dikerjakan setelah deadline karena arsip sudah aman |
| 4 | **Gambar situs lama** | 153 berkas (±60 MB) di `assets.zyrosite.com` (CDN Hostinger), hilang saat layanan mati | `node scripts/backup-old-site.mjs` |
| 5 | **Email** (paket "Free Business Email" ikut hosting) | **9 kotak surat, total ±78 MB**, hampir semuanya di kotak surat operasional; sisanya kecil | Buat ulang di Rumahweb, salin isi (IMAP) |
| 6 | **DNS zone** | NS `ns1/ns2.dns-parking.com` | Bangun ulang di Rumahweb (lihat §3), ganti NS |
| 7 | **Formulir, forwarder, analitik, verifikasi Google** | belum terverifikasi (tidak ada TXT verifikasi Google di zona) | Cek hPanel; verifikasi ulang Search Console |
| 8 | Akun & penagihan Hostinger | milik MEC | Jangan batalkan sebelum §5 lengkap |

Ketiga website berada dalam **satu paket Business** yang sama, jadi semuanya berhenti bersamaan.

**Temuan konten:** `/syarat-in-class` di situs lama memuat persyaratan peserta yang belum ada di situs baru (SMA/SMK, sehat, tidak buta warna/berkacamata/bertato, tinggi min. 163 cm, usia maks. 23 tahun; in-class 3 bulan; OJT 3–6 bulan). Konfirmasi MEC lalu masukkan ke Tahapan/FAQ.

### Zona DNS Hostinger yang sebenarnya
```
ALIAS  @       → *.cdn.hstgr.net        (bukan A biasa; jadi zona TIDAK bisa disalin 1:1)
CNAME  www     → www.malangeducationcenter.com.cdn.hstgr.net
ALIAS  admin   → connect.hostinger.com
MX     @       5 mx1.hostinger.com, 10 mx2.hostinger.com
TXT    @       v=spf1 include:_spf.mail.hostinger.com ~all
TXT    _dmarc  v=DMARC1; p=none
CNAME  autodiscover, autoconfig → *.mail.hostinger.com
CNAME  hostingermail-a|b|c._domainkey → hostingermail-{a,b,c}.dkim.mail.hostinger.com
NS     ns1/ns2.dns-parking.com
```
Tidak ada AAAA manual (yang terlihat di pencarian publik hanya hasil ALIAS), tidak ada TXT verifikasi Google, tidak ada record `belajar`.

## 2. Prasyarat H0 (harus selesai SEBELUM nameserver diganti)
- **Keputusan pemilik (11 Okt):** situs `.com` **tetap di akun trial** (`Unlimited M (Trial)`, server trial), **tanpa addon**; build yang dipasang adalah branch **`staging`** (multi-halaman), bukan `dev`.
  - Risiko yang diterima: trial **tidak bisa di-upgrade**, masa berlaku tidak tertulis, dan **email 9 kotak surat juga akan berada di akun trial**. Mitigasi: (a) simpan salinan lokal `dist/` + arsip supaya bisa dipasang ulang di paket lain dalam hitungan menit; (b) buka tiket Rumahweb: apakah Free Account boleh dipakai produksi dan kapan berakhir; (c) pertahankan Hostinger (perpanjangan 1 bulan) sampai jawaban tiket jelas.
  - Target IP zona DNS = IP server **trial** (bukan IP `Unlimited M`). Jangan menutup atau menghapus akun trial.
  - Konsekuensi proposal: Paket Ringkas yang ditandatangani menyebut satu halaman; build `staging` memuat blog dan halaman terpisah. Pemilik sudah mengetahui dan memilih ini.
- [ ] Aktifkan Auto Renew `Unlimited M` (portal `.my.id`) hanya untuk portal; tidak terkait situs `.com` lagi.
- [ ] **Jaring pengaman:** perpanjangan Hostinger 1 bulan tersedia (sampai 15 Nov); pembayaran ditangani pemilik. Jika diambil, migrasi bisa dilakukan lebih tenang; urutan langkah tetap sama.
- [ ] Catat **IP server** hosting, dan isi **Nameserver Setting** Rumahweb (client zone > Domain > Nameserver Setting) yang akan dipakai.
- [ ] **Arsipkan `admin.` dan `belajar.` sebelum Selasa 13 Okt**, apa pun keputusannya: ekspor database + unduh berkas dari hPanel, simpan **terenkripsi dan offline/Drive MEC**, **jangan masuk repo git**, jangan membuka `.env` (memuat kredensial; ganti sandi DB bila arsip pernah dibagikan). Backup harian Hostinger ikut hilang saat paket berakhir.
- [ ] Keputusan MEC (pertanyaan terbuka): (a) apakah `belajar.` masih dipakai/direncanakan; (b) siapa pemegang lisensi skrip komersialnya (bukti beli, kunci lisensi, apakah boleh dipasang di server lain); (c) `admin.` setuju dimatikan.
- [ ] Minta akses hPanel (ekspor formulir/analitik, daftar forwarder) bila belum.

## 3. Aturan DNS
- Pakai nameserver hosting Rumahweb yang tercantum di halaman info hosting (`ns1.rumahweb.com`, `ns2.rumahweb.com`, `ns3.rumahweb.net`, `ns4.rumahweb.net`) dan **zona cPanel**, bukan produk "Managed DNS" (client zone memperingatkan bisa mengganggu hosting).
- **Delegasi NS bisa butuh sampai 48 jam.** NS harus diganti paling lambat **Minggu malam**; zona Hostinger tetap hidup sampai 13 Okt.
- Zona **tahap 1** (email masih di Hostinger): `A @` → IP hosting Rumahweb; `www` CNAME → `@`; salin MX, SPF, DMARC, 3 DKIM, `autodiscover`, `autoconfig` persis seperti Hostinger. Jangan membuat AAAA. `admin` ikuti keputusan §2.
- Zona **tahap 2** (setelah email pindah): `MX` → server mail Rumahweb; `SPF` → `v=spf1 +a +mx +ip4:<IP hosting> ~all`; DKIM dari cPanel (Email Deliverability); hapus CNAME DKIM/`autodiscover`/`autoconfig` Hostinger.
- Domain terdaftar di **Rumahweb** (aktif sampai 23 Agu 2028, auto-renew OFF). **Harga .COM naik per 15 Okt 2026**: aktifkan auto-renew atau cek biaya perpanjangan.

## 4. Jadwal

### H0 · Sabtu 10 – Minggu 11 Okt (pagi): persiapan
- [ ] Prasyarat §2 (terutama hosting berbayar).
- [ ] Cadangan situs lama: `node scripts/backup-old-site.mjs` → `backup/hostinger-site/` (HTML, teks, 153 gambar), salin ke Drive; periksa `LAPORAN.txt`.
- [ ] Cadangan `admin.` dan `belajar.` (file + DB).
- [ ] cPanel Rumahweb: tambahkan domain, unggah build situs (branch `dev`) ke `public_html/`, uji lewat file `hosts`.
- [ ] Buat 9 kotak surat yang sama di cPanel Rumahweb (sandi sementara); reset sandi lama di Hostinger bila perlu untuk IMAP.

### H1 · Minggu 11 Okt (batas malam): nameserver
- [ ] Zona tahap 1 di Zone Editor; cocokkan dengan §1.
- [ ] Ganti NS di Nameserver Setting.
- [ ] Setelah domain mengarah ke Rumahweb: **Run AutoSSL** (SSL/TLS Status). Situs lama mengirim HSTS (2 tahun); jika sertifikat telat terbit, pengunjung lama melihat error.
- [ ] Pasang pengalihan alamat lama (`public/.htaccess`).

### H2 · Senin 12 Okt: email
- [ ] Salin isi semua kotak surat (IMAP, sumber `imap.hostinger.com:993`): `imapsync`, Thunderbird, atau bantuan Trouble Ticket Rumahweb. Total hanya ±78 MB, jadi ringan.
- [ ] **Syarat lanjut: kotak surat lengkap**, yaitu jumlah pesan per folder di Rumahweb = di Hostinger untuk ke-9 kotak surat.
- [ ] Ubah MX → Rumahweb (tahap 2); aktifkan SPF/DKIM; atur ulang klien email staf.
- [ ] Uji kirim/terima dua arah (Gmail, Outlook), cek mail-tester.

### H3 · Selasa 13 Okt: penutupan
- [ ] Sinkron IMAP susulan (surat yang masih masuk ke Hostinger).
- [ ] Search Console: verifikasi ulang (TXT via zona Rumahweb), kirim `sitemap-index.xml`; periksa Google Business Profile dan bio sosial.
- [ ] Ekspor terakhir dari Hostinger (formulir, forwarder, analitik).
- [ ] Uji akhir online: dialog dan tautan langsung, redirect lama dan 410 halaman templat, HTTP→HTTPS, www→apex, Lighthouse (`AUDIT_URL=https://malangeducationcenter.com npm run audit:lh`).

### H4 · Rabu 14 Okt (batas aman): verifikasi bersih
- [ ] Jalankan §5. Jangan batalkan manual sebelum semua centang; biarkan kedaluwarsa atau batalkan setelah H4 aman.

## 5. Verifikasi "tidak ada yang tersisa"
```
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=NS"    # ns*.rumahweb.*
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=MX"    # tanpa hostinger
curl -s "https://dns.google/resolve?name=admin.malangeducationcenter.com&type=A"
curl -sI https://malangeducationcenter.com/ | grep -i "hcdn\|hostinger\|zyro"  # kosong
grep -rniE "zyrosite|hstgr|hostinger" src public   # hanya komentar .htaccess
```
- [ ] NS, MX, A, TXT semuanya Rumahweb; tak ada rujukan `hostinger.com` / `hstgr.net` di DNS.
- [ ] Situs baru tidak memuat sumber dari `assets.zyrosite.com`.
- [ ] 9 kotak surat lengkap di Rumahweb; kirim/terima OK; klien email staf sudah dipindah.
- [ ] `admin.` dan `belajar.` sudah diputuskan (dipindah/dialihkan/dimatikan) dan file + DB-nya tercadangkan.
- [ ] Cadangan situs lama tersimpan (folder + Drive).
- [ ] Persyaratan peserta dari `/syarat-in-class` sudah dipindah atau dicatat sebagai TODO konten.

## 6. Rollback
Sebelum batas: kembalikan NS ke `ns1/ns2.dns-parking.com` (zona Hostinger masih utuh). Untuk email: kembalikan MX ke Hostinger (hanya sebelum Hostinger mati).

## 7. Risiko dan keputusan
| Risiko | Mitigasi |
|---|---|
| Hosting Rumahweb masih trial saat NS dipindah | jadikan berbayar di H0 sebelum menyentuh nameserver |
| SSL telat terbit setelah NS pindah (HSTS) | Run AutoSSL segera; kerjakan saat sepi; jangan matikan zona Hostinger |
| Email hilang | sinkron IMAP dua kali (H2 dan H3), syarat "kotak surat lengkap", simpan salinan lokal (`.mbox`) |
| `belajar.` berisi data penting yang rusak (HTTP 500; kemungkinan karena PHP 7.4 sudah tidak tersedia di hPanel, opsi hanya 8.2 ke atas; belum diubah) | ekspor file + DB sekarang, simpan offline, putuskan bersama MEC |
| Record DNS tersembunyi terlewat (forwarder, formulir) | cek hPanel; belum terverifikasi |
| Akses hPanel/cPanel telat | perpanjang Hostinger 1 bulan sebagai jaring pengaman (khusus email) |
| Konten situs baru belum final | **tayang dulu**, perbaiki bertahap |
| Hosting portal assessment `.my.id` jatuh tempo **19 Nov 2026** (Auto Renew OFF) | bayar atau aktifkan Auto Renew sebelum tanggal itu |

## 8. Belum terverifikasi
Isi Nameserver Setting Rumahweb, IP server hosting trial, isi dan ukuran file/DB `admin.` dan `belajar.`, apakah ada forwarder email atau formulir di Hostinger.
