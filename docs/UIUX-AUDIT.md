# Audit UI/UX — MEC Academy

Diukur 2026-09-29 di Chromium (desktop 1440×900, HP 390×844) dengan mode gerak dimatikan supaya semua elemen terlihat.
Angka di bawah hasil ukur otomatis, bukan perkiraan. Status: **P1–P3 yang bisa dikerjakan sudah diimplementasikan** (lihat kolom "Status" di akhir). Tersisa yang bergantung pada foto asli dari MEC.

Prioritas: **P1** = pengaruh besar ke keterbacaan/konversi/SEO · **P2** = terasa jelas · **P3** = polesan.

## A. Tipografi

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| A1 | Terlalu banyak teks kecil | 75 elemen <12px di beranda (27 × 9px, 27 × 10px, 21 × 11px). Termasuk konten penting: deskripsi instruktur (10px), keterangan metrik (9px), timeline (9px), link footer (9px), bar status (9px), label tab mesin (11px) | Lantai 12px untuk label mono (eyebrow, kicker); konten (deskripsi, caption, nama perusahaan) minimal 13–14px | P1 |
| A2 | Skala ukuran tidak konsisten | 27 ukuran berbeda dalam satu halaman (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25, 27, 42, 48, 62, 72–79, 100, 109, 115) | Tetapkan skala: 12 / 14 / 16 / 20 / 24 / 32 / 48 / clamp(display). Pakai token, bukan angka lepas | P2 |
| A3 | Body text campuran 15/16/17/20px | Paragraf pendamping heading berbeda tiap bab | Samakan: body 16–18px, lead 20–24px | P2 |
| A4 | Judul artikel/halaman dalam semua kapital | H1 artikel 3 baris kapital ("TAHAPAN BELAJAR BASIC MECHANIC COURSE DI MEC ACADEMY") sulit dibaca | Kapital hanya untuk display beranda dan label; judul panjang pakai title/sentence case | P2 |
| A5 | Heading display 72–115px memakan ruang | Di layar 900 tinggi, 3 baris heading + paragraf mendorong CTA ke bawah | Turunkan ke 64–96px pada bab padat, atau batasi 2 baris | P3 |
| A6 | Panjang baris | Paragraf konten 35–45 karakter/baris (baik); artikel 70ch (baik) | Pertahankan | – |

## B. Warna & kontras

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| B1 | Kontras teks pada latar polos | 0 kegagalan WCAG AA dari seluruh pasangan warna yang terukur (desktop & HP) | Pertahankan | – |
| B2 | Teks di atas foto belum terjamin | 18 elemen (7 di antaranya <14px): "16 modul…" (10px), "Gulir untuk menjelajah", "Tonton company profile", caption hero-frame, bar status | Tambah scrim lokal di belakang teks kecil, naikkan ukuran ≥12px dan bobot ≥500 | P1 |
| B3 | Emas dipakai terlalu banyak peran | Eyebrow, baris kedua heading, angka, border, hover link, tombol, dot, garis — semuanya emas | Sisihkan emas untuk aksi & penekanan utama; eyebrow/garis pakai sage | P2 |
| B4 | Hierarki dua baris heading di latar terang | Baris 1 ink, baris 2 hijau `#265154` — selisih tipis | Naikkan kontras baris 2 (hijau lebih gelap) atau bedakan lewat bobot | P3 |
| B5 | State interaktif | Fokus 3px emas ✓, hover tombol ✓ | Tambah state `:active` dan `disabled` yang konsisten | P3 |

## C. Foto

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| C1 | Crop terlalu agresif | Rail "Belajar" 640×225 (rasio 2,8:1) membuang 38–47% foto; foto event Putra Perkasa (potret 475×845) dipaksa 368×252 → 61% terbuang; kartu journey 13–27% | Rasio 3:2 / 16:9, atur `object-position` per foto (wajah/komponen tidak terpotong) | P1 |
| C2 | Resolusi sumber rendah | Sumber foto 475–734px tampil 407–640px → 1,0–1,3 px per CSS px. Di layar retina (2×) buram. Potret instruktur 230px lebar | Minta foto asli dari MEC (≥1600px untuk foto lebar, ≥600px untuk potret) | P1 |
| C3 | Foto terlalu kecil di ruang lega | Foto mesin 545×300 di kolom ±700px; potret instruktur 202px lebar; polaroid alumni 520px | Perbesar foto utama agar mengisi kolom; pertimbangkan tinggi 40–50vh | P2 |
| C4 | Bobot gambar | Beranda 0,8–1,4 MB total; hero 90 KB; gambar terbesar 276 KB | Sudah sehat. Setelah foto asli masuk, pertahankan AVIF/WebP + `srcset` | P3 |
| C5 | Tanpa placeholder blur | Hanya shimmer; CLS sudah 0 | Opsional: blur-up (LQIP) untuk foto besar | P3 |

## D. Layout & spasi

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| D1 | Ruang kosong tidak seimbang di bab pinned | Contoh bab Tantangan: konten 411px di layar 900px (±45% kosong); bab lain padat | Perbesar elemen utama atau tambah foto pendukung; atur ulang jarak vertikal | P2 |
| D2 | Halaman dalam terasa datar | Banner atas polos ±200px tanpa gambar; halaman modul memuat "Detail materi… akan dilengkapi" | Tambah foto per halaman; sembunyikan modul yang belum berisi atau isi deskripsi | P1 |
| D3 | Daftar 16 modul berupa list biasa | Dua kolom teks polos | Kartu dengan nomor/ikon dan pengelompokan (Fundamental / Sistem / Perawatan) | P2 |
| D4 | Halaman Kontak minim | Hanya alamat + satu tombol | Tambah peta, jam operasional, alur singkat, tombol telepon/email | P2 |
| D5 | Dua gaya footer | Beranda: bar mono kecil; halaman dalam: footer 3 kolom | Satukan | P3 |
| D6 | Grid artikel kosong | Satu kartu di grid 3 kolom, tanpa thumbnail | Thumbnail per artikel; kartu unggulan lebar bila artikel sedikit | P3 |

