# Rencana konten SEO (draf kerangka; belum ditulis atau diterbitkan)

Tujuan: menjawab pertanyaan nyata calon peserta dan orang tua, mengarahkan ke halaman modul/tahapan dan WhatsApp. **Semua fakta (biaya, durasi, sertifikasi, penempatan kerja) harus dikonfirmasi MEC** sebelum terbit; jangan menjanjikan penempatan kerja (kebijakan situs). Penulis/peninjau sebaiknya instruktur MEC (sinyal keahlian), dengan tautan ke halaman instrukturnya.

## Pilar dan kata kunci sasaran
| Pilar (kategori) | Kata kunci utama (verifikasi volume di Search Console/Keyword Planner) |
|---|---|
| Info BMC & OJT | kursus mekanik alat berat Malang · pelatihan mekanik alat berat Jawa Timur · syarat masuk pelatihan mekanik alat berat · apa itu OJT mekanik · MEC Academy / Malang Education Center |
| Karier Mekanik Alat Berat | prospek kerja mekanik alat berat · mekanik vs operator alat berat · gaji mekanik alat berat *(hati-hati klaim angka: sertakan sumber)* |
| Pengetahuan Teknis | sistem hidrolik alat berat · undercarriage excavator · cara membaca part book · perawatan berkala alat berat |
| K3 & Budaya Kerja | APD di workshop alat berat · K3 mekanik alat berat · budaya kerja industri alat berat |
| Cerita Alumni | alumni mekanik alat berat *(butuh izin alumni)* |

## 9 artikel awal (urutan prioritas)
| # | Judul kerja | Niat pencari | Halaman internal yang ditaut | Data dari MEC |
|---|---|---|---|---|
| 1 | Syarat Masuk Pelatihan Mekanik Alat Berat di MEC Academy Malang | calon peserta, berniat daftar | `/tahapan-seleksi/`, `/kontak/` | persyaratan (sudah di situs; konfirmasi), alur seleksi |
| 2 | Apa Itu Basic Mechanic Course (BMC)? Materi, Tahapan, dan OJT | informasi awal | `/program/basic-mechanic-course/`, 16 modul | durasi in-class 3 bulan, OJT 3–6 bulan (konfirmasi) |
| 3 | Mekanik atau Operator Alat Berat: Apa Bedanya? | membandingkan jalur | `/program/...`, `/instruktur/` | pandangan instruktur |
| 4 | Prospek Karier Mekanik Alat Berat di Indonesia | motivasi, orang tua | `/industri/`, `/alumni/` | sumber eksternal terpercaya, contoh kegiatan industri (tanpa jaminan kerja) |
| 5 | Mengenal Sistem Hidrolik Alat Berat untuk Pemula | belajar | modul Hydraulic system | ulasan instruktur |
| 6 | Undercarriage Alat Berat: Fungsi, Komponen, dan Perawatan | belajar | modul Final drive & undercarriage | ulasan instruktur |
| 7 | APD dan K3 Dasar di Workshop Alat Berat | keselamatan | modul Basic safety | prosedur MEC |
| 8 | Cara Membaca Part Book Alat Berat | belajar | modul Part book reading | contoh halaman (izin merek) |
| 9 | Cerita Alumni BMC *(setelah izin)* | bukti sosial | `/alumni/` | wawancara, foto, izin tertulis |

## Pedoman tiap artikel
- 700–1.200 kata, satu `<h1>`, subjudul bertanya (H2), daftar poin, 3–5 tautan internal, 1 CTA WhatsApp yang relevan.
- Isi frontmatter lengkap (`description` 120–155 huruf, `cover` + `coverAlt`, `relatedModules`, `faq` 2–4 pertanyaan agar ikut skema FAQ).
- Kategori baru otomatis diindeks setelah ≥ 3 artikel (`MIN_ARTICLES` di `src/lib/articles.ts` dan `astro.config.mjs`); sebelum itu `noindex` dan tidak masuk sitemap.
- Ritme: 1 artikel/minggu selama 2 bulan; bagikan di Instagram dan profil Google Business Profile ("Postingan").
- Ukur di Search Console: impresi dan klik per kueri; perkuat artikel yang mulai muncul di halaman 2.
