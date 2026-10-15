#!/usr/bin/env python3
"""Panduan klien: mengubah kode situs MEC Academy sampai deploy (manual).

    python3 docs/proposal/make_panduan_deploy.py
Hasil: docs/Panduan-Update-Situs-MEC-Academy.pdf. Font Inter (SIL OFL). Sumber isi: docs/PANDUAN-UPDATE-KODE-DAN-DEPLOY.md
"""
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, XPreformatted

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'Panduan-Update-Situs-MEC-Academy.pdf')
for n, f in [('Inter', 'Inter.ttf'), ('Inter-SB', 'Inter-SB.ttf'), ('Inter-B', 'Inter-B.ttf')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, 'fonts', f)))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-B', italic='Inter', boldItalic='Inter-B')

GREEN = colors.HexColor('#265154'); GOLD = colors.HexColor('#B9A974'); SLATE = colors.HexColor('#334155')
MUTE = colors.HexColor('#64748B'); LINE = colors.HexColor('#DCE3EE'); BG = colors.HexColor('#F3F6F6'); WARN = colors.HexColor('#FFF6DD')
def PS(n, **k):
    d = dict(fontName='Inter', fontSize=9.2, leading=13.4, textColor=SLATE, alignment=TA_LEFT); d.update(k); return ParagraphStyle(n, **d)
BODY = PS('b'); SMALL = PS('s', fontSize=8, leading=11.5, textColor=MUTE)
TITLE = PS('t', fontName='Inter-B', fontSize=24, leading=29, textColor=GREEN)
H1 = PS('h1', fontName='Inter-B', fontSize=14, leading=18, textColor=GREEN, spaceBefore=12, spaceAfter=5)
STEP = PS('st', fontName='Inter-SB', fontSize=10, leading=14, textColor=colors.HexColor('#1B2A2C'), spaceBefore=4, spaceAfter=2)
BUL = PS('bul', leftIndent=12, bulletIndent=1, spaceAfter=2.6)
TC = PS('tc', fontSize=8.6, leading=12); TCH = PS('tch', fontName='Inter-SB', fontSize=8.4, leading=11, textColor=colors.white)
CODE = ParagraphStyle('code', fontName='Courier', fontSize=8.6, leading=12.2, textColor=colors.HexColor('#12302F'))
W, H = A4; ML = 20 * mm; CW = W - 2 * ML

def P(t, s=BODY): return Paragraph(t, s)
def bl(items): return [Paragraph(i, BUL, bulletText='•') for i in items]
def code(txt):
    t = Table([[XPreformatted(txt, CODE)]], colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BG), ('LINEBEFORE', (0, 0), (0, -1), 2.5, GOLD),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return [t, Spacer(1, 5)]
def note(txt):
    t = Table([[P(txt, TC)]], colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), WARN), ('BOX', (0, 0), (-1, -1), .6, GOLD), ('LEFTPADDING', (0, 0), (-1, -1), 9),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 9), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return [t, Spacer(1, 6)]
def table(head, rows, widths):
    t = Table([[P(h, TCH) for h in head]] + [[P(c, TC) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), GREEN), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), .4, LINE),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG]), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    return [t, Spacer(1, 6)]

s = []
s += [P('PANDUAN PENGELOLA SITUS', PS('e', fontName='Inter-SB', fontSize=8, textColor=GOLD)), Spacer(1, 4),
      P('Mengubah kode situs sampai tayang', TITLE), Spacer(1, 4),
      P('MEC Academy · malangeducationcenter.com · versi 15 Oktober 2026', SMALL), Spacer(1, 10),
      P('Alurnya enam langkah: <b>ambil kode » ubah » lihat di komputer » periksa » simpan » unggah (deploy)</b>. Setelah itu cek situs yang tayang. '
        'Sandi tidak dicantumkan di panduan ini; sandi diberikan terpisah lewat pengelola sandi.'),
      Spacer(1, 4)]
s += note('<b>Tidak perlu panduan ini</b> untuk menambah foto alumni. Foto alumni dikelola lewat halaman pengelola tersembunyi (lihat berkas <i>docs/ALUMNI-ADMIN.md</i>).')

s += [P('0. Persiapan (sekali saja)', H1)]
s += bl(['Pasang <b>Node.js 22 LTS</b> (nodejs.org) dan <b>Git</b>. Mac: <font name="Courier">brew install lftp</font>. Windows: pakai <b>WSL (Ubuntu)</b>, lalu <font name="Courier">sudo apt install lftp</font>. Skrip deploy memakai <b>lftp</b>.',
         'Ambil kode dari repositori, lalu pasang kebutuhan:'])
s += code('git clone &lt;alamat-repositori&gt; mec-academy\ncd mec-academy\nnpm install')
s += bl(['Buat berkas <b>.env.deploy</b> di folder utama. Berkas ini tidak ikut git dan <b>tidak boleh dibagikan</b>:'])
s += code('FTP_HOST=gede.iixcp.rumahweb.net\nFTP_USER=&lt;akun FTP deploy&gt;\nFTP_PASS=&lt;sandi akun FTP&gt;')
s += [P('Akun FTP dibuat di cPanel Rumahweb (menu Akun FTP, dibatasi ke folder <i>public_html</i>). Rincian: <i>docs/CICD.md</i>.', SMALL)]

