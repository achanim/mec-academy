#!/usr/bin/env python3
"""Proposal rincian biaya (multi-halaman) — MEC Academy.

Ubah data di bagian KONFIGURASI/DATA lalu jalankan:
    pip install reportlab
    python3 docs/proposal/make_proposal_detail.py
Hasil: docs/Proposal-Website-MEC-Academy-Rincian-Biaya.pdf
Semua total dihitung dari data (ada assert), jadi angka tidak bisa saling bertentangan.
Font Inter (SIL OFL) ada di docs/proposal/fonts/.
"""
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak,
                                NextPageTemplate, KeepTogether, CondPageBreak, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'Proposal-Website-MEC-Academy-Rincian-Biaya.pdf')

# ============================== KONFIGURASI ==============================
NO_PROPOSAL = '001/PRP/IX/2026'
TANGGAL = '29 September 2026'
BERLAKU = '30 hari sejak tanggal proposal'
KLIEN = 'MEC Academy'
KLIEN_ENTITAS = 'CV MEC Academy'
KLIEN_ALAMAT = 'Jl. Jatisari No. 07, Patuksari, Desa Plaosan, Kec. Wonosari, Kab. Malang, Jawa Timur'
# Isi data penyedia jasa; kosong = ditampilkan sebagai garis isian pada tanda tangan
PENYEDIA = {'nama': '', 'npwp': '', 'kontak': '', 'rekening': ''}
TARIF_PERUBAHAN = 150_000          # Rp/jam untuk pekerjaan di luar lingkup
GARANSI_HARI = 30
# ============================================================================

# ------------------------------ DATA BIAYA --------------------------------
# (kode, pekerjaan & hasil, usaha hari, biaya)
PAKET_LENGKAP = [
    ('A', 'Persiapan & fondasi', [
        ('A1', 'Perencanaan: peta situs, kebutuhan halaman, struktur URL', 1.0, 800_000),
        ('A2', 'Penyiapan proyek: repositori, standar kode, pengujian otomatis dasar', 1.0, 1_000_000),
        ('A3', 'Pemindahan isi dari desain contoh: foto (format modern), font, data konten', 1.0, 1_200_000)]),
    ('B', 'Beranda interaktif', [
        ('B1', 'Sistem desain: warna, huruf, komponen, header & menu', 1.5, 1_500_000),
        ('B2', 'Beranda 12 bagian: tata letak & isi', 3.5, 3_000_000),
        ('B3', 'Animasi scroll: 7 bagian ter-pin, zoom foto, geser horizontal, tab 3D', 4.0, 3_500_000),
        ('B4', 'Layar pembuka, mode gerak tenang, navigasi antar-bagian', 2.0, 1_500_000)]),
    ('C', 'Halaman-halaman utama', [
        ('C1', 'Program BMC + 16 halaman modul (berkelompok, navigasi sebelum/sesudah)', 2.0, 1_800_000),
        ('C2', 'Tahapan seleksi, Fasilitas + galeri foto dengan pembesar', 1.5, 1_200_000),
        ('C3', 'Instruktur (daftar + 6 profil), Industri, Tentang, Sumber informasi', 1.5, 1_500_000),
        ('C4', 'Assessment (langkah + FAQ), Kontak, FAQ umum (9 pertanyaan)', 2.0, 1_500_000)]),
    ('D', 'Blog & optimasi mesin pencari (SEO)', [
        ('D1', 'Sistem artikel: kategori, sampul, penulis, waktu baca, artikel terkait', 1.5, 1_500_000),
        ('D2', 'SEO teknis: meta, sitemap, RSS, data terstruktur (organisasi, kursus, artikel, FAQ, profil)', 2.0, 2_000_000),
        ('D3', 'Pencarian artikel + 1 artikel contoh', 1.0, 800_000),
        ('D4', 'Robots, struktur URL, kesiapan pengalihan alamat lama', 1.0, 700_000)]),
    ('E', 'Responsif & pengujian tampilan', [
        ('E1', 'Tampilan HP, tablet, laptop, layar lebar', 2.5, 2_000_000),
        ('E2', 'Pengujian 5 ukuran layar × 16 halaman, target sentuh, tanpa geser mendatar', 1.5, 1_500_000)]),
    ('F', 'Kecepatan, aksesibilitas & audit', [
        ('F1', 'Optimasi gambar/font, kestabilan tata letak (CLS), target skor Lighthouse 95 ke atas', 1.5, 1_400_000),
        ('F2', 'Aksesibilitas: kontras, keyboard, pembaca layar, mode kurangi animasi', 1.0, 900_000),
        ('F3', 'Skrip audit otomatis + pemeriksaan di CI + laporan', 1.0, 700_000)]),
    ('G', 'Ketahanan & penanganan error', [
        ('G1', 'Skeleton loading & penanganan gagal muat (gambar, video, pencarian, offline)', 1.0, 1_000_000),
        ('G2', 'Halaman 404/500, penanganan error global, cadangan bila animasi gagal', 1.0, 1_000_000)]),
]
# Pengurangan Paket Inti dari Paket Lengkap (kode, uraian, pengurang)
INTI_KURANG = [
    ('B3', 'Animasi scroll disederhanakan: hanya muncul-saat-digulir (tanpa ter-pin, zoom, 3D)', 2_500_000),
    ('B4', 'Tanpa layar pembuka & mode gerak tenang', 1_500_000),
    ('C3', 'Tanpa profil per-instruktur, halaman Industri, dan Sumber informasi', 1_000_000),
    ('D2', 'Data terstruktur dasar saja (organisasi & artikel)', 500_000),
    ('D3', 'Tanpa pencarian artikel', 800_000),
    ('F3', 'Tanpa skrip audit otomatis & pemeriksaan CI', 700_000),
    ('G1', 'Tanpa skeleton loading (hanya halaman 404 & error dasar)', 1_000_000),
]
# Tambahan Paket Lengkap+ (uraian, harga normal, harga paket)
PLUS_TAMBAH = [
    ('Pemasangan online: domain, sertifikat keamanan (SSL), pengalihan alamat', 1_500_000, 1_500_000),
    ('10 artikel SEO (riset kata kunci, 700–1.000 kata, terbit terjadwal)', 3_000_000, 3_000_000),
    ('Pemeliharaan 12 bulan: cadangan, pemantauan, perbaikan & ubah teks kecil', 6_000_000, 4_500_000),
]
ADDONS = [
    ('Pemasangan online (domain, SSL, pengalihan alamat)', 'Sekali', 'Rp 1.500.000'),
    ('Pantau pengunjung: Google Analytics & Search Console', 'Sekali', 'Rp 1.000.000'),
    ('Artikel SEO (riset kata kunci + penulisan)', 'Per artikel', 'Rp 350.000 · paket 10 = Rp 3.000.000'),
    ('Editor artikel untuk staf tanpa coding (CMS)', 'Sekali', 'Rp 3.500.000'),
    ('Formulir pendaftaran online (ke WhatsApp/email)', 'Sekali', 'Rp 2.500.000'),
    ('Versi bahasa Inggris (tergantung jumlah konten)', 'Sekali', 'mulai Rp 6.000.000'),
    ('Pemeliharaan bulanan (min. 6 bulan)', 'Per bulan', 'Rp 500.000'),
    ('Sesi pelatihan tambahan (2 jam)', 'Per sesi', 'Rp 500.000'),
    ('Pekerjaan di luar lingkup', 'Per jam', f'Rp {TARIF_PERUBAHAN:,.0f}'.replace(',', '.')),
]
BIAYA_BERJALAN = [
    ('Nama domain (.id / .com)', 'Rp 150.000 – 350.000 / tahun', 'Dibayar ke penyedia domain atas nama MEC. Pasar: Rp 150–500 rb/tahun'),
    ('Hosting (tempat situs berada)', 'Rp 0', 'Memakai layanan gratis Cloudflare Pages. Pasar hosting umum: Rp 0,5–6 juta/tahun'),
    ('Email bisnis (opsional)', 'Rp 100.000 – 150.000 / pengguna / bulan', 'Contoh: Google Workspace'),
    ('Pemeliharaan (opsional setelah masa paket)', 'Rp 500.000 / bulan', 'Setara ±19% biaya awal per tahun; acuan pasar 15–25%'),
]
TERMIN = [('M1', 'Persetujuan proposal & penandatanganan', 40), ('M2', 'Bahan lengkap & situs siap ditinjau (staging)', 40), ('M3', 'Tayang, serah terima & pelatihan', 20)]

