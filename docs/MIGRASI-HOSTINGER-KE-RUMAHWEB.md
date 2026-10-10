# Rencana migrasi Hostinger → Rumahweb (batas: Hostinger mati 14 Okt 2026)

Dibuat: 2026-10-10 (Sabtu). Hostinger berhenti **Rabu 14 Okt**; target selesai semua **Selasa 13 Okt** (H-1) supaya ada satu hari cadangan.
Prinsip: **tidak ada yang tersisa di Hostinger**: situs, email, DNS, berkas, dan semua pihak ketiga yang bergantung padanya.

> Rencana ini menggantikan saran lama "ubah A record di Hostinger": karena Hostinger akan mati, **DNS ikut mati**, jadi nameserver **wajib dipindah ke Rumahweb** sebelum 14 Okt.

## 1. Inventaris: apa saja yang ada di Hostinger

| # | Komponen | Kondisi (dari pengecekan publik) | Tindakan |
|---|---|---|---|
| 1 | **Situs** (Website Builder) | 20 URL di sitemap: `/`, `/organisasi`, `/galeri`, `/alumni`, `/hubungi-kami`, `/assessment`, `/learning`, **`/syarat-in-class`**, dan **12 halaman contoh bawaan templat** (classic-cap, face-serum, hand-soap, wooden-chair, dst.) yang ikut terindeks | Cadangkan (skrip di bawah), ganti dengan situs baru, redirect/410 (`public/.htaccess`) |
| 2 | **Gambar situs** | 153 berkas (±60 MB) di `assets.zyrosite.com` (CDN Hostinger) → **hilang saat layanan mati** | Unduh semua (skrip) |
| 3 | **Email domain** | MX `mx1/mx2.hostinger.com`; jumlah kotak surat belum diketahui (minimal `operasional@`) | Buat ulang di Rumahweb, salin isi (IMAP), pindah MX |
| 4 | **DNS zone** | NS `ns1/ns2.dns-parking.com` (Hostinger) | Salin ke Rumahweb, ganti NS (lihat §3) |
| 5 | **Formulir/pesan** dari situs lama | belum diketahui (builder biasanya menyimpan kiriman formulir) | Ekspor di hPanel jika ada |
| 6 | **Analitik, verifikasi Google, Google Business Profile** | belum diketahui | Cek di hPanel dan Search Console |
| 7 | **Akun/penagihan Hostinger** | pemilik akun: MEC | Jangan batalkan sebelum §6 selesai |
| 8 | Link media sosial di situs lama | Instagram `malangeducation`; Facebook/LinkedIn belum terisi (hanya tautan umum) | Kumpulkan URL resmi |

**Temuan penting dari situs lama:** halaman `/syarat-in-class` memuat **persyaratan peserta** yang belum ada di situs baru (SMA/SMK, sehat, tidak buta warna/berkacamata/bertato, tinggi min. 163 cm, usia maks. 23 tahun; in-class 3 bulan; OJT 3–6 bulan). Perlu dikonfirmasi MEC lalu dimasukkan ke dialog Tahapan/FAQ (di proposal, persyaratan masih "tanya tim MEC").

### Zona DNS saat ini (hasil pencarian DNS publik)
```
A      @      2 IP Hostinger (TTL 60)          AAAA @   2 IPv6 Hostinger
CNAME  www    www.malangeducationcenter.com.cdn.hstgr.net
MX     @      5 mx1.hostinger.com, 10 mx2.hostinger.com
TXT    @      v=spf1 include:_spf.mail.hostinger.com ~all
TXT    _dmarc v=DMARC1; p=none
CNAME  autodiscover / autoconfig   → autodiscover|autoconfig.mail.hostinger.com
CNAME  hostingermail-a|b|c._domainkey → hostingermail-{a,b,c}.dkim.mail.hostinger.com
NS     dns-parking.com (ns1, ns2)
```
Record lain (mis. verifikasi Google, subdomain) **tidak terlihat dari luar**; ambil daftar lengkap dari hPanel (DNS Zone) atau minta MEC screenshot.

