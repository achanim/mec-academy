#!/usr/bin/env python3
"""Pembuat PDF penawaran 1 lembar untuk klien awam.

Ubah harga & teks di bagian KONFIGURASI, lalu jalankan:
    pip install reportlab
    python3 docs/proposal/make_proposal.py
Hasil: docs/Penawaran-Website-MEC-Academy.pdf
Angka default adalah ESTIMASI (lihat docs/proposal/README.md untuk dasar perhitungan) — sesuaikan dengan tarif Anda.
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph, Table, TableStyle, Spacer, KeepInFrame

# ============================== KONFIGURASI ==============================
KLIEN = 'MEC Academy'
TANGGAL = '29 September 2026'
BERLAKU = '30 hari'
PENYAJI = ''            # mis. 'Nama Anda · 08xx-xxxx-xxxx · email@anda.com' (kosong = tidak ditampilkan)

PAKET = 'Paket Website Lengkap'
# (item, manfaat bagi MEC dalam bahasa awam, harga)
RINCIAN = [
    ('Perencanaan & fondasi teknis', 'Struktur situs, pengaturan awal, dan pemindahan seluruh isi dari desain contoh', 3_000_000),
    ('Beranda interaktif 12 bagian', 'Halaman utama bergerak halus saat digulir, ada layar pembuka dan logo, sesuai desain contoh', 9_500_000),
    ('Halaman-halaman utama (44 halaman)', 'Program & 16 modul, tahapan seleksi, fasilitas & galeri, profil instruktur, industri, tentang, kontak, FAQ, assessment', 6_000_000),
    ('Blog artikel + dasar SEO', 'Tempat menulis artikel agar mudah ditemukan di Google; ada kolom pencarian artikel', 5_000_000),
    ('Nyaman di HP, tablet, dan laptop', 'Tampilan dan tombol diuji di 5 ukuran layar', 3_500_000),
    ('Cepat, aman, dan mudah diakses', 'Skor kecepatan Google 98–100; laporan audit kualitas 8 halaman', 3_000_000),
    ('Layar pembuka & penanganan error', 'Halaman "tidak ditemukan" yang rapi, gambar/video gagal muat tidak merusak tampilan', 2_000_000),
]
TAMBAHAN = [
    ('Pasang di internet (nama situs, gembok keamanan, alihan alamat lama)', 'Rp 1.500.000'),
    ('Pantau jumlah pengunjung (Google Analytics & Search Console)', 'Rp 1.000.000'),
    ('Penulisan artikel agar mudah ditemukan di Google', 'Rp 350.000 / artikel · 10 artikel Rp 3.000.000'),
    ('Editor artikel untuk staf (tanpa coding)', 'Rp 3.500.000'),
    ('Formulir pendaftaran online', 'Rp 2.500.000'),
    ('Versi bahasa Inggris', 'mulai Rp 6.000.000'),
    ('Pemeliharaan bulanan (backup, pantau, ubah teks kecil)', 'mulai Rp 750.000 / bulan'),
]
BIAYA_BERJALAN = [
    ('Nama domain (mis. .id atau .com)', '±Rp 150.000–350.000 / tahun, dibayar ke penyedia domain'),
    ('Hosting (tempat situs berada)', 'Rp 0 — layanan gratis (Cloudflare) cukup untuk skala ini'),
    ('Email bisnis (opsional)', 'mulai ±Rp 100.000 / bulan'),
]
DIBUTUHKAN = ['Foto asli beresolusi tinggi (agar tajam di layar HP modern)', 'Deskripsi isi 12 modul yang belum ada',
              'Info biaya, jadwal, persyaratan, dan jam operasional', 'Keputusan nama domain dan akses ke akun-nya']
LANGKAH = [('1', 'Setuju', 'Konfirmasi penawaran & bayar DP 50%'), ('2', 'Lengkapi bahan', 'MEC kirim foto, teks modul, info biaya'),
           ('3', 'Tayang', 'Pasang di internet, uji akhir, pelatihan singkat'), ('4', 'Pelunasan', 'Sisa 50% saat situs online')]
CATATAN = 'Harga belum termasuk PPN (jika ada). Termasuk 2× putaran revisi kecil setelah situs tayang. Tampilan & kode sudah selesai; '\
          'yang tersisa adalah bahan dari MEC dan pemasangan.'
# ============================================================================

OUT = os.path.join(os.path.dirname(__file__), '..', 'Penawaran-Website-MEC-Academy.pdf')
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV', boldItalic='DV-B')

GREEN = colors.HexColor('#265154'); DEEP = colors.HexColor('#0C3438'); INK = colors.HexColor('#061F23')
GOLD = colors.HexColor('#CDBE86'); GOLD_D = colors.HexColor('#8C7B3E'); PAPER = colors.HexColor('#F3F0E4')
LINE = colors.HexColor('#D6D2C0'); OK = colors.HexColor('#1E7A4C'); GREY = colors.HexColor('#5E6E6E')

rp = lambda n: 'Rp ' + f'{n:,.0f}'.replace(',', '.')
TOTAL = sum(r[2] for r in RINCIAN)

def S(name, **k):
    b = dict(fontName='DV', fontSize=8, leading=10.6, textColor=INK); b.update(k); return ParagraphStyle(name, **b)
CELL = S('c'); CELLB = S('cb', fontName='DV-B'); SM = S('sm', fontSize=7, leading=9.2, textColor=GREY)
H = S('h', fontName='DV-B', fontSize=10, leading=13, textColor=GREEN, spaceBefore=0, spaceAfter=2)

W, Hh = A4; M = 15 * mm; CW = W - 2 * M
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle(f'Penawaran Website {KLIEN}'); c.setAuthor(PENYAJI or 'Tim pengembangan'); c.setSubject('Estimasi investasi website')

# --- pita atas ---
c.setFillColor(DEEP); c.rect(0, Hh - 38 * mm, W, 38 * mm, stroke=0, fill=1)
c.setFillColor(GOLD); c.rect(0, Hh - 38 * mm, W, 1.2 * mm, stroke=0, fill=1)
c.setFont('DV', 7.5); c.setFillColor(GOLD); c.drawString(M, Hh - 12 * mm, 'PENAWARAN · RINGKASAN INVESTASI')
c.setFont('DV-B', 21); c.setFillColor(colors.white); c.drawString(M, Hh - 23 * mm, f'Website {KLIEN}')
c.setFont('DV', 9); c.setFillColor(colors.HexColor('#C0CBC0'))
c.drawString(M, Hh - 30.5 * mm, 'Situs untuk memperkenalkan program Basic Mechanic Course dan menjaring calon peserta')
c.setFont('DV', 7.5); c.drawRightString(W - M, Hh - 12 * mm, f'{TANGGAL} · berlaku {BERLAKU}')

y = Hh - 38 * mm - 5 * mm

# --- kotak harga ---
bh = 27 * mm
c.setFillColor(colors.HexColor('#FAF8F1')); c.setStrokeColor(GOLD); c.setLineWidth(1)
c.roundRect(M, y - bh, CW, bh, 3 * mm, stroke=1, fill=1)
c.setFont('DV', 8); c.setFillColor(GREY); c.drawString(M + 6 * mm, y - 7 * mm, PAKET.upper())
c.setFont('DV-B', 26); c.setFillColor(GREEN); c.drawString(M + 6 * mm, y - 17.5 * mm, rp(TOTAL))
c.setFont('DV', 8); c.setFillColor(INK); c.drawString(M + 6 * mm, y - 23.2 * mm, 'Sekali bayar · tanpa biaya berlangganan ke kami')
# status kanan
bx = M + CW * 0.60
c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(bx - 4 * mm, y - 4 * mm, bx - 4 * mm, y - bh + 4 * mm)
c.setFillColor(OK); c.setFont('DV-B', 9); c.drawString(bx, y - 8 * mm, '✓ Sudah berjalan')
c.setFillColor(INK); c.setFont('DV', 7.8)
for i, t in enumerate(['Tampilan dan seluruh halaman sudah selesai', 'dan sudah lolos pengujian kecepatan Google.', 'Tinggal bahan dari MEC dan pemasangan.']):
    c.drawString(bx, y - (13.4 + i * 4.3) * mm, t)
y -= bh + 5 * mm

# --- rincian ---
def tbl(rows, widths, head=None, price_col=None):
    data = ([[Paragraph(h, S('th', fontName='DV-B', textColor=colors.white)) for h in head]] if head else []) + rows
    t = Table(data, colWidths=widths)
    st = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
          ('TOPPADDING', (0, 0), (-1, -1), 2.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6), ('LINEBELOW', (0, 0), (-1, -1), 0.4, LINE)]
    if head: st.append(('BACKGROUND', (0, 0), (-1, 0), GREEN))
    for i in range(1 if head else 0, len(data)):
        if (i % 2) == 0: st.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FAF8F1')))
    if price_col is not None: st.append(('ALIGN', (price_col, 0), (price_col, -1), 'RIGHT'))
    t.setStyle(TableStyle(st)); return t

def draw(flow, x, y_top, w, h):
    f = Frame(x, y_top - h, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList([KeepInFrame(w, h, flow, mode='shrink')], c)

rows = [[Paragraph(f'<b>{a}</b>', CELL), Paragraph(b, CELL), Paragraph(f'<b>{rp(p)}</b>', CELL)] for a, b, p in RINCIAN]
rows.append([Paragraph('<b>Total</b>', CELL), '', Paragraph(f'<b>{rp(TOTAL)}</b>', CELL)])
t = tbl(rows, [CW * 0.28, CW * 0.52, CW * 0.20], head=['Yang dikerjakan', 'Manfaatnya untuk MEC', 'Harga'], price_col=2)
t.setStyle(TableStyle([('BACKGROUND', (0, len(rows)), (-1, len(rows)), colors.HexColor('#EFEBD9')), ('LINEABOVE', (0, len(rows)), (-1, len(rows)), 0.8, GREEN)]))
w_, h_ = t.wrapOn(c, CW, 200 * mm)
draw([Paragraph('Apa yang Anda dapatkan', H), t], M, y, CW, h_ + 8 * mm); y -= h_ + 8 * mm + 4 * mm

# --- dua kolom: tambahan & biaya berjalan ---
gap = 5 * mm; cw2 = (CW - gap) / 2
t1 = tbl([[Paragraph(a, CELL), Paragraph(f'<b>{b}</b>', CELL)] for a, b in TAMBAHAN], [cw2 * 0.52, cw2 * 0.48])
t2 = tbl([[Paragraph(a, CELL), Paragraph(b, CELL)] for a, b in BIAYA_BERJALAN], [cw2 * 0.42, cw2 * 0.58])
_, h1 = t1.wrapOn(c, cw2, 200 * mm); _, h2 = t2.wrapOn(c, cw2, 200 * mm)
need = [Paragraph('<b>Yang perlu disiapkan MEC</b>', S('hh', fontName='DV-B', fontSize=8.5, textColor=GREEN, spaceBefore=6, spaceAfter=2))] + \
       [Paragraph(f'• {d}', S('li', fontSize=7.8, leading=10.2, leftIndent=8, firstLineIndent=-8)) for d in DIBUTUHKAN]
right = [Paragraph('Biaya berjalan (bayar ke penyedia)', H), t2] + need
col_h = max(h1 + 8 * mm, h2 + 8 * mm + 34 * mm)
draw([Paragraph('Tambahan opsional', H), t1], M, y, cw2, col_h)
draw(right, M + cw2 + gap, y, cw2, col_h)
y -= col_h + 4 * mm

# --- langkah ---
c.setFillColor(GREEN); c.setFont('DV-B', 10); c.drawString(M, y - 3 * mm, 'Langkah berikutnya')
y -= 6 * mm; bw = (CW - 3 * 3 * mm) / 4; bh2 = 19 * mm
for i, (n, ttl, d) in enumerate(LANGKAH):
    x = M + i * (bw + 3 * mm)
    c.setFillColor(PAPER); c.setStrokeColor(LINE); c.setLineWidth(0.6); c.roundRect(x, y - bh2, bw, bh2, 2 * mm, stroke=1, fill=1)
    c.setFillColor(GREEN); c.circle(x + 5 * mm, y - 5.4 * mm, 2.9 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont('DV-B', 8); c.drawCentredString(x + 5 * mm, y - 6.4 * mm, n)
    c.setFillColor(INK); c.setFont('DV-B', 8); c.drawString(x + 10 * mm, y - 6.3 * mm, ttl)
    p = Paragraph(d, S('sd', fontSize=7, leading=9, textColor=GREY)); f = Frame(x + 2.5 * mm, y - bh2 + 0.8 * mm, bw - 5 * mm, 10 * mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f.addFromList([p], c)
y -= bh2 + 3.5 * mm

# --- catatan + footer ---
f = Frame(M, y - 13 * mm, CW, 13 * mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
f.addFromList([Paragraph(CATATAN, SM)], c)
c.setStrokeColor(LINE); c.line(M, 12 * mm, W - M, 12 * mm)
c.setFont('DV', 7); c.setFillColor(GREY)
c.drawString(M, 8 * mm, PENYAJI or f'Penawaran untuk {KLIEN}')
c.drawRightString(W - M, 8 * mm, 'Estimasi; harga final disepakati tertulis')
c.showPage(); c.save()
print('OK', OUT, rp(TOTAL), 'y_akhir(mm)=', round(y / mm, 1))