# ------------------------------ HITUNG & VALIDASI -------------------------
sum_wp = lambda wp: sum(i[3] for i in wp[2]); day_wp = lambda wp: sum(i[2] for i in wp[2])
HARGA_LENGKAP = sum(sum_wp(w) for w in PAKET_LENGKAP); HARI_LENGKAP = sum(day_wp(w) for w in PAKET_LENGKAP)
HARGA_INTI = HARGA_LENGKAP - sum(k[2] for k in INTI_KURANG)
HARGA_PLUS = HARGA_LENGKAP + sum(t[2] for t in PLUS_TAMBAH)
assert HARGA_LENGKAP == 32_000_000, HARGA_LENGKAP
assert HARGA_INTI == 24_000_000, HARGA_INTI
assert HARGA_PLUS == 41_000_000, HARGA_PLUS
assert sum(t[2] for t in TERMIN) == 100
rp = lambda n: 'Rp ' + f'{n:,.0f}'.replace(',', '.')
jt = lambda n: f'{n/1_000_000:.1f}'.replace('.', ',') + ' jt'
DAY_RATE = HARGA_LENGKAP / HARI_LENGKAP

# ------------------------------ WARNA & FONT ------------------------------
NAVY = colors.HexColor('#0B1F3A'); NAVY2 = colors.HexColor('#12305A'); BLUE = colors.HexColor('#2557D6'); BLUE_L = colors.HexColor('#E8EEFC')
SLATE = colors.HexColor('#334155'); MUTE = colors.HexColor('#64748B'); LINE = colors.HexColor('#DCE3EE'); BG = colors.HexColor('#F6F8FB')
AMBER = colors.HexColor('#E8A317'); GREEN = colors.HexColor('#15803D'); RED = colors.HexColor('#B42318'); WHITE = colors.white
for name, f in [('Inter', 'Inter.ttf'), ('Inter-M', 'Inter-M.ttf'), ('Inter-SB', 'Inter-SB.ttf'), ('Inter-B', 'Inter-B.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, 'fonts', f)))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-B', italic='Inter', boldItalic='Inter-B')
hexs = lambda c: '#' + c.hexval()[2:]

def PS(n, **k):
    d = dict(fontName='Inter', fontSize=9.2, leading=14, textColor=SLATE, alignment=TA_LEFT); d.update(k); return ParagraphStyle(n, **d)
BODY = PS('body'); SMALL = PS('small', fontSize=7.8, leading=11, textColor=MUTE); LEAD = PS('lead', fontSize=10.4, leading=16, textColor=SLATE)
H1 = PS('H1', fontName='Inter-B', fontSize=19, leading=23, textColor=NAVY, spaceBefore=0, spaceAfter=8)
H2 = PS('H2', fontName='Inter-SB', fontSize=11, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=4)
EYEBROW = PS('eb', fontName='Inter-SB', fontSize=7.6, leading=10, textColor=BLUE, spaceAfter=2)
TC = PS('tc', fontSize=8.3, leading=11.6); TCB = PS('tcb', fontName='Inter-SB', fontSize=8.3, leading=11.6, textColor=NAVY)
TCW = PS('tcw', fontName='Inter-SB', fontSize=8, leading=11, textColor=WHITE); TCR = PS('tcr', fontSize=8.3, leading=11.6, alignment=TA_RIGHT)
TCRB = PS('tcrb', fontName='Inter-SB', fontSize=8.3, leading=11.6, alignment=TA_RIGHT, textColor=NAVY); TCC = PS('tcc', fontSize=8.3, leading=11.6, alignment=TA_CENTER)
BUL = PS('bul', leftIndent=11, firstLineIndent=0, bulletIndent=1, spaceAfter=2.4)

W, H = A4; ML = 20 * mm; MR = 20 * mm; CW = W - ML - MR
P = lambda t, s=BODY: Paragraph(t, s)
def bullets(items, s=BUL): return [Paragraph(i, s, bulletText='•') for i in items]

# ------------------------------ FLOWABLE KHUSUS ---------------------------
class Mark(Flowable):
    """Ikon centang / strip untuk matriks paket."""
    def __init__(self, ok=True, size=11): super().__init__(); self.ok = ok; self.size = size; self.width = size; self.height = size
    def wrap(self, aw, ah): return self.size, self.size
    def draw(self):
        c = self.canv; s = self.size
        if self.ok:
            c.setFillColor(BLUE_L); c.circle(s / 2, s / 2, s / 2, stroke=0, fill=1)
            c.setStrokeColor(BLUE); c.setLineWidth(1.3); c.setLineCap(1); c.setLineJoin(1)
            p = c.beginPath(); p.moveTo(s * .27, s * .5); p.lineTo(s * .43, s * .34); p.lineTo(s * .74, s * .68); c.drawPath(p, stroke=1, fill=0)
        else:
            c.setStrokeColor(colors.HexColor('#B8C2D0')); c.setLineWidth(1.2); c.line(s * .3, s * .5, s * .7, s * .5)

def tbl(rows, widths, head=True, zebra=True, extra=None, pad=4):
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    st = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
          ('TOPPADDING', (0, 0), (-1, -1), pad), ('BOTTOMPADDING', (0, 0), (-1, -1), pad), ('LINEBELOW', (0, 0), (-1, -1), 0.4, LINE)]
    if head: st += [('BACKGROUND', (0, 0), (-1, 0), NAVY)]
    if zebra:
        for i in range(2 if head else 1, len(rows), 2): st.append(('BACKGROUND', (0, i), (-1, i), BG))
    if extra: st += extra
    t.setStyle(TableStyle(st)); return t

def head(*labels, align=None):
    return [Paragraph(l, PS('th', fontName='Inter-SB', fontSize=8, textColor=WHITE, alignment=(align[i] if align else TA_LEFT))) for i, l in enumerate(labels)]

