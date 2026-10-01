#!/usr/bin/env python3
"""Proposal Paket Ringkas (anggaran < Rp 10 juta, ±2 minggu) — MEC Academy. DRAFT.

    python3 docs/proposal/make_proposal_ringkas.py
Hasil: docs/Proposal-Website-MEC-Academy-Paket-Ringkas.pdf
Semua total dihitung dari data (ada assert). Font Inter (SIL OFL) di docs/proposal/fonts/.
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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'Proposal-Website-MEC-Academy-Paket-Ringkas.pdf')
# ============================== KONFIGURASI ==============================
NO_PROPOSAL = '002/PRP/X/2026'
TANGGAL = '1 Oktober 2026'
BERLAKU = '14 hari sejak tanggal proposal'
KLIEN = 'MEC Academy'
KLIEN_ENTITAS = 'CV MEC Academy'
KLIEN_ALAMAT = 'Jl. Jatisari No. 07, Patuksari, Desa Plaosan, Kec. Wonosari, Kab. Malang, Jawa Timur'
PENYEDIA = {'nama': 'Achmad Hanim', 'npwp': '', 'rekening': 'BCA 4400198034 a/n Achmad Hanim'}
TARIF_PERUBAHAN = 150_000
GARANSI_HARI = 14
TERMIN = [('T1', 'Persetujuan proposal & mulai pekerjaan', 50), ('T2', 'Serah terima & tayang', 50)]

# (kode, pekerjaan & hasil, hari, biaya)
ITEMS = [
    ('A', 'Persiapan & pemindahan isi dari desain contoh', 'Foto diubah ke format ringan, font, dan seluruh teks dipindahkan; struktur proyek disiapkan.', 1.0, 900_000),
    ('B', 'Landing page & dashboard (beranda)', 'Layar pembuka “klik untuk mulai” dan beranda 12 bagian sesuai desain: tata letak, warna, huruf, dan isi.', 3.0, 2_700_000),
    ('C', 'Animasi sesuai desain', 'Animasi gulir, zoom foto utama, daftar yang bergeser, dan tab mesin, dibuat ringan agar tetap lancar di HP.', 2.0, 1_800_000),
    ('D', 'Dialog / modal isi', '16 modul pelatihan, profil instruktur, fasilitas + galeri, tahapan seleksi, FAQ, dan kontak dalam bentuk dialog, seperti pada desain contoh.', 2.0, 1_800_000),
    ('E', 'Tampilan HP, tablet & laptop', 'Penyesuaian ukuran layar dan pengujian di perangkat umum.', 1.0, 900_000),
    ('F', 'Kecepatan & SEO dasar', 'Judul, deskripsi, tampilan saat dibagikan (WhatsApp/sosmed), sitemap, dan optimasi gambar.', 0.5, 450_000),
    ('G', 'Pemasangan & serah terima', 'Pemasangan di hosting & domain milik MEC, uji akhir, panduan singkat, dan serah terima file.', 0.5, 450_000),
]
HARGA = sum(i[4] for i in ITEMS); HARI = sum(i[3] for i in ITEMS)
assert HARGA == 9_000_000 and HARI == 10.0 and HARGA < 10_000_000
assert sum(t[2] for t in TERMIN) == 100
rp = lambda n: 'Rp ' + f'{n:,.0f}'.replace(',', '.')
ADDONS = [
    ('Analitik dasar: Google Analytics 4 + Search Console', 'Sekali', 'Rp 1.000.000'),
    ('Formulir pendaftaran online (ke WhatsApp/email)', 'Sekali', 'Rp 2.500.000'),
    ('Pemeliharaan bulanan (perbaikan kecil, cadangan)', 'Per bulan', 'Rp 500.000'),
    ('Sesi pelatihan tambahan (2 jam)', 'Per sesi', 'Rp 500.000'),
    ('Pekerjaan di luar lingkup', 'Per jam', rp(TARIF_PERUBAHAN)),
]


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


def gantt():
    rows = [('Kickoff & persiapan', 0, 1), ('Landing & beranda', 1, 4), ('Animasi', 4, 6), ('Dialog / modal isi', 6, 8),
            ('Responsif, SEO, pengujian', 8, 9.5), ('MEC meninjau & revisi kecil', 7, 10), ('Pemasangan & serah terima', 9.5, 10)]
    lw = 135; nd = 10; cw_ = (CW - lw) / nd; rh = 18
    d = Drawing(CW, rh * (len(rows) + 1) + 6); top = rh * len(rows) + 4
    for w in range(nd):
        d.add(Rect(lw + w * cw_, 0, cw_ - 1, rh * len(rows) + 2, fillColor=BG if (w // 5) % 2 == 0 else WHITE, strokeColor=None))
        d.add(String(lw + w * cw_ + cw_ / 2, top + 5, f'H{w + 1}', fontName='Inter-SB', fontSize=7, fillColor=MUTE, textAnchor='middle'))
    for i, (lab, a, b) in enumerate(rows):
        y = rh * (len(rows) - 1 - i) + 3
        d.add(String(0, y + 5, lab, fontName='Inter', fontSize=7.9, fillColor=SLATE))
        d.add(Rect(lw + a * cw_, y + 2, max((b - a) * cw_, 6), 10, rx=3, ry=3, fillColor=BLUE if i == 5 else NAVY, strokeColor=None))
    return d

def bar():
    d = Drawing(CW, 40); x = 0; pal = ['#0B1F3A', '#2557D6', '#4F7DE8', '#7EA1F0', '#A9C0F5', '#E8A317', '#8FA3BF']
    for i, it in enumerate(ITEMS):
        w = CW * it[4] / HARGA
        d.add(Rect(x, 14, w - 1.5, 20, fillColor=colors.HexColor(pal[i]), strokeColor=None))
        d.add(String(x + 4, 20, f'{it[0]}', fontName='Inter-SB', fontSize=7.6, fillColor=WHITE if i < 4 or i == 6 else NAVY)); x += w
    return d

# ------------------------------ DOKUMEN -----------------------------------
class Doc(BaseDocTemplate):
    pass

def cover(c, d):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H * 0.36, W, H * 0.64, stroke=0, fill=1)
    c.setFillColor(NAVY2)
    for r, a in [(150, .5), (105, .5), (62, .5)]:
        c.setStrokeColor(NAVY2); c.setLineWidth(1); c.circle(W - 40 * mm, H - 48 * mm, r, stroke=1, fill=0)
    c.setFillColor(BLUE); c.rect(ML, H - 46 * mm, 22 * mm, 1.6 * mm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#9DB4E8')); c.setFont('Inter-SB', 8.5); c.drawString(ML, H - 36 * mm, 'PROPOSAL PENGEMBANGAN WEBSITE · PAKET RINGKAS')
    c.setFillColor(WHITE); c.setFont('Inter-B', 36); c.drawString(ML, H - 68 * mm, 'Website')
    c.drawString(ML, H - 83 * mm, KLIEN)
    c.setFont('Inter', 12.5); c.setFillColor(colors.HexColor('#C7D4EA'))
    c.drawString(ML, H - 100 * mm, 'Satu halaman sesuai desain, di bawah Rp 10 juta,')
    c.drawString(ML, H - 107 * mm, 'selesai sekitar dua minggu')
    # meta
    y0 = H * 0.36 - 16 * mm
    rows = [('Disiapkan untuk', f'{KLIEN_ENTITAS}\n{KLIEN_ALAMAT}'), ('Disiapkan oleh', PENYEDIA['nama']),
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
          title=f'Proposal Website {KLIEN} — Paket Ringkas', author=PENYEDIA['nama'], subject='Proposal website (draft)')
frame = Frame(ML, 22 * mm, CW, H - 46 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
cframe = Frame(ML, 20 * mm, CW, 10 * mm, id='c')
doc.addPageTemplates([PageTemplate(id='cover', frames=[cframe], onPage=cover), PageTemplate(id='body', frames=[frame], onPage=body_page)])
S = [NextPageTemplate('body'), PageBreak()]
def sec(num, title): return [P(f'BAGIAN {num}', EYEBROW), P(title, H1)]

# ---- 1 Ringkasan ----
S += sec('1', 'Ringkasan')
S += [P(f'{KLIEN} memerlukan website yang menampilkan program <b>Basic Mechanic Course (BMC)</b> persis seperti desain contoh yang sudah disiapkan. '
        'Proposal ini menawarkan versi yang fokus: <b>hanya yang ada di desain</b>, tanpa fitur tambahan, dengan harga di bawah Rp 10 juta dan waktu sekitar dua minggu.', LEAD), Spacer(1, 4 * mm)]
S += [kpi([('Rp 9 jt', 'harga tetap, seluruh pekerjaan'), ('±2 minggu', '10 hari kerja sejak bahan lengkap'), ('1 + dialog', 'satu halaman, detail dalam dialog'), ('2 × revisi', 'revisi kecil sebelum serah terima')]), Spacer(1, 4 * mm)]
S += [callout('<b>Prinsipnya sederhana:</b> yang Anda lihat di desain contoh adalah yang Anda terima. Hal-hal yang tidak ada di desain, seperti blog, halaman terpisah untuk setiap modul, atau pencarian, tidak termasuk di paket ini (lihat Bagian 5).', 'info')]
S += [P('Yang Anda dapatkan', H2), *bullets([
    '<b>Layar pembuka</b> “klik untuk mulai” dan <b>beranda 12 bagian</b> sesuai desain.',
    '<b>Animasi</b> utama seperti di desain, dibuat ringan agar nyaman di HP.',
    '<b>16 modul pelatihan</b>, profil instruktur, fasilitas + galeri, tahapan seleksi, FAQ, dan kontak, semuanya dalam <b>dialog</b> seperti desain contoh.',
    '<b>Tampilan HP, tablet, dan laptop</b>, serta pengaturan dasar agar mudah dibagikan dan ditemukan.',
    '<b>Dipasang di hosting dan domain MEC</b> yang sudah ada, ditambah panduan singkat dan serah terima file.'])]

# ---- 2 Ruang lingkup ----
S += [PageBreak()] + sec('2', 'Ruang lingkup')
inc = [P('<b>Termasuk</b>', TCB)] + bullets([
    'Satu halaman web dengan layar pembuka dan 12 bagian beranda',
    'Animasi gulir, zoom foto utama, daftar bergeser, tab mesin',
    'Dialog untuk 16 modul, instruktur, fasilitas/galeri, tahapan, FAQ, kontak',
    'Tampilan responsif (HP, tablet, laptop)',
    'Optimasi gambar dan SEO dasar untuk satu halaman',
    'Pemasangan di hosting MEC dan panduan singkat',
    'Dua putaran revisi kecil; garansi perbaikan 14 hari'])
exc = [P('<b>Tidak termasuk</b>', TCB)] + bullets([
    'Blog/artikel dan halaman terpisah per modul atau instruktur',
    'Pencarian, CMS, formulir pendaftaran, bahasa Inggris',
    'Penulisan teks, foto, atau video baru',
    'Logo atau identitas visual baru',
    'Analitik, pelacakan, dan skrip audit otomatis',
    'Biaya perpanjangan domain/hosting MEC',
    'Jaminan peringkat Google'])
t = Table([[inc, exc]], colWidths=[CW * 0.53, CW * 0.47]); t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOX', (0, 0), (-1, -1), 0.5, LINE), ('LINEAFTER', (0, 0), (0, -1), 0.5, LINE), ('BACKGROUND', (1, 0), (1, 0), BG),
                                                                              ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
S += [t, P('Asumsi', H2), *bullets([
    f'{KLIEN} menyerahkan bahan (foto asli, teks modul, profil instruktur, kontak) <b>paling lambat hari ke-2</b>; keterlambatan menggeser jadwal.',
    'Satu penanggung jawab dari MEC memberi umpan balik maksimal 2 hari kerja.',
    'MEC memberi akses ke hosting/domain yang sudah ada. Hosting perlu mendukung situs statis (HTML) dan SSL.',
    'Foto memakai resolusi yang tersedia; foto yang kecil akan terlihat kurang tajam di layar besar.',
    'Penambahan bagian, halaman, atau fitur di luar desain contoh dihitung terpisah.'])]

# ---- 3 Rincian biaya ----
S += [PageBreak()] + sec('3', f'Rincian biaya ({rp(HARGA)})')
S += [P(f'Setiap pekerjaan dirinci menurut hasil kerjanya. Usaha ditampilkan sebagai transparansi; harga yang mengikat adalah harga tetap {rp(HARGA)}.')]
rows = [head('Kode', 'Pekerjaan dan hasil yang diserahkan', 'Usaha', 'Biaya', align=[TA_LEFT, TA_LEFT, TA_RIGHT, TA_RIGHT])]
for code, nm, desc, hari, biaya in ITEMS:
    rows.append([P(f'<b>{code}</b>', TCB), [P(f'<b>{nm}</b>', TCB), P(desc, PS('d', fontSize=7.9, leading=11, textColor=MUTE))], Paragraph(f'{hari:.1f} hr'.replace('.', ','), TCR), Paragraph(rp(biaya), TCR)])
rows.append([P('', TC), Paragraph('<b>TOTAL</b>', PS('tt', fontName='Inter-B', fontSize=9, textColor=WHITE)), Paragraph(f'<b>{HARI:.1f} hr</b>'.replace('.', ','), PS('tt2', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_RIGHT)),
             Paragraph(f'<b>{rp(HARGA)}</b>', PS('tt3', fontName='Inter-B', fontSize=9, textColor=WHITE, alignment=TA_RIGHT))])
S += [Spacer(1, 2 * mm), tbl(rows, [CW * 0.08, CW * 0.62, CW * 0.11, CW * 0.19], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), NAVY)], pad=4.5)]
S += [P('Ke mana uang dialokasikan', H2), bar(), Spacer(1, 1 * mm),
      P(f'Bobot terbesar ada pada <b>landing + beranda ({round(100 * ITEMS[1][4] / HARGA)}%)</b>, <b>animasi ({round(100 * ITEMS[2][4] / HARGA)}%)</b>, dan <b>dialog ({round(100 * ITEMS[3][4] / HARGA)}%)</b>: tiga hal yang membentuk tampilan sesuai desain. '
        f'Rata-rata ±{rp(HARGA / HARI)} per hari kerja.', BODY)]

# ---- 4 Jadwal, termin, pajak ----
S += [PageBreak()] + sec('4', 'Jadwal dan pembayaran')
S += [P('Jadwal (hari kerja sejak proposal disetujui dan bahan diterima)', H2), gantt(), Spacer(1, 1 * mm),
      P(f'Batang biru = tahap yang membutuhkan masukan MEC. Total 10 hari kerja (±2 minggu), diikuti garansi perbaikan {GARANSI_HARI} hari.', SMALL)]
S += [P('Termin pembayaran', H2)]
rows = [head('Tahap', 'Pemicu penagihan', '%', 'Jumlah', align=[TA_LEFT, TA_LEFT, TA_CENTER, TA_RIGHT])]
for code, pemicu, pct in TERMIN: rows.append([P(f'<b>{code}</b>', TCB), P(pemicu, TC), Paragraph(f'{pct}%', TCC), Paragraph(rp(HARGA * pct // 100), TCR)])
rows.append([P('', TC), P('<b>Total</b>', TCB), Paragraph('<b>100%</b>', TCC), Paragraph(f'<b>{rp(HARGA)}</b>', TCRB)])
S += [tbl(rows, [CW * 0.1, CW * 0.55, CW * 0.1, CW * 0.25], extra=[('BACKGROUND', (0, len(rows) - 1), (-1, len(rows) - 1), BLUE_L)]), Spacer(1, 2 * mm)]
S += [*bullets([f'Jatuh tempo 7 hari sejak invoice. Pembayaran ke rekening: {PENYEDIA["rekening"]}.',
                'Perpanjangan domain dan hosting tetap dibayar MEC langsung ke penyedianya, di luar tagihan ini.'])]
S += [P('Pajak', H2), *bullets([
    'Penyedia jasa <b>bukan PKP</b>, sehingga <b>tidak ada PPN</b>.',
    'Pemesan berbadan usaha lazimnya memotong <b>PPh Pasal 23</b> (2% dari nilai jasa; <b>4% bila penyedia tanpa NPWP aktif</b>) dan menerbitkan bukti potong. Pada paket ini 4% setara ' + rp(HARGA * 4 // 100) + ' dari total.',
    'Perjanjian tertulis di atas Rp 5 juta dikenai bea meterai Rp 10.000 per dokumen, ditanggung pemesan kecuali disepakati lain.'])]

# ---- 5 Batasan & peningkatan ----
S += [PageBreak()] + sec('5', 'Yang perlu diketahui dan pilihan peningkatan')
S += [P('Karena seluruh isi berada dalam satu halaman dan dialog, ada konsekuensi yang kami sampaikan di awal agar tidak ada kejutan:')]
rows = [head('Hal', 'Dampak pada paket ini'),
        [P('<b>Pencarian Google</b>', TC), P('Google melihat satu halaman. Modul dan instruktur tidak muncul sebagai hasil pencarian tersendiri. Cocok untuk kartu nama digital, pameran, dan dibagikan lewat WhatsApp; kurang untuk menjaring pengunjung dari Google.', TC)],
        [P('<b>Blog / artikel</b>', TC), P('Tidak tersedia. Artikel membutuhkan halaman tersendiri.', TC)],
        [P('<b>Tautan langsung</b>', TC), P('Membagikan satu modul tertentu tidak otomatis. Pengunjung membuka beranda lalu dialognya.', TC)],
        [P('<b>Mesin pencari AI</b>', TC), P('Sama seperti Google: isi detail dalam dialog sulit dikutip sebagai sumber tersendiri.', TC)],
        [P('<b>Perawatan isi</b>', TC), P('Perubahan teks dilakukan lewat file kode (kami bantu; lihat tarif di Layanan tambahan). Belum ada editor untuk staf.', TC)]]
S += [tbl(rows, [CW * 0.22, CW * 0.78])]
S += [P('Bila kebutuhan bertambah', H2), P('Paket ini dapat ditingkatkan kapan saja menjadi situs multi-halaman dengan blog dan SEO penuh. Pekerjaan yang sudah jadi (tampilan, animasi, isi) dipakai ulang, sehingga yang dibayar hanya tambahannya. Estimasi dan harga diberikan terpisah setelah kebutuhan dikonfirmasi.', BODY)]

# ---- 6 Add-on ----
S += [P('Layanan tambahan (opsional)', H2)]
rows = [head('Layanan', 'Satuan', 'Harga', align=[TA_LEFT, TA_LEFT, TA_RIGHT])] + [[P(a, TC), P(b, TC), Paragraph(c, TCR)] for a, b, c in ADDONS]
S += [tbl(rows, [CW * 0.58, CW * 0.14, CW * 0.28])]

# ---- 7 Ketentuan ----
S += [PageBreak()] + sec('6', 'Ketentuan dan persetujuan')
terms = [('Harga & masa berlaku', f'Harga dalam Rupiah dan tetap selama lingkup tidak berubah. Proposal berlaku {BERLAKU}.'),
         ('Revisi', 'Dua putaran revisi kecil (teks, warna, urutan, penggantian foto). Perubahan struktur atau tambahan bagian dianggap perubahan lingkup.'),
         ('Perubahan lingkup', f'Dikerjakan setelah ada estimasi tertulis yang disetujui, atau dengan tarif Rp {TARIF_PERUBAHAN:,.0f}/jam.'.replace(',', '.')),
         ('Tanggung jawab pemesan', 'Menyediakan bahan tepat waktu dan memberi umpan balik maksimal 2 hari kerja. Keterlambatan menggeser jadwal.'),
         ('Kepemilikan', 'Setelah pelunasan, MEC memiliki situs, isi, dan kode sumber. Komponen pihak ketiga (font, pustaka) tunduk pada lisensi sumber terbukanya.'),
         ('Garansi', f'Perbaikan kesalahan fungsi hasil pekerjaan ini gratis selama {GARANSI_HARI} hari sejak tayang; tidak mencakup perubahan konten/desain atau gangguan layanan pihak ketiga.'),
         ('Kerahasiaan', 'Informasi MEC dijaga kerahasiaannya dan tidak dipakai untuk keperluan lain.'),
         ('Pembatalan', 'Bila dibatalkan setelah pekerjaan dimulai, DP tidak dikembalikan dan pekerjaan yang sudah diserahkan ditagih sesuai tahap yang dicapai.')]
rows = [[P(f'<b>{i + 1}</b>', PS('n', fontName='Inter-B', textColor=BLUE, fontSize=9)), P(f'<b>{a}</b>', TCB), P(b, TC)] for i, (a, b) in enumerate(terms)]
S += [tbl(rows, [CW * 0.05, CW * 0.22, CW * 0.73], head=False, pad=4.2)]
S += [Spacer(1, 6 * mm), P('Persetujuan', H2), P('Dengan menandatangani di bawah ini, kedua pihak menyetujui ruang lingkup, harga, dan ketentuan pada proposal ini.', BODY), Spacer(1, 2 * mm)]
box_l = [P('<b>PEMESAN</b>', PS('bh', fontName='Inter-B', fontSize=8, textColor=BLUE)), P(KLIEN_ENTITAS, TCB), Spacer(1, 16 * mm), P('Nama : ____________________________', TC), P('Jabatan : __________________________', TC), P('Tanggal : ___________________________', TC)]
box_r = [P('<b>PENYEDIA JASA</b>', PS('bh', fontName='Inter-B', fontSize=8, textColor=BLUE)), P(PENYEDIA['nama'], TCB), Spacer(1, 16 * mm), P('Nama : ' + PENYEDIA['nama'], TC), P('Rekening : ' + PENYEDIA['rekening'], TC), P('Tanggal : ___________________________', TC)]
sig = Table([[box_l, box_r]], colWidths=[CW / 2, CW / 2]); sig.setStyle(TableStyle([('BOX', (0, 0), (0, 0), 0.6, LINE), ('BOX', (1, 0), (1, 0), 0.6, LINE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                                                                ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
S += [KeepTogether([sig])]
doc.build(S)
print('OK', os.path.abspath(OUT), os.path.getsize(OUT) // 1024, 'KB |', rp(HARGA), '|', HARI, 'hari')
