# TODO — cek file asli (untuk dikerjakan di lokal)

Diperbarui: 2026-10-10 · untuk branch `claude/new-repo-infra-tech-stack-e62imy`.
Konteks: sumber saat ini adalah hasil ekstraksi dari `MEC_UI_Preview.html` (21 MB) dan `Company Profile MEC ACADEMY.pdf` (16 halaman, versi thumbnail). Banyak foto beresolusi rendah. Tujuan: ganti dengan file mentah/asli, lalu jalankan ulang `npm run extract` (preview) atau salin ke `src/assets/images/` dengan **nama file yang sama** (kode memuat gambar lewat nama, lihat `src/lib/images.ts`).

Cara kerja per item: buka file asli, cek resolusi/kualitas, ganti, `npm run build`, lihat hasilnya, lalu centang.

## 1. Gambar yang paling perlu dicek (urut prioritas)

Ukuran = ukuran sekarang di `src/assets/images/`. Tampil = ukuran tampil terbesar di situs (layar retina menuntut ±2×).

### Prioritas tinggi (tampil besar, sumber kecil/buram)
- [ ] `ojt.jpg` — **360×203**, tampil ±640 px di beranda bab 03 (langkah "On the Job Training"). Terburuk. Cari foto OJT asli ≥ 1600 px.
- [ ] `powertrain.jpg` dan `finaldrive.jpg` — **457×609** (potret), dipakai pada tab "Jelajahi sistem" / detail modul Torqflow dan Final drive. Cari foto asli ≥ 1600 px (lanskap lebih aman).
- [ ] `gallery-01` … `gallery-20.jpg` — **1000×667**; dipakai di galeri fasilitas dan lightbox (diperbesar sampai 1600 px). Cari 20 foto asli ≥ 1600 px **beserta keterangan** (`src/data/gallery.json`). Catat mana foto yang tidak bisa dipakai (wajah, privasi).
- [ ] `classroom.jpg` — **962×542**, dipakai di langkah "Kenali dasarnya" dan halaman Tahapan/FAQ. Cari asli ≥ 1600 px.
- [ ] `logo.webp` — **479×259**, tampil di header, menu, bab "Tentang". Cari **logo vektor (SVG/AI/PDF)**; kalau tidak ada, PNG transparan ≥ 1000 px. Perlu juga versi untuk latar terang dan gelap.
- [ ] Potret instruktur `trainer-*.webp`: `trainer-chandra` dan `trainer-johan` **379×676**; `trainer-andy`, `-erik`, `-nur`, `-saifullah` **701×1052**. Cari foto asli ≥ 800 px lebar, latar rapi, pose konsisten.

### Prioritas sedang
- [ ] `event-ppa.jpg` — **787×1400 (potret)**, terpotong 63% di grid 3:2 (peringatan audit). Cari versi lanskap atau tentukan crop manual (`focus` di `src/lib/images.ts`).
- [ ] `event-komatsu.jpg` (1800×1013) — peringatan **upscale 0,96×**: cek apakah ada file asli lebih besar.
- [ ] `event-abp` 1461×720, `event-sinarindo` 1280×720, `event-trinity` 1280×720, `event-tenggarong` 1287×726, `event-ut` 1280×964 — cek ada yang lebih besar; sertakan **nama perusahaan, tanggal, dan izin tampil**.
- [ ] `alumni.jpg` (1800×809), `alumni2.jpg` (**1019×573**) — dipakai di bab Alumni dan OJT. Cari asli, dan izin alumni.
- [ ] `alumni3.jpg` (807×1077) — **tidak dipakai** di situs sekarang. Putuskan: pakai atau hapus.

### Cek kualitas saja (sudah 1800×1200, tetapi mungkin ada master lebih besar)
- [ ] `hero.jpg`, `practice.jpg`, `workshop.jpg`, `bintalsik.jpg`, `prayer.jpg`, `film.jpg`, `building.jpg`, `teaching.jpg`, `adab.jpg`, `engine.jpg`, `hydraulic.jpg` — apakah file asli ≥ 2400 px? `hero` tampil layar penuh (LCP). Kalau ada master lebih besar, ganti.
- [ ] `safety.jpg`, `safetyclose.jpg` — dipakai? `safetyclose` tidak dirujuk kode. Putuskan hapus atau pakai.

## 2. Dokumen/teks yang perlu dibandingkan dengan aslinya

Sumber: `Company Profile MEC ACADEMY.pdf` (16 halaman). Pemetaan halaman (dari `src/data/content.json` → `source_map`):