## 2. Akses yang dibutuhkan hari ini (blokir utama)
- [ ] **Hostinger hPanel**: daftar kotak surat + reset sandi, DNS Zone lengkap, ekspor formulir/analitik, status verifikasi Google.
- [ ] **Rumahweb cPanel** (paket yang dipakai) dan akses **client zone** (ubah nameserver).
- [ ] Keputusan hosting: trial `Unlimited M (Trial)` dijadikan berbayar, atau domain ditambahkan ke `Unlimited M` milik portal assessment.
- **Jaring pengaman** bila akses Hostinger telat (batas: Minggu 11 Okt siang): minta MEC **memperpanjang paket Hostinger 1 bulan** supaya email tidak hilang. Tanpa kredensial kotak surat, isi email lama tidak bisa dipindah.

## 3. Aturan DNS (kunci kelancaran)
- Nameserver Rumahweb untuk hosting: `ns1.rumahweb.com`, `ns2.rumahweb.com`, `ns3.rumahweb.net`, `ns4.rumahweb.net` (tertera di halaman info hosting). Pakai **zona cPanel** (bukan produk "Managed DNS" di client zone yang memperingatkan gangguan hosting).
- **Delegasi NS bisa butuh hingga 48 jam** untuk merata. Karena itu NS harus diganti paling lambat **Minggu 11 Okt malam**, dan zona di Hostinger **tetap hidup dan identik** sampai 13 Okt.
- **Hapus record AAAA** (IPv6 Hostinger) di zona baru; kalau tidak, pengunjung IPv6 diarahkan ke server yang mati.
- Zona **tahap 1** (mail masih di Hostinger): salin semua record di atas, **kecuali** `A @` → IP hosting Rumahweb, `www` → CNAME ke `@`, tanpa AAAA.
- Zona **tahap 2** (setelah email pindah): `MX` → server mail Rumahweb, `SPF` → `v=spf1 +a +mx +ip4:<IP hosting> ~all`, DKIM dari cPanel (Email Deliverability), hapus CNAME `hostingermail-*`, `autodiscover`, `autoconfig` milik Hostinger.

## 4. Jadwal

### H0 · Sabtu 10 Okt — persiapan
- [ ] Minta akses §2 (kirim daftar ke MEC). 
- [ ] Jalankan **cadangan situs lama** (lokal): `node scripts/backup-old-site.mjs` → folder `backup/hostinger-site/` (HTML, teks, 153 gambar). Simpan juga ke Drive. Periksa `LAPORAN.txt` (baris GAGAL diunduh manual).
- [ ] Rumahweb: tambahkan domain `malangeducationcenter.com` ke cPanel (addon/primary), catat **IP server**.
- [ ] Build dan unggah situs baru (branch `dev`; atau `staging` untuk versi multi-halaman) ke `public_html/` domain tersebut; uji lewat file `hosts` (IP server → domain) tanpa mengubah DNS.
- [ ] Buat kotak surat yang sama di cPanel Rumahweb (minimal `operasional@`) dengan sandi sementara.

### H1 · Minggu 11 Okt — nameserver (batas akhir malam)
- [ ] Siapkan **zona tahap 1** di cPanel Zone Editor (lihat §3). Cocokkan satu per satu dengan zona Hostinger.
- [ ] Ganti nameserver di **client zone Rumahweb** ke ns1-ns4 Rumahweb.
- [ ] Setelah domain mulai mengarah ke Rumahweb: cPanel > **SSL/TLS Status > Run AutoSSL**. Situs lama mengirim HSTS (`max-age` 2 tahun); bila sertifikat telat terbit, pengunjung yang pernah membuka situs lama melihat error. Pantau sampai gembok hijau.
- [ ] Pasang pengalihan alamat lama (`public/.htaccess` sudah memuatnya).