def callout(text, kind='info'):
    col = {'info': BLUE, 'warn': AMBER, 'ok': GREEN}[kind]; bg = {'info': BLUE_L, 'warn': colors.HexColor('#FEF6E0'), 'ok': colors.HexColor('#E7F5EC')}[kind]
    t = Table([[Paragraph(text, PS('co', fontSize=8.8, leading=13.2, textColor=NAVY))]], colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LINEBEFORE', (0, 0), (0, -1), 3, col), ('LEFTPADDING', (0, 0), (-1, -1), 10),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)])); return t

def kpi(items):
    cells = []
    for v, l in items:
        cells.append([Paragraph(f'<font name="Inter-B" size="19" color="{hexs(BLUE)}">{v}</font>', PS('kv', leading=23)), Paragraph(l, PS('kl', fontSize=7.8, leading=10.5, textColor=MUTE))])
    t = Table([cells], colWidths=[CW / len(items)] * len(items))
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, LINE), ('INNERGRID', (0, 0), (-1, -1), 0.5, LINE), ('BACKGROUND', (0, 0), (-1, -1), BG),
                           ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8), ('LEFTPADDING', (0, 0), (-1, -1), 10), ('VALIGN', (0, 0), (-1, -1), 'TOP')])); return t

def stacked_bar():
    d = Drawing(CW, 46 + 14 * 4); x = 0; total = HARGA_LENGKAP; bw = CW
    pal = ['#0B1F3A', '#2557D6', '#4F7DE8', '#7EA1F0', '#A9C0F5', '#E8A317', '#8FA3BF']
    for i, wp in enumerate(PAKET_LENGKAP):
        w = bw * sum_wp(wp) / total
        d.add(Rect(x, 14 * 4 + 14, w - 1.5, 20, fillColor=colors.HexColor(pal[i]), strokeColor=None))
        pct = round(100 * sum_wp(wp) / total)
        if w > 22: d.add(String(x + 4, 14 * 4 + 20, f'{pct}%', fontName='Inter-SB', fontSize=7.4, fillColor=WHITE if i < 4 or i == 6 else NAVY))
        x += w
    for i, wp in enumerate(PAKET_LENGKAP):
        col, row = divmod(i, 4); lx = col * (CW / 2); ly = 14 * (3 - row) + 2
        d.add(Rect(lx, ly, 7, 7, fillColor=colors.HexColor(pal[i]), strokeColor=None))
        d.add(String(lx + 11, ly, f'{wp[0]}. {wp[1]}  ·  {jt(sum_wp(wp))}', fontName='Inter', fontSize=7.8, fillColor=SLATE))
    return d

def gantt():
    rows = [('Kickoff, perencanaan, sistem desain', 0, 1.0), ('Beranda interaktif dan animasi', 1.0, 3.5),
            ('Halaman utama, modul, blog dan SEO', 3.0, 5.5), ('Responsif, kecepatan, ketahanan, audit', 5.0, 7.0),
            ('MEC: kirim bahan, tinjau, 2 putaran revisi', 1.5, 7.5), ('Pemasangan online, pelatihan, serah terima', 7.5, 8.5),
            (f'Masa garansi perbaikan {GARANSI_HARI} hari', 8.5, 12)]
    lw = 178; wk = 12; cw_ = (CW - lw) / wk; rh = 18
    d = Drawing(CW, rh * (len(rows) + 1) + 6)
    top = rh * len(rows) + 4
    for w in range(wk):
        d.add(Rect(lw + w * cw_, 0, cw_ - 1, rh * len(rows) + 2, fillColor=BG if w % 2 == 0 else WHITE, strokeColor=None))
        d.add(String(lw + w * cw_ + cw_ / 2, top + 5, f'M{w + 1}', fontName='Inter-SB', fontSize=7, fillColor=MUTE, textAnchor='middle'))
    for i, (lab, a, b) in enumerate(rows):
        y = rh * (len(rows) - 1 - i) + 3
        d.add(String(0, y + 5, lab, fontName='Inter', fontSize=7.7, fillColor=SLATE))
        col = AMBER if i == 6 else (BLUE if i == 4 else NAVY)
        d.add(Rect(lw + a * cw_, y + 2, max((b - a) * cw_, 6), 10, rx=3, ry=3, fillColor=col, strokeColor=None))
    return d

def market_bar():
    Wd = CW; d = Drawing(Wd, 92); lo, hi = 0, 90; sx = lambda v: 8 + (Wd - 16) * (v - lo) / (hi - lo)
    bands = [('Dasar', 5, 12, '#C9D3E3'), ('Profesional', 12, 35, '#9DB4E8'), ('Kustom/Premium', 35, 80, '#5C82DE')]
    for lab, a, b, col in bands:
        d.add(Rect(sx(a), 44, sx(b) - sx(a) - 1, 16, fillColor=colors.HexColor(col), strokeColor=None))
        d.add(String((sx(a) + sx(b)) / 2, 49, lab, fontName='Inter-SB', fontSize=7.4, fillColor=NAVY if col != '#5C82DE' else WHITE, textAnchor='middle'))
        d.add(String(sx(a), 33, f'Rp {a} jt', fontName='Inter', fontSize=6.8, fillColor=MUTE))
    d.add(String(sx(80), 33, 'Rp 80 jt', fontName='Inter', fontSize=6.8, fillColor=MUTE))
    for v, lab, col in [(HARGA_INTI / 1e6, 'Inti', BLUE), (HARGA_LENGKAP / 1e6, 'Lengkap', NAVY), (HARGA_PLUS / 1e6, 'Lengkap+', AMBER)]:
        d.add(Line(sx(v), 44, sx(v), 68, strokeColor=col, strokeWidth=1.6)); d.add(Circle(sx(v), 70, 3.2, fillColor=col, strokeColor=None))
        d.add(String(sx(v), 78, f'{lab} {v:.0f} jt', fontName='Inter-SB', fontSize=7.6, fillColor=col, textAnchor='middle'))
    return d

# ------------------------------ DOKUMEN -----------------------------------
class Doc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == 'H1':
            txt = fl.getPlainText(); key = 'k%s' % self.seq.nextf('k'); self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(txt, key, 0, 0); self.notify('TOCEntry', (0, txt, self.page, key))