## E. Navigasi & alur

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| E1 | Layar intro memaksa klik tiap sesi | Progres 100% dalam ±1 dtk, lalu pengunjung harus klik "Mulai perjalanan". Untuk crawler, overlay layar penuh berisiko dianggap interstitial | Auto-lanjut ±1,2 dtk setelah 100%, tombol "Lewati" langsung aktif, lewati untuk bot & pengunjung kembali | P1 |
| E2 | Scroll sangat panjang | 8 bab pinned = ±20 layar gulir untuk isi yang muat ±8 layar; tinggi halaman 14.400px di HP | Kurangi `data-span`; tombol lompat antar-bab sudah ada (dot) — tampilkan label saat hover | P2 |
| E3 | Konversi bertumpu pada satu jalur | Semua CTA ke WhatsApp; tidak ada ringkasan biaya/jadwal/persyaratan, FAQ, testimoni, atau logo klien | Strip FAQ singkat + persyaratan di beranda; logo mitra industri (dari kegiatan) | P1 |
| E4 | Label "Gerak aktif" ambigu | 10px, tanpa ikon | Ikon + tooltip "Kurangi animasi" | P3 |
| E5 | Dot navigasi bab | Titik 4px, tanpa label | Label muncul saat hover/fokus | P3 |
| E6 | Bar status bawah | 9px, mengulang informasi bab | Naikkan ke 11–12px atau sembunyikan di bab tertentu | P3 |
| E7 | Menu hamburger | Sebelumnya 10 item × ±80px satu kolom, "Kontak" terpotong | **Sudah diperbaiki**: grid 2 kolom, muat satu layar (desktop, tablet, HP), tiap item punya deskripsi | ✅ |

## F. Aksesibilitas

- Sudah baik: satu `<h1>` per halaman, semua gambar punya `alt`, skip link, fokus terlihat, reduced-motion, target sentuh ≥32px di HP.
- Perlu: kontras teks di atas foto (B2), label teks kecil (A1), judul kapital panjang (A4).

## G. Performa

| # | Temuan | Data | Saran | Prioritas |
|---|---|---|---|---|
| G1 | Font mono terlalu besar | `MECMono` (DejaVu Sans Mono) 147 KB dari total font 184 KB (80%) di setiap halaman | Subset ke Latin (±10–15 KB) atau ganti mono lebih ringan; hemat ±130 KB per halaman | P1 |
| G2 | Lain-lain | JS/CSS kecil; hero 90 KB; CLS 0 | Pertahankan | – |

## Status pengerjaan

| Kode | Status | Catatan |
|---|---|---|
| A1 | ✅ | Lantai 12px untuk label mono; konten 13–14px. Font mono di-subset |
| A2 | ◐ | Token `--fs-*` ditambahkan; skala penuh belum dipakai di semua komponen |
| A3 | ✅ | Body 16px, lead 18–25px |
| A4 | ✅ | Judul artikel/halaman panjang memakai title case |
| A5 | ◐ | Heading display dikecilkan sedikit; sisanya dibiarkan agar sama dengan preview |
| B2 | ✅ | Scrim + text-shadow untuk teks kecil di atas foto, ukuran ≥12px |
| B3 | ◐ | Label minor memakai sage; eyebrow tetap emas mengikuti preview |
| B4 | ✅ | Baris kedua heading di latar terang memakai hijau lebih gelap |
| B5 | ✅ | State `:active` dan `disabled` |
| C1 | ✅ | Titik fokus per foto, rasio 3:2 di grid industri, rail lebih lebar-tinggi seimbang |
| C2 | ⏳ | Menunggu foto asli dari MEC (≥1600px lebar, potret ≥600px) |
| C3 | ✅ | Foto mesin, instruktur, tentang diperbesar |
| D1 | ◐ | Durasi pin dipangkas; ruang kosong sisa dibiarkan |
| D2 | ✅ | Banner berfoto, halaman modul tanpa placeholder + navigasi sebelumnya/berikutnya |
| D3 | ✅ | Modul berkelompok dalam kartu |
| D4 | ✅ | Kartu kontak, cara mendaftar, link peta |
| D5 | ✅ | Footer lengkap dipakai di halaman dalam |
| D6 | ✅ | Kartu artikel bergambar + kartu unggulan |
| E1 | ✅ | Intro masuk otomatis, tombol lewati langsung aktif, dilewati untuk crawler |
| E2 | ✅ | Bab Alumni tidak di-pin; durasi pin dipangkas; daftar horizontal di HP. Tinggi halaman desktop ±24 → ±18 layar |
| E3 | ◐ | FAQ (`/faq/` + ringkasan di beranda) dan chip mitra industri. Testimoni/logo klien belum ada datanya |
| E4–E6 | ✅ | Ikon + tooltip kontrol gerak, label dot bab, bar status ≥12px |
| G1 | ✅ | Font mono 147 KB → 8,6 KB |
