# Dasar perhitungan penawaran (internal — jangan kirim ke klien)

PDF klien: `docs/Penawaran-Website-MEC-Academy.pdf` · dibuat oleh `docs/proposal/make_proposal.py` (ubah harga/teks di bagian KONFIGURASI, lalu `python3 docs/proposal/make_proposal.py`; butuh `pip install reportlab`).

## Cara angka Rp 32.000.000 didapat
Estimasi usaha kerja manual oleh developer menengah–senior (hari kerja):

| Komponen | Estimasi hari | Harga di PDF |
|---|---|---|
| Perencanaan, fondasi teknis, pemindahan konten dari desain contoh | 2–3 | Rp 3.000.000 |
| Beranda interaktif 12 bagian (animasi scroll, layar pembuka, logo) | 10–12 | Rp 9.500.000 |
| 14 jenis halaman / 44 halaman | 6–7 | Rp 6.000.000 |
| Blog artikel + SEO teknis + pencarian | 5 | Rp 5.000.000 |
| Responsif HP/tablet/laptop + pengujian | 3–4 | Rp 3.500.000 |
| Kecepatan, aksesibilitas, laporan audit | 3 | Rp 3.000.000 |
| Layar pembuka, penanganan error, 404 | 2 | Rp 2.000.000 |
| **Total** | **±31–36 hari** | **Rp 32.000.000** |

≈ 35 hari × ±Rp 900 ribu/hari.

## Rentang yang masuk akal (perkiraan, bukan data pasar terverifikasi)
- **Batas bawah ±Rp 22 juta** — tarif freelance ramah anggaran, atau bila animasi dikurangi.
- **Rekomendasi Rp 30–35 juta** (dipakai: 32 juta) — website custom + animasi + blog siap SEO, sudah teruji.
- **Bila lewat studio/agensi ±Rp 45–60 juta** — untuk cakupan yang sama, karena ada manajemen proyek, desain, dan garansi.

Tarif harian Rp 750 ribu–1,2 juta menghasilkan Rp 26–43 juta untuk 35 hari. Silakan ganti dengan tarif Anda sendiri.

## Hal yang perlu Anda putuskan sebelum mengirim
- Harga akhir dan apakah mau diskon/paket (mis. gratis "Pasang di internet" bila setuju hari ini).
- Isi `PENYAJI` (nama & kontak Anda) di skrip.
- PPN, termin pembayaran (default DP 50% / pelunasan 50%), jumlah revisi (default 2× kecil), dan tarif pemeliharaan.
- Harga add-on di PDF adalah usulan; biaya domain/email adalah kisaran umum dan berubah menurut penyedia.

## Batasan
- Hanya mencakup yang **sudah dibuat**. Isi tersisa (foto asli, deskripsi modul, info biaya/jadwal, artikel, deploy) ada di add-on atau bahan dari klien.
- Harga bukan biaya jam kerja; pekerjaan dibantu AI selesai lebih cepat dari estimasi manual di atas. Penetapan harga sebaiknya berdasarkan nilai hasil dan pasar, bukan sekadar waktu.