def cover(c, d):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H * 0.36, W, H * 0.64, stroke=0, fill=1)
    c.setFillColor(NAVY2)
    for r, a in [(150, .5), (105, .5), (62, .5)]:
        c.setStrokeColor(NAVY2); c.setLineWidth(1); c.circle(W - 40 * mm, H - 48 * mm, r, stroke=1, fill=0)
    c.setFillColor(BLUE); c.rect(ML, H - 46 * mm, 22 * mm, 1.6 * mm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#9DB4E8')); c.setFont('Inter-SB', 8.5); c.drawString(ML, H - 36 * mm, 'PROPOSAL PENGEMBANGAN WEBSITE')
    c.setFillColor(WHITE); c.setFont('Inter-B', 36); c.drawString(ML, H - 68 * mm, 'Website')
    c.drawString(ML, H - 83 * mm, KLIEN)
    c.setFont('Inter', 12.5); c.setFillColor(colors.HexColor('#C7D4EA'))
    c.drawString(ML, H - 100 * mm, 'Rincian ruang lingkup, biaya, jadwal, dan ketentuan')
    c.drawString(ML, H - 107 * mm, 'untuk program Basic Mechanic Course')
    # meta
    y0 = H * 0.36 - 16 * mm
    rows = [('Disiapkan untuk', f'{KLIEN_ENTITAS}\n{KLIEN_ALAMAT}'), ('Disiapkan oleh', PENYEDIA['nama'] or 'Penyedia jasa pengembangan web'),
            ('Nomor · Tanggal', f'{NO_PROPOSAL} · {TANGGAL}'), ('Masa berlaku', BERLAKU)]
    for i, (k, v) in enumerate(rows):
        yy = y0 - i * 17 * mm
        c.setFillColor(MUTE); c.setFont('Inter-SB', 7.6); c.drawString(ML, yy, k.upper())
        c.setFillColor(NAVY); c.setFont('Inter-M', 10)
        for j, line in enumerate(v.split('\n')):
            if j: c.setFont('Inter', 8.4); c.setFillColor(SLATE)
            c.drawString(ML, yy - 5.2 * mm - j * 4.6 * mm, line)
    c.setFillColor(MUTE); c.setFont('Inter', 7.6); c.drawString(ML, 14 * mm, 'Dokumen ini bersifat rahasia dan hanya ditujukan kepada penerima yang tercantum.')
    c.restoreState()

def body_page(c, d):
    c.saveState()
    c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(ML, H - 15 * mm, W - MR, H - 15 * mm); c.line(ML, 15 * mm, W - MR, 15 * mm)
    c.setFillColor(NAVY); c.setFont('Inter-SB', 7.6); c.drawString(ML, H - 12 * mm, f'PROPOSAL WEBSITE {KLIEN.upper()}')
    c.setFillColor(MUTE); c.setFont('Inter', 7.6); c.drawRightString(W - MR, H - 12 * mm, f'No. {NO_PROPOSAL}')
    c.drawString(ML, 10.5 * mm, f'Rahasia · {TANGGAL}'); c.drawRightString(W - MR, 10.5 * mm, f'Halaman {d.page}')
    c.setFillColor(BLUE); c.rect(ML, H - 15.6 * mm, 16 * mm, 1.1 * mm, stroke=0, fill=1)
    c.restoreState()

doc = Doc(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=24 * mm, bottomMargin=22 * mm,
          title=f'Proposal Website {KLIEN} — Rincian Biaya', author=PENYEDIA['nama'] or 'Penyedia jasa', subject='Proposal, ruang lingkup dan rincian biaya')
frame = Frame(ML, 22 * mm, CW, H - 46 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
cframe = Frame(ML, 20 * mm, CW, 10 * mm, id='c')
doc.addPageTemplates([PageTemplate(id='cover', frames=[cframe], onPage=cover), PageTemplate(id='body', frames=[frame], onPage=body_page)])

S = [NextPageTemplate('body'), PageBreak()]
def sec(num, title): return [P(f'BAGIAN {num}', EYEBROW), P(title, H1)]

# ---- Daftar isi + ringkasan eksekutif ----
toc = TableOfContents(); toc.levelStyles = [PS('toc0', fontName='Inter-M', fontSize=9.4, leading=17, textColor=NAVY, leftIndent=0, rightIndent=0)]
toc.dotsMinLevel = 0
S += [P('DAFTAR ISI', EYEBROW), toc, Spacer(1, 6 * mm)]
S += [P('RINGKASAN EKSEKUTIF', EYEBROW), P('Ringkasan eksekutif', H1)]
S += [P(f'{KLIEN} memerlukan website resmi yang memperkenalkan program <b>Basic Mechanic Course (BMC)</b>, meyakinkan calon peserta dan orang tua, '
        f'serta menjadi kanal jangka panjang lewat artikel yang mudah ditemukan di Google. Proposal ini merinci apa yang dikerjakan, berapa biayanya, '
        f'kapan selesai, dan apa saja yang diperlukan dari pihak {KLIEN}.', LEAD), Spacer(1, 3 * mm)]
S += [kpi([('±44', 'halaman website'), ('16', 'modul pelatihan tersaji'), ('95+', 'target skor kecepatan Google (Lighthouse)'), ('3', 'pilihan paket')]), Spacer(1, 4 * mm)]
S += [callout(f'<b>Rekomendasi kami: Paket Lengkap, {rp(HARGA_LENGKAP)}.</b> Website dibangun dari nol mengikuti desain acuan (preview) yang sudah Anda miliki: beranda interaktif, halaman program dan modul, blog dengan SEO, tampilan HP, serta pengujian kualitas. '
              f'Paket Inti ({rp(HARGA_INTI)}) lebih ringkas; Paket Lengkap+ ({rp(HARGA_PLUS)}) sudah termasuk pemasangan online, 10 artikel, dan pemeliharaan setahun.', 'ok'), Spacer(1, 3 * mm)]
S += [P('Mengapa harganya begini', H2), *bullets([
    f'<b>Harga tetap</b> per paket, dirinci per pekerjaan (Bagian 5). Usaha kerja ditampilkan sebagai transparansi: {HARI_LENGKAP:.0f} hari kerja, setara ±{rp(round(DAY_RATE, -3))} per hari.',
    '<b>Sejalan dengan pasar</b>: kelas “Profesional” (8–15 halaman, blog, SEO) di Indonesia berkisar Rp 12–35 juta dan “Kustom/Premium” Rp 35–80 juta (Lampiran A). Website ini ±44 halaman dengan animasi kustom, sehingga berada di rentang atas kelas Profesional.',
    '<b>Tanpa biaya hosting</b>: situs dipasang di layanan gratis (Cloudflare Pages) sehingga biaya berjalan hanya domain.',
    '<b>Anda memiliki hasilnya</b>: situs, isi, dan kode sumber menjadi milik MEC setelah pelunasan (Bagian 8).'])]

# ---- 01 Pemahaman & status ----
S += [PageBreak()] + sec('1', 'Pemahaman kebutuhan dan peningkatan yang diusulkan')
S += [P('Tujuan bisnis yang kami tangkap', H2), *bullets([
    'Memperkenalkan program BMC (16 modul, praktik komponen, OJT) dan membangun kepercayaan: instruktur bersertifikat, fasilitas, kegiatan bersama industri.',
    'Mengarahkan calon peserta ke satu tindakan yang jelas: menghubungi tim lewat WhatsApp untuk jadwal, biaya, dan persyaratan.',
    'Menjaring calon peserta secara organik lewat artikel dan halaman yang terindeks Google (SEO).',
    'Mudah dirawat: tim MEC dapat menambah artikel tanpa bergantung pada developer (opsional).'])]
PERBAIKAN = [
    ('Berkas tunggal ±21 MB; foto dan font tertanam di dalamnya',
     'Foto dikonversi ke format modern dan ukuran sesuai layar; font dimuat efisien; halaman dipecah sehingga cepat dibuka di HP', ['A3', 'F1']),
    ('Satu halaman panjang, tanpa halaman terpisah dan navigasi',
     'Struktur situs ±44 halaman: beranda, Program BMC, 16 modul, tahapan, fasilitas, instruktur, industri, tentang, assessment, kontak, FAQ, dengan menu dan URL yang jelas', ['A1', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']),
    ('Animasi baru berupa contoh tampilan',
     'Animasi scroll disusun ulang agar ringan dan stabil, dilengkapi mode kurangi gerak, cadangan bila gagal, dan aksesibilitas (kontras, keyboard)', ['B3', 'B4', 'F2']),
    ('Belum ada blog dan SEO',
     'Sistem artikel, sitemap, RSS, data terstruktur, pencarian, dan struktur URL agar mudah ditemukan Google', ['D1', 'D2', 'D3', 'D4']),
    ('Belum dirancang untuk HP dan tablet',
     'Tampilan responsif dan pengujian di 5 ukuran layar; target sentuh yang nyaman', ['E1', 'E2']),
    ('Belum ada penanganan gagal muat dan error',
     'Skeleton loading, halaman 404/500, penanganan gambar/video gagal dan koneksi terputus', ['G1', 'G2']),
    ('Belum ada pengujian kualitas',
     'Pengujian otomatis dasar, skrip audit, dan laporan hasil sebelum tayang', ['A2', 'F3']),
]
_biaya = {it[0]: it[3] for wp in PAKET_LENGKAP for it in wp[2]}
assert sorted(k for p in PERBAIKAN for k in p[2]) == sorted(_biaya), 'setiap pekerjaan harus dipetakan tepat satu kali'
S += [P('Kondisi desain awal dan yang perlu ditingkatkan', H2),
      P('Desain acuan (preview) sudah menunjukkan arah tampilan yang tepat, tetapi masih berupa contoh, belum siap dipakai sebagai website. Berikut peningkatan yang diusulkan dan biayanya pada Paket Lengkap.')]
rows = [head('Kondisi awal', 'Peningkatan yang dikerjakan', 'Biaya', align=[TA_LEFT, TA_LEFT, TA_RIGHT])]
for a, b, ks in PERBAIKAN:
    rows.append([P(f'<b>{a}</b>', TC), P(b, TC), Paragraph(rp(sum(_biaya[k] for k in ks)), TCR)])
rows.append([P('', TC), P('<b>Total Paket Lengkap</b>', TCB), Paragraph(f'<b>{rp(HARGA_LENGKAP)}</b>', TCRB)])
S += [Spacer(1, 2 * mm), tbl(rows, [CW * 0.29, CW * 0.52, CW * 0.19], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), BLUE_L)])]
S += [Spacer(1, 2 * mm), P('Rincian per pekerjaan ada di Bagian 4. Paket Inti mengurangi sebagian peningkatan di atas (Bagian 5).', SMALL)]

# ---- 02 Ruang lingkup ----
S += [PageBreak()] + sec('2', 'Ruang lingkup pekerjaan')
inc = [P('<b>Termasuk (Paket Lengkap)</b>', TCB)] + bullets([
    'Beranda 12 bagian: animasi scroll, layar pembuka, mode kurangi animasi',
    'Program BMC dan 16 halaman modul; tahapan seleksi; fasilitas + galeri',
    '6 profil instruktur; halaman Industri, Tentang, Sumber, Assessment, Kontak, FAQ',
    'Blog artikel dengan kategori, sampul, pencarian, dan data terstruktur untuk Google',
    'Tampilan HP, tablet, laptop; pengujian 5 ukuran layar',
    'Optimasi kecepatan, aksesibilitas, halaman error, laporan audit',
    'Serah terima kode sumber, panduan penggunaan, pelatihan singkat'])
exc = [P('<b>Tidak termasuk</b>', TCB)] + bullets([
    'Penulisan isi/teks (kecuali paket artikel), fotografi & video',
    'Pembuatan logo/identitas visual baru',
    'Hosting berbayar, email bisnis, dan biaya domain',
    'Sistem ujian online (portal assessment tetap di alamat yang ada)',
    'Pembayaran online, toko, sistem akun/LMS',
    'Jaminan peringkat Google; iklan berbayar',
    'Pemeliharaan setelah masa garansi (kecuali paket/opsi)'])
t = Table([[inc, exc]], colWidths=[CW * 0.53, CW * 0.47]); t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOX', (0, 0), (-1, -1), 0.5, LINE), ('LINEAFTER', (0, 0), (0, -1), 0.5, LINE), ('BACKGROUND', (1, 0), (1, 0), BG),
                                                                              ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
S += [t, P('Asumsi dan ketergantungan', H2), *bullets([
    'Harga mengacu pada <b>44 halaman, 16 modul, satu bahasa (Indonesia)</b>. Penambahan modul/halaman/bahasa dihitung terpisah.',
    f'{KLIEN} menyediakan bahan (foto, teks, info biaya) dan menunjuk <b>satu penanggung jawab</b> yang memberi umpan balik maksimal 3 hari kerja.',
    'Domain dan seluruh akun layanan (Cloudflare, repositori) dibuat atas nama MEC sejak awal.',
    'Jadwal bergeser sebanding dengan keterlambatan bahan atau persetujuan dari pihak MEC.'])]

# ---- 03 Paket ----
S += [PageBreak()] + sec('3', 'Pilihan paket')
S += [P('Tiga paket disusun bertingkat. Semuanya menggunakan fondasi yang sama; perbedaannya ada pada kedalaman animasi, kelengkapan halaman, dan layanan tambahan setelah situs jadi.')]
def m(ok): return Mark(ok)
feat = [('Beranda 12 bagian + desain responsif', True, True, True), ('Program BMC + 16 halaman modul', True, True, True), ('Tahapan seleksi, fasilitas & galeri, kontak, FAQ, assessment', True, True, True),
        ('Profil per-instruktur, halaman Industri & Sumber', False, True, True), ('Animasi scroll penuh (ter-pin, zoom, 3D)', False, True, True), ('Layar pembuka + mode gerak tenang', False, True, True),
        ('Blog artikel + SEO teknis', True, True, True), ('Data terstruktur lengkap (kursus, FAQ, profil, breadcrumb)', False, True, True), ('Pencarian artikel', False, True, True),
        ('Skeleton loading & penanganan gagal muat', False, True, True), ('Skrip audit otomatis + pemeriksaan CI + laporan', False, True, True),
        ('Pemasangan online (domain, SSL, pengalihan alamat)', False, False, True), ('10 artikel SEO (riset kata kunci + penulisan)', False, False, True), ('Pemeliharaan 12 bulan', False, False, True)]
rows = [[Paragraph('', TCW), Paragraph('INTI', PS('p1', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_CENTER)),
         Paragraph('LENGKAP', PS('p2', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_CENTER)), Paragraph('LENGKAP+', PS('p3', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_CENTER))]]
rows += [[P(f, TC), m(a), m(b), m(c)] for f, a, b, c in feat]
rows += [[P('<b>Investasi</b>', TCB)] + [Paragraph(f'<font name="Inter-B" size="10" color="{hexs(NAVY)}">{rp(v)}</font>', PS('pr', alignment=TA_CENTER, leading=16)) for v in (HARGA_INTI, HARGA_LENGKAP, HARGA_PLUS)]]
rows += [[P('Cocok untuk', TC)] + [P(x, PS('cf', fontSize=7.6, leading=10.4, alignment=TA_CENTER, textColor=MUTE)) for x in ('Anggaran terbatas, kebutuhan dasar profesional', 'Kebutuhan penuh sesuai desain contoh', 'Ingin langsung tayang, punya konten & dirawat 1 tahun')]]
tp = tbl(rows, [CW * 0.46, CW * 0.18, CW * 0.18, CW * 0.18], extra=[
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'), ('BACKGROUND', (2, 0), (2, 0), BLUE), ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#EEF3FE')),
    ('BACKGROUND', (0, len(rows) - 2), (-1, len(rows) - 2), BLUE_L), ('LINEABOVE', (0, len(rows) - 2), (-1, len(rows) - 2), 0.8, BLUE)], zebra=False)