### H2 · Senin 12 Okt — email
- [ ] Salin isi kotak surat lama → Rumahweb (IMAP: sumber `imap.hostinger.com:993`, tujuan server mail Rumahweb): `imapsync`, atau Thunderbird (dua akun, seret folder), atau minta bantuan Trouble Ticket Rumahweb. Salin juga folder Terkirim, kontak, dan alias/forwarder.
- [ ] Setelah sinkron pertama: ubah **MX → Rumahweb** (zona tahap 2). TTL MX 4 jam, jadi surat baru bisa masih masuk ke Hostinger beberapa jam.
- [ ] Aktifkan DKIM/SPF di cPanel; atur ulang aplikasi email di HP/laptop staf (server baru, sandi baru).
- [ ] Uji kirim/terima dua arah (Gmail, Outlook), cek skor di mail-tester.com.

### H3 · Selasa 13 Okt — penutupan
- [ ] **Sinkron IMAP susulan** (menangkap surat yang masih masuk ke Hostinger). Pastikan Hostinger sudah kosong dari surat baru.
- [ ] Verifikasi Google Search Console (TXT lewat zona Rumahweb), kirim `sitemap-index.xml`, minta indeks ulang beranda. Perbarui URL situs di Google Business Profile dan bio media sosial (domain sama, tetapi cek).
- [ ] Ekspor terakhir dari Hostinger (formulir, analitik, daftar kotak surat). Unduh ulang berkas yang GAGAL di laporan.
- [ ] Uji akhir situs online: semua dialog dan tautan langsung, redirect lama (`/organisasi`, `/syarat-in-class`, halaman contoh → 410), HTTP→HTTPS, www→apex, Lighthouse (`AUDIT_URL=https://malangeducationcenter.com npm run audit:lh`).

### H4 · Rabu 14 Okt — hari Hostinger mati
- [ ] Verifikasi bersih (bagian §5). Jangan batalkan manual sebelum semua centang; biarkan kedaluwarsa atau batalkan setelah H4 aman.

## 5. Verifikasi "tidak ada yang tersisa"
Perintah (jalankan dari mana saja):
```
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=NS"    # harus ns*.rumahweb.*
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=MX"    # tidak ada hostinger
curl -s "https://dns.google/resolve?name=malangeducationcenter.com&type=AAAA"  # kosong atau IPv6 Rumahweb
curl -sI https://malangeducationcenter.com/ | grep -i "hcdn\|hostinger\|zyro"  # harus kosong
grep -rniE "zyrosite|hstgr|hostinger" src public   # hanya komentar .htaccess
```
- [ ] NS, MX, A, TXT semuanya Rumahweb; tidak ada rujukan `hostinger.com`/`hstgr.net` di DNS.
- [ ] Situs baru tidak memuat sumber dari `assets.zyrosite.com` (sudah dicek: repo tidak memakainya).
- [ ] Semua kotak surat lama ada di Rumahweb; kirim/terima OK; klien email staf sudah dipindah.
- [ ] Cadangan situs lama tersimpan (folder + Drive).
- [ ] Persyaratan peserta dari `/syarat-in-class` sudah dipindah (atau dicatat sebagai TODO konten).

## 6. Rollback
Sebelum 14 Okt: kembalikan NS ke `ns1/ns2.dns-parking.com` di client zone (zona Hostinger masih utuh). Setelah email dipindah, rollback MX saja = ubah MX kembali ke Hostinger (hanya sebelum Hostinger mati).

## 7. Risiko dan keputusan
| Risiko | Mitigasi |
|---|---|
| Tidak ada akses Hostinger sampai 11 Okt | perpanjang Hostinger 1 bulan sebagai jaring pengaman |
| SSL telat terbit setelah NS pindah (HSTS) | Run AutoSSL segera; kerjakan saat sepi; jangan matikan zona Hostinger |
| Surat hilang | sinkron IMAP dua kali (H2 dan H3), simpan salinan lokal (Thunderbird/`.mbox`) |
| Record DNS tak terlihat terlewat (verifikasi, subdomain) | ekspor zona lengkap dari hPanel (butuh akses) |
| Konten situs baru belum final (foto resolusi rendah, 12 deskripsi modul) | **tayang dulu**, perbaiki bertahap; deploy ulang itu murah |
| Hosting portal assessment jatuh tempo **19 Okt**, Auto Renew OFF | bayar/aktifkan Auto Renew |