| Konten di situs | Halaman PDF | Yang dicek |
|---|---|---|
| Nama institusi, sejarah (ETTC 2018, MEC 2023, MEC Academy 2025), proposisi, metrik | 1–2 | Tahun dan nama lembaga; metrik "±600 alumni" dan "BMC 55 (per Agustus 2026)" masih berlaku? |
| Visi, misi, nilai | 3 | Salin persis, bukan parafrase |
| Legal (AHU, NIB) | 4 | `AHU-0011655-AH-01.14 Tahun 2025`, `NIB 1202250103384` — cocokkan dengan dokumen asli; tentukan boleh ditampilkan atau tidak |
| Tim (direktur, wakil, divisi) | 5 | Nama dan jabatan; **ejaan Johan "Wiharto" (hlm. 5) vs "Winarto" (hlm. 7)** — tentukan satu |
| Profil 6 instruktur (pengalaman, sertifikasi) | 6–7 | Pengalaman ditulis sebagai riwayat, bukan jabatan aktif; cek sertifikasi (BNSP ToT, POP, asesor, K3 Umum) |
| 16 modul + daftar komponen praktik | 8 | Nama modul persis; **deskripsi 12 modul** (baru 4 punya deskripsi) |
| Tahapan: Assessment, In-class, OJT | 9 | Isi tiap tahap |
| Fasilitas | 10 | Daftar: 6 ruang kelas, mess 30 siswa, workshop, musholla, pantry, kamar mandi, parkir, seragam |
| Kegiatan industri | 12–13 | Nama perusahaan, tanggal, jenis kegiatan (kunjungan / penyerahan komponen) |
| Foto alumni | 14–15 | Izin tampil |
| Kontak | 16 | Telepon/email contoh di gambar kartu **sengaja tidak dipakai**; konfirmasi nomor resmi |
| Halaman 11 | 11 | Belum dipetakan; cek isinya, mungkin ada konten yang terlewat |
| "SAA" (Sholat, Al-Qur'an, Adab) | — | Berasal dari brief percakapan, bukan PDF. Konfirmasi redaksi resmi dengan MEC |

- [ ] Verifikasi 16 modul: nama dan urutan sesuai PDF hlm. 8 (`content.json` → `modules`) dan pengelompokan tim web (`src/lib/modules.ts`).
- [ ] Cocokkan angka dan tahun di bab "Tentang MEC" (hlm. 2) dengan PDF.
- [ ] Putuskan data legal (AHU/NIB) ditampilkan atau tidak.

## 3. File lain yang perlu dicek
- [ ] `MEC_UI_Preview.html` asli: bandingkan lagi dengan hasil (hover, header, tipografi, animasi). Catat selisih yang masih terlihat.
- [ ] **Font**: situs memakai Archivo + Archivo Narrow (OFL) sebagai pengganti Nimbus Sans (AGPL). File font yang pernah Anda kirim (DejaVu, Nimbus Sans, NimbusSansNarrow-Bold.otf) + lisensinya: putuskan tetap Archivo atau memakai font asli (cek lisensi untuk web).
- [ ] **Video company profile**: YouTube `ZV39to3Qfz8` — tautan dari pengguna; konfirmasi masih benar dan boleh disematkan.
- [ ] **Sumber riset** `src/data/research.json` (ditinjau 2026-09-15) dan bagian "Arah vokasi 2026" di beranda (kutipan Kemenko PMK, 9 Sep 2026, serta United Tractors 3 Sep 2026): buka tautannya, pastikan masih aktif dan ringkasannya akurat.
- [ ] **Tautan sosial** (Facebook, Instagram, LinkedIn) dari situs lama `malangeducationcenter.com`: kumpulkan URL resmi (belum ada di situs baru).
- [ ] **Portal assessment** `malangeducationcentreacademy.my.id/assessment/`: konfirmasi URL, dan hosting-nya jatuh tempo **19 Nov 2026** (Auto Renew OFF).
- [ ] **Situs lama (Hostinger)**: salin teks/foto yang mungkin tidak ada di PDF (halaman Organisasi, Galeri, Alumni, Learning) sebelum dimatikan.

## 4. Setelah file asli masuk
- [ ] Ganti file di `src/assets/images/` (nama sama), perbarui `focus` di `src/lib/images.ts` bila crop berubah.
- [ ] `npm run build` lalu `npm run audit` (pelanggaran harus 0; peringatan upscale/crop harus turun dari 5).
- [ ] Perbarui `docs/TODO.md` bagian "Menunggu data dari klien" dan "Peringatan audit tersisa".
- [ ] Setelah ukuran gambar naik, cek bobot halaman dan LCP (`reports/lighthouse-summary.md`); sesuaikan `widths`/`sizes` bila perlu.