S += [Spacer(1, 3 * mm), tp, Spacer(1, 2 * mm), P('Kolom LENGKAP adalah rekomendasi kami: mewujudkan desain acuan secara penuh.', SMALL)]

# ---- 04 Rincian biaya Paket Lengkap ----
S += [PageBreak()] + sec('4', f'Rincian biaya — Paket Lengkap ({rp(HARGA_LENGKAP)})')
S += [P(f'Setiap pekerjaan dirinci menurut hasil kerjanya. Kolom “Usaha” menunjukkan perkiraan hari kerja sebagai bahan transparansi; harga yang mengikat adalah harga tetap per paket. '
        f'Rata-rata ±{rp(round(DAY_RATE, -3))} per hari kerja.')]
rows = [head('Kode', 'Pekerjaan dan hasil yang diserahkan', 'Usaha', 'Biaya', align=[TA_LEFT, TA_LEFT, TA_RIGHT, TA_RIGHT])]
extra = []
for wp in PAKET_LENGKAP:
    r0 = len(rows)
    rows.append([Paragraph(f'<b>{wp[0]}</b>', TCB), Paragraph(f'<b>{wp[1]}</b>', TCB), Paragraph(f'<b>{day_wp(wp):.1f} hr</b>'.replace('.', ','), TCRB), Paragraph(f'<b>{rp(sum_wp(wp))}</b>', TCRB)])
    extra += [('BACKGROUND', (0, r0), (-1, r0), BLUE_L)]
    for code, txt, hari, biaya in wp[2]:
        rows.append([P(code, PS('cd', fontSize=7.8, textColor=MUTE)), P(txt, TC), Paragraph(f'{hari:.1f} hr'.replace('.', ','), TCR), Paragraph(rp(biaya), TCR)])