s += [P('1. Setiap kali mengubah', H1)]
s += code('git pull                       # ambil versi terbaru\ngit checkout -b perubahan-baru  # cabang kerja (disarankan)\nnpm run dev                    # lihat di http://localhost:4321')
s += [P('Setiap berkas disimpan, tampilan di browser langsung ikut berubah. Ubah <b>satu hal per kali</b>.')]
s += [Spacer(1, 4), P('Di mana mengubah apa', STEP)]
s += table(['Yang ingin diubah', 'Berkas'], [
    ['Nomor WA, email, alamat, jam buka, medsos, deskripsi situs', '<font name="Courier">src/lib/site.ts</font>'],
    ['Isi beranda (12 bab)', '<font name="Courier">src/pages/index.astro</font>'],
    ['Halaman lain (Tentang, Kontak, Fasilitas, dan seterusnya)', '<font name="Courier">src/pages/…</font>'],
    ['Artikel blog', '<font name="Courier">src/content/articles/*.mdx</font>. Salin artikel lama sebagai contoh; isi title, description, publishedAt, category, cover'],
    ['Gambar', '<font name="Courier">src/assets/images/</font> (JPG/PNG, idealnya di bawah 500 KB)'],
    ['Warna, jarak, tampilan', '<font name="Courier">src/styles/global.css</font>'],
    ['Alamat lama / redirect, cache', '<font name="Courier">public/.htaccess</font>. <b>Jangan hapus blok PHP handler cPanel.</b>'],
], [CW * .46, CW * .54])

s += [P('2. Periksa sebelum tayang', H1)]
s += code('npm run check     # cek kesalahan penulisan\nnpm test          # uji otomatis (harus lulus semua)\nnpm run build     # membuat folder dist/ (harus tanpa error)\nnpm run preview   # lihat hasil build di http://localhost:4321')
s += note('Kalau ada yang merah, <b>jangan deploy</b>. Baca pesan error (biasanya menyebut nama berkas dan baris), perbaiki, ulangi.')

s += [P('3. Simpan perubahan (commit)', H1)]
s += code('git add -A\ngit commit -m "Ubah nomor WA dan jam buka"\ngit push -u origin perubahan-baru')
s += [P('Gabungkan ke cabang utama <b>main</b> lewat Pull Request di GitHub, lalu di komputer: <font name="Courier">git checkout main &amp;&amp; git pull</font>. '
        'Yang di-deploy adalah <b>isi komputer Anda</b>, jadi pastikan sedang berada di <b>main</b> yang sudah mutakhir sebelum langkah 4.')]

s += [P('4. Deploy (unggah ke Rumahweb)', H1)]
s += code('npm run deploy               # cek, uji, build, lalu unggah lewat FTPS\nDRY_RUN=1 npm run deploy      # latihan: tidak ada yang diunggah')
s += [P('Berkas yang <b>dihapus</b> dari kode tidak otomatis hilang di server (disengaja agar folder <i>alumni-foto/</i> aman). '
        'Untuk menghapus halaman lama, hapus lewat cPanel File Manager.')]

s += [P('5. Cek hasilnya', H1)]
s += bl(['Buka malangeducationcenter.com dan segarkan keras (<b>Ctrl+Shift+R</b>, di Mac <b>Cmd+Shift+R</b>).',
         'Cek halaman yang diubah, tombol WhatsApp, dan satu halaman lain, di HP dan laptop.',
         'Belum berubah? Tunggu 1 sampai 2 menit (cache) atau coba jendela penyamaran.'])

s += [P('6. Kalau ada masalah', H1)]
s += table(['Gejala', 'Tindakan'], [
    ['<font name="Courier">lftp: command not found</font>', 'Pasang lftp (langkah 0).'],
    ['Login FTP gagal', 'Cek <i>.env.deploy</i> (host, user, sandi). Sandi bisa diganti di cPanel.'],
    ['Situs error / halaman putih setelah deploy', 'Kembali ke versi sebelumnya: <font name="Courier">git checkout &lt;commit-lama&gt;</font> lalu <font name="Courier">npm run deploy</font> (lihat <i>docs/RUNBOOK-ROLLBACK.md</i>).'],
    ['Halaman <i>/kelola-foto/</i> error 500', 'Pastikan PHP <b>8.3</b> di cPanel (MultiPHP Manager).'],
    ['Ragu atau buntu', 'Berhenti, jangan deploy, hubungi pengembang.'],
], [CW * .38, CW * .62])

s += [P('Aturan aman', H1)]
s += bl(['Jangan commit <i>.env.deploy</i>, sandi, atau data pribadi ke GitHub.',
         'Pastikan <b>build berhasil</b> sebelum deploy; satu perubahan, satu deploy.',
         'Simpan cadangan: folder <i>alumni-foto/</i> dan salinan <i>dist/</i> terakhir.',
         'Aktifkan 2FA di Rumahweb, GitHub, dan Google; ganti sandi bila ada staf keluar.'])

def footer(c, d):
    c.saveState(); c.setFont('Inter', 7.5); c.setFillColor(MUTE)
    c.drawString(ML, 12 * mm, 'MEC Academy · Panduan pengelola situs'); c.drawRightString(W - ML, 12 * mm, f'Halaman {d.page}')
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(ML, H - 12 * mm, ML + 26 * mm, H - 12 * mm); c.restoreState()
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=ML, topMargin=17 * mm, bottomMargin=17 * mm,
                      title='Panduan Pengelola Situs MEC Academy', author='Achmad Hanim')
doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(ML, 17 * mm, CW, H - 34 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer)])
doc.build(s)
print('OK', OUT)