rows.append([P('', TC), Paragraph('<b>TOTAL PAKET LENGKAP</b>', PS('tt', fontName='Inter-B', fontSize=9, textColor=WHITE)), Paragraph(f'<b>{HARI_LENGKAP:.1f} hr</b>'.replace('.', ','), PS('tt2', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_RIGHT)),
             Paragraph(f'<b>{rp(HARGA_LENGKAP)}</b>', PS('tt3', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_RIGHT))])
extra += [('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), NAVY)]
S += [Spacer(1, 2 * mm), tbl(rows, [CW * 0.08, CW * 0.62, CW * 0.11, CW * 0.19], zebra=False, extra=extra, pad=2.5)]
S += [CondPageBreak(75 * mm), P('Ke mana uang dialokasikan', H2), stacked_bar(), Spacer(1, 2 * mm),
      P(f'Bobot terbesar ada pada <b>beranda interaktif ({round(100 * sum_wp(PAKET_LENGKAP[1]) / HARGA_LENGKAP)}%)</b> karena animasi kustom paling menuntut pengembangan dan pengujian; '
        f'pondasi SEO, blog, dan kualitas teknis (D–G) bersama-sama {round(100 * sum(sum_wp(w) for w in PAKET_LENGKAP[3:]) / HARGA_LENGKAP)}% — porsi yang menentukan hasil jangka panjang di Google dan kenyamanan pengguna.', BODY)]

# ---- 05 Selisih paket ----
S += [PageBreak()] + sec('5', 'Rincian selisih: Paket Inti dan Paket Lengkap+')
S += [P('Paket Inti — dikurangi dari Paket Lengkap', H2)]
rows = [head('Kode', 'Yang dikurangi', 'Pengurang', align=[TA_LEFT, TA_LEFT, TA_RIGHT])]
rows += [[P(c, PS('cd', fontSize=7.8, textColor=MUTE)), P(t_, TC), Paragraph(f'– {rp(v)}', TCR)] for c, t_, v in INTI_KURANG]
rows += [[P('', TC), P('<b>Total pengurang</b>', TCB), Paragraph(f'<b>– {rp(sum(k[2] for k in INTI_KURANG))}</b>', TCRB)],
         [P('', TC), P(f'<b>Paket Inti = {rp(HARGA_LENGKAP)} – {rp(sum(k[2] for k in INTI_KURANG))}</b>', TCB), Paragraph(f'<b>{rp(HARGA_INTI)}</b>', TCRB)]]
S += [tbl(rows, [CW * 0.09, CW * 0.65, CW * 0.26], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), BLUE_L)]), Spacer(1, 2 * mm),
      P('Paket Inti tetap profesional dan responsif, tetapi terasa lebih “statis”: tanpa layar pembuka, animasi scroll sederhana, dan tanpa alat audit otomatis. Dapat ditingkatkan ke Paket Lengkap kapan saja dengan membayar selisihnya.', SMALL)]
S += [P('Paket Lengkap+ — ditambahkan pada Paket Lengkap', H2)]
rows = [head('Yang ditambahkan', 'Harga normal', 'Harga paket', align=[TA_LEFT, TA_RIGHT, TA_RIGHT])]
rows += [[P(t_, TC), Paragraph(rp(a), TCR), Paragraph(rp(b), TCR)] for t_, a, b in PLUS_TAMBAH]
normal = sum(t_[1] for t_ in PLUS_TAMBAH); paket = sum(t_[2] for t_ in PLUS_TAMBAH)
rows += [[P('<b>Total tambahan</b>', TCB), Paragraph(f'<b>{rp(normal)}</b>', TCRB), Paragraph(f'<b>{rp(paket)}</b>', TCRB)],
         [P(f'<b>Paket Lengkap+ = {rp(HARGA_LENGKAP)} + {rp(paket)}</b>', TCB), Paragraph('', TCR), Paragraph(f'<b>{rp(HARGA_PLUS)}</b>', TCRB)]]
S += [tbl(rows, [CW * 0.62, CW * 0.19, CW * 0.19], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), BLUE_L)]), Spacer(1, 2 * mm),
      P(f'Hemat {rp(normal - paket)} dibanding membeli tambahan satu per satu, dan situs langsung tayang dengan 10 artikel awal serta dirawat selama setahun.', SMALL)]

# ---- 06 Opsional & biaya berjalan ----
S += [PageBreak()] + sec('6', 'Biaya opsional dan biaya berjalan')
S += [P('Layanan tambahan (dapat dipesan kapan saja)', H2)]
rows = [head('Layanan', 'Satuan', 'Harga', align=[TA_LEFT, TA_LEFT, TA_RIGHT])]
rows += [[P(a, TC), P(b, TC), Paragraph(c, TCR)] for a, b, c in ADDONS]
S += [tbl(rows, [CW * 0.52, CW * 0.14, CW * 0.34])]
S += [P('Biaya berjalan (dibayar langsung ke penyedia, bukan ke kami)', H2)]
rows = [head('Komponen', 'Perkiraan biaya', 'Catatan')]
rows += [[P(a, TCB), P(b, TC), P(c, PS('n', fontSize=7.8, leading=10.8, textColor=MUTE))] for a, b, c in BIAYA_BERJALAN]
S += [tbl(rows, [CW * 0.27, CW * 0.31, CW * 0.42])]
S += [P('Gambaran total biaya kepemilikan', H2)]
dom = 300_000; upkeep = 500_000 * 12
rows = [head('', 'Tahun 1', 'Tahun berikutnya', align=[TA_LEFT, TA_RIGHT, TA_RIGHT])]
for nm, v in [('Paket Inti', HARGA_INTI), ('Paket Lengkap', HARGA_LENGKAP), ('Paket Lengkap+', HARGA_PLUS)]:
    rows.append([P(f'<b>{nm}</b> (+ domain ±{rp(dom)})', TC), Paragraph(rp(v + dom), TCR),
                 Paragraph(f'{rp(dom)} <font color="{hexs(MUTE)}">atau {rp(upkeep + dom)} dengan pemeliharaan</font>', TCR)])
S += [tbl(rows, [CW * 0.42, CW * 0.2, CW * 0.38]), Spacer(1, 1.5 * mm),
      P('Belum termasuk pemasangan online untuk Paket Inti dan Lengkap (Rp 1.500.000, sudah termasuk di Lengkap+). Pemeliharaan opsional; tanpa pemeliharaan, biaya tahun berikutnya hanya domain.', SMALL)]

# ---- 07 Jadwal & termin ----
S += [PageBreak()] + sec('7', 'Jadwal dan termin pembayaran')
S += [P('Jadwal perkiraan (sejak proposal disetujui)', H2), gantt(), Spacer(1, 1 * mm),
      P('Batang biru = tahap yang membutuhkan masukan MEC. Estimasi ±8 minggu sampai tayang (36 hari kerja), dengan asumsi bahan diterima pada minggu ke-2 dan umpan balik maksimal 3 hari kerja. Paket Inti lebih singkat ±1–2 minggu.', SMALL)]
S += [P('Termin pembayaran', H2)]
rows = [head('Tahap', 'Pemicu penagihan', '%', 'Paket Inti', 'Paket Lengkap', 'Paket Lengkap+', align=[TA_LEFT, TA_LEFT, TA_CENTER, TA_RIGHT, TA_RIGHT, TA_RIGHT])]
for code, pemicu, pct in TERMIN:
    rows.append([P(f'<b>{code}</b>', TCB), P(pemicu, TC), Paragraph(f'{pct}%', TCC)] + [Paragraph(rp(v * pct // 100), TCR) for v in (HARGA_INTI, HARGA_LENGKAP, HARGA_PLUS)])
rows.append([P('', TC), P('<b>Total</b>', TCB), Paragraph('<b>100%</b>', TCC)] + [Paragraph(f'<b>{rp(v)}</b>', TCRB) for v in (HARGA_INTI, HARGA_LENGKAP, HARGA_PLUS)])
S += [tbl(rows, [CW * 0.07, CW * 0.30, CW * 0.09, CW * 0.17, CW * 0.18, CW * 0.19], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), BLUE_L)]), Spacer(1, 2 * mm)]
S += [*bullets(['Jatuh tempo 7 hari sejak invoice. Pembayaran ke rekening: ' + (PENYEDIA['rekening'] or 'akan dicantumkan pada invoice') + '.',
                'Keterlambatan lebih dari 14 hari menghentikan pekerjaan sementara sampai pembayaran diterima.',
                'Domain dan sertifikat SSL dibayar langsung oleh MEC ke penyedia dan tidak ikut dipotong pajak jasa.'])]
S += [P('Pajak', H2), *bullets([
    'Penyedia jasa <b>bukan Pengusaha Kena Pajak (PKP)</b>, sehingga <b>tidak ada PPN</b> pada harga di atas.',
    'Pemesan berbadan usaha lazimnya memotong <b>PPh Pasal 23 sebesar 2%</b> dari nilai jasa (4% bila penyedia tanpa NPWP) dan menerbitkan bukti potong. Contoh: tagihan Rp 12.800.000 dipotong 2% = Rp 256.000, sehingga dibayar Rp 12.544.000.',
    'Perjanjian tertulis bernilai di atas Rp 5 juta dikenai bea meterai Rp 10.000 per dokumen (UU 10/2020), ditanggung pemesan kecuali disepakati lain.'])]

# ---- 08 Ketentuan & persetujuan ----
S += [PageBreak()] + sec('8', 'Ketentuan dan persetujuan')
terms = [
    ('Harga & masa berlaku', f'Harga dalam Rupiah dan tetap selama lingkup tidak berubah. Proposal berlaku {BERLAKU}.'),
    ('Revisi', 'Termasuk 2 putaran revisi kecil pada tahap peninjauan (teks, warna, urutan, penggantian foto). Perubahan struktur, desain ulang, atau halaman baru dianggap perubahan lingkup.'),
    ('Perubahan lingkup', f'Dikerjakan setelah ada estimasi tertulis yang disetujui; ditagih per paket tetap atau Rp {TARIF_PERUBAHAN:,.0f}/jam'.replace(',', '.') + '.'),
    ('Tanggung jawab pemesan', 'Menyediakan bahan tepat waktu, menunjuk satu penanggung jawab, dan memberi umpan balik maksimal 3 hari kerja. Keterlambatan menggeser jadwal.'),
    ('Kepemilikan', 'Setelah pelunasan, MEC memiliki situs, isi, dan kode sumber. Domain dan akun atas nama MEC sejak awal. Komponen pihak ketiga (Astro, Tailwind, font sumber terbuka, dll.) tetap tunduk pada lisensi sumber terbuka masing-masing.'),
    ('Garansi', f'Perbaikan kesalahan fungsi hasil pekerjaan ini gratis selama {GARANSI_HARI} hari sejak tayang. Tidak mencakup perubahan konten/desain atau gangguan layanan pihak ketiga.'),
    ('Kinerja & SEO', 'Target skor Lighthouse 95 ke atas diukur pada versi produksi dalam kondisi lab. Hasil di situs online dapat bervariasi menurut jaringan dan hosting. Kami tidak menjamin peringkat Google.'),
    ('Kerahasiaan', 'Informasi MEC dijaga kerahasiaannya dan tidak dipakai untuk keperluan lain.'),
    ('Pembatalan', 'Bila dibatalkan setelah pekerjaan dimulai, DP tidak dikembalikan dan pekerjaan yang sudah diserahkan ditagih sesuai tahap yang telah dicapai.'),
]
rows = [[P(f'<b>{i + 1}</b>', PS('n', fontName='Inter-B', textColor=BLUE, fontSize=9)), P(f'<b>{a}</b>', TCB), P(b, TC)] for i, (a, b) in enumerate(terms)]
S += [tbl(rows, [CW * 0.05, CW * 0.22, CW * 0.73], head=False, pad=4.2)]
S += [CondPageBreak(78 * mm), P('Persetujuan', H2), P('Dengan menandatangani di bawah ini, kedua pihak menyetujui ruang lingkup, harga, dan ketentuan pada proposal ini.', BODY), Spacer(1, 2 * mm)]
line = lambda label, val='': [P(f'<font color="{hexs(MUTE)}" size="7.6">{label}</font>', TC), P(val or '&nbsp;', TC)]
box_l = [P('<b>PEMESAN</b>', PS('bh', fontName='Inter-B', fontSize=8, textColor=BLUE)), P(KLIEN_ENTITAS, TCB), Spacer(1, 2 * mm),
         P('Paket dipilih:  ☐ Inti     ☐ Lengkap     ☐ Lengkap+'.replace('☐', '[  ]'), TC), Spacer(1, 12 * mm), P('Nama : ____________________________', TC), P('Jabatan : __________________________', TC), P('Tanggal : ___________________________', TC)]
box_r = [P('<b>PENYEDIA JASA</b>', PS('bh', fontName='Inter-B', fontSize=8, textColor=BLUE)), P(PENYEDIA['nama'] or 'Penyedia jasa pengembangan web', TCB), Spacer(1, 2 * mm),
         P(('NPWP : ' + PENYEDIA['npwp']) if PENYEDIA['npwp'] else 'NPWP : ______________________', TC), Spacer(1, 12 * mm), P('Nama : ____________________________', TC), P('Tanda tangan di atas nama jelas', SMALL), P('Tanggal : ___________________________', TC)]
sig = Table([[box_l, box_r]], colWidths=[CW / 2, CW / 2]); sig.setStyle(TableStyle([('BOX', (0, 0), (0, 0), 0.6, LINE), ('BOX', (1, 0), (1, 0), 0.6, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                                                                ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (0, 0), 10)]))
S += [KeepTogether([sig])]

# ---- Lampiran ----
S += [PageBreak(), P('LAMPIRAN', EYEBROW), P('A. Referensi pasar dan cara harga ditetapkan', H1)]
S += [P('Posisi harga terhadap kelas website di Indonesia (2026)', H2), market_bar(), Spacer(1, 2 * mm)]
S += [tbl([head('Kelas', 'Kisaran pasar', 'Cakupan umum'),
           [P('<b>Dasar</b>', TC), P('Rp 5–12 juta', TC), P('5–7 halaman, desain berbasis templat, isi dari klien', TC)],
           [P('<b>Profesional</b>', TC), P('Rp 12–35 juta', TC), P('8–15 halaman, desain semi-kustom, blog, formulir, SEO dasar, integrasi WhatsApp', TC)],
           [P('<b>Kustom / Premium</b>', TC), P('Rp 35–80 juta', TC), P('Desain orisinal, penulisan konten, multibahasa, optimasi kecepatan', TC)],
           [P('<b>Perkiraan proyek ini</b>', TCB), P(f'{rp(HARGA_INTI)} – {rp(HARGA_PLUS)}', TCB), P('44 halaman, animasi kustom, blog + SEO + pencarian, audit kualitas', TC)]],
          [CW * 0.25, CW * 0.25, CW * 0.5], extra=[('BACKGROUND', (0, 4), (-1, 4), BLUE_L)])]
S += [Spacer(1, 2 * mm), P('Sebagian penyedia menawarkan paket jauh lebih murah (Rp 0,5–3 juta), umumnya berbasis templat dengan 5 halaman dan tanpa audit kualitas. Waktu pengerjaan acuan pasar: Profesional 4–6 minggu, Kustom 6–10 minggu. '
                                    'Biaya pemeliharaan tahunan yang lazim dianggarkan 15–25% dari biaya awal.', BODY)]
S += [P('Cara harga ditetapkan', H2), *bullets([
    f'Estimasi usaha {HARI_LENGKAP:.0f} hari kerja pengembang menengah–senior × tarif ±{rp(round(DAY_RATE, -3))}/hari = {rp(HARGA_LENGKAP)}. Tarif pasar Indonesia untuk pengembang menengah sekitar Rp 150.000–400.000/jam (Rp 1,2–3,2 juta per hari kerja 8 jam); tarif efektif penawaran ini (±Rp 111.000/jam) berada di bawah rentang tersebut karena desain acuan sudah tersedia sehingga tidak ada biaya perancangan visual dari nol. Angka tarif ini indikatif (acuan yang beredar di pasar), bukan tarif baku.',
    'Paket Inti dihitung dengan mengurangi komponen yang paling mahal dan paling “mewah” (animasi, layar pembuka, alat audit). Paket Lengkap+ menambahkan layanan yang lazim dibutuhkan agar situs benar-benar hidup: pemasangan, konten awal, dan pemeliharaan.',
    'Angka pasar bersifat indikatif dan berubah menurut vendor; pengecekan ulang disarankan sebelum keputusan akhir.'])]
S += [P('Sumber referensi', H2), P('Majapahit Teknologi — Jasa Pembuatan Website Company Profile 2026 (majapahit.id) · Ascendweb — Biaya Jasa Pembuatan Website Profesional 2026 (ascendweb.id) · '
                                   'TopKarir — daftar gaji freelance web developer (topkarir.com) · Webnesia — PPh 23 atas jasa pembuatan website (webnesia.co.id) · DJP — Bea Meterai (pajak.go.id) · DDTC/Pajakku — tarif PPN 2026. '
                                   'Struktur proposal mengacu pada praktik templat web development proposal umum (mis. Prospero, Proposify, Qwilr): ringkasan, ruang lingkup, biaya per tahap, milestone, ketentuan, dan tanda tangan.', SMALL)]
S += [CondPageBreak(60 * mm), P('B. Istilah singkat', H1)]
S += [tbl([head('Istilah', 'Artinya'),
           [P('<b>SEO</b>', TC), P('Penataan situs agar mudah ditemukan di Google, misalnya lewat judul, struktur, dan artikel yang relevan.', TC)],
           [P('<b>SSL / HTTPS</b>', TC), P('Gembok keamanan di alamat situs; wajib agar situs dipercaya browser dan Google.', TC)],
           [P('<b>CMS</b>', TC), P('Editor tempat staf menulis dan menerbitkan artikel tanpa perlu menulis kode.', TC)],
           [P('<b>Lighthouse</b>', TC), P('Alat penilai dari Google untuk kecepatan, aksesibilitas, dan SEO (skor 0–100).', TC)],
           [P('<b>CLS</b>', TC), P('Ukuran seberapa banyak tampilan “melompat” saat halaman dimuat; makin kecil makin nyaman.', TC)],
           [P('<b>Staging</b>', TC), P('Salinan situs untuk ditinjau MEC sebelum dipasang resmi di internet.', TC)],
           [P('<b>PKP / PPh 23</b>', TC), P('PKP: pengusaha yang wajib memungut PPN. PPh 23: pajak penghasilan atas jasa yang dipotong oleh pemberi kerja.', TC)]],
          [CW * 0.22, CW * 0.78])]

doc.multiBuild(S)
print('OK', os.path.abspath(OUT), os.path.getsize(OUT) // 1024, 'KB', '| Inti', rp(HARGA_INTI), '| Lengkap', rp(HARGA_LENGKAP), '| Lengkap+', rp(HARGA_PLUS), '| hari', HARI_LENGKAP, '| tarif/hari', rp(round(DAY_RATE, -3)))
