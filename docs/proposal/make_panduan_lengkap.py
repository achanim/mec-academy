#!/usr/bin/env python3
"""Panduan lengkap pengelola website MEC Academy untuk pengguna awam (pasang di komputer, ubah isi, tayang lewat cPanel).

    python3 docs/proposal/make_panduan_lengkap.py
Hasil: docs/Panduan-Pengelola-Website-MEC-Academy.pdf. Font Inter (SIL OFL) di docs/proposal/fonts/.
"""
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether,
                                XPreformatted, PageBreak, CondPageBreak, NextPageTemplate, Flowable)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'Panduan-Pengelola-Website-MEC-Academy.pdf')
for n, f in [('Inter', 'Inter.ttf'), ('Inter-SB', 'Inter-SB.ttf'), ('Inter-B', 'Inter-B.ttf')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, 'fonts', f)))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-B', italic='Inter', boldItalic='Inter-B')

GREEN = colors.HexColor('#265154'); DEEP = colors.HexColor('#061F23'); GOLD = colors.HexColor('#B9A974'); INK = colors.HexColor('#1B2A2C')
SLATE = colors.HexColor('#334155'); MUTE = colors.HexColor('#64748B'); LINE = colors.HexColor('#DCE3EE'); BG = colors.HexColor('#F3F6F6')
WARN = colors.HexColor('#FFF4D6'); WARNB = colors.HexColor('#E0B84A'); TIP = colors.HexColor('#E6F3EE'); TIPB = colors.HexColor('#4C9A7C')
STOP = colors.HexColor('#FDE8E6'); STOPB = colors.HexColor('#D2574B'); WHITE = colors.white

def PS(n, **k):
    d = dict(fontName='Inter', fontSize=10, leading=15, textColor=SLATE, alignment=TA_LEFT); d.update(k); return ParagraphStyle(n, **d)
BODY = PS('b'); SMALL = PS('s', fontSize=8.4, leading=12, textColor=MUTE)
H1 = PS('h1', fontName='Inter-B', fontSize=20, leading=25, textColor=GREEN, spaceBefore=0, spaceAfter=6)
H2 = PS('h2', fontName='Inter-B', fontSize=13, leading=17, textColor=GREEN, spaceBefore=14, spaceAfter=5)
H3 = PS('h3', fontName='Inter-SB', fontSize=10.6, leading=14.5, textColor=INK, spaceBefore=8, spaceAfter=3)
EB = PS('eb', fontName='Inter-SB', fontSize=8, leading=11, textColor=GOLD, spaceAfter=3)
BUL = PS('bul', leftIndent=13, bulletIndent=2, spaceAfter=3)
TC = PS('tc', fontSize=9, leading=12.6); TCH = PS('tch', fontName='Inter-SB', fontSize=8.8, leading=12, textColor=WHITE)
CODE = ParagraphStyle('code', fontName='Courier-Bold', fontSize=9.2, leading=13, textColor=colors.HexColor('#10302F'))
W, H = A4; ML = 20 * mm; CW = W - 2 * ML
C = lambda t: f'<font name="Courier-Bold" color="#10302F">{t}</font>'   # teks yang diketik / nama berkas

def P(t, s=BODY): return Paragraph(t, s)
def bl(items): return [Paragraph(i, BUL, bulletText='•') for i in items]

class Num(Flowable):
    """Lingkaran bernomor di samping judul langkah."""
    def __init__(self, n, d=16): super().__init__(); self.n = str(n); self.d = d; self.width = d; self.height = d
    def draw(self):
        c = self.canv; c.setFillColor(GREEN); c.circle(self.d / 2, self.d / 2, self.d / 2, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont('Inter-B', 8.6); c.drawCentredString(self.d / 2, self.d / 2 - 3.1, self.n)

def step(n, title, *body):
    """Satu langkah: lingkaran nomor + judul tebal, lalu isi."""
    head = Table([[Num(n), P(f'<b>{title}</b>', PS('st', fontName='Inter-SB', fontSize=10.8, leading=14.5, textColor=INK))]],
                 colWidths=[9 * mm, CW - 9 * mm])
    head.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 2), ('TOPPADDING', (0, 0), (-1, -1), 0)]))
    inner = Table([[list(body)]], colWidths=[CW - 9 * mm]); inner.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    outer = Table([['', inner]], colWidths=[9 * mm, CW - 9 * mm])
    outer.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                               ('LINEBEFORE', (1, 0), (1, 0), 0, WHITE)]))
    return [KeepTogether([head, outer]), Spacer(1, 5)]

def box(kind, title, text, w=None):
    bg, bd, lab = {'tip': (TIP, TIPB, 'TIPS'), 'warn': (WARN, WARNB, 'PERHATIAN'), 'stop': (STOP, STOPB, 'JANGAN')}[kind]
    t = Table([[P(f'<font size="7.6" color="{bd.hexval().replace("0x", "#")}"><b>{lab}</b></font><br/><b>{title}</b><br/>{text}', TC)]], colWidths=[w or CW])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LINEBEFORE', (0, 0), (0, -1), 3, bd), ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    return [t, Spacer(1, 7)]

def box9(kind, title, text): return box(kind, title, text, CW - 9 * mm)

def code(txt, w=None):
    t = Table([[XPreformatted(txt, CODE)]], colWidths=[w or CW - 9 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BG), ('LINEBEFORE', (0, 0), (0, -1), 2.5, GOLD), ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return [t, Spacer(1, 5)]

def table(head, rows, widths, w=None):
    tw = w or CW
    t = Table([[P(h, TCH) for h in head]] + [[P(c, TC) for c in r] for r in rows], colWidths=[tw * x for x in widths], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), GREEN), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), .4, LINE),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, BG]), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    return [t, Spacer(1, 7)]

def chapter(no, title, sub):
    return [PageBreak(), P(f'BAB {no}', EB), P(title, H1), P(sub, PS('sub', fontSize=10.4, leading=15.5, textColor=MUTE, spaceAfter=10))]

import json, re
def _slug(t): return re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', t.lower().replace('&', 'dan')))
_mods = json.load(open(os.path.join(HERE, '..', '..', 'src', 'data', 'content.json'), encoding='utf8'))['modules']
_cells = [(C(_slug(m)), m) for m in _mods]
_half = (len(_cells) + 1) // 2
MODUL_ROWS = [[_cells[i][1], _cells[i][0]] + ([_cells[i + _half][1], _cells[i + _half][0]] if i + _half < len(_cells) else ['', '']) for i in range(_half)]
s = []
# ---------------------------------------------------------------- SAMPUL (digambar di onFirstPage)
s += [Spacer(1, 150 * mm), NextPageTemplate('main'), PageBreak()]

# ---------------------------------------------------------------- BAB 1
s += [P('BAB 1', EB), P('Sebelum mulai: gambaran besar', H1),
      P('Panduan ini untuk Anda yang <b>belum pernah menulis kode sama sekali</b>. Semua langkah ditulis berurutan, cukup diikuti satu per satu. '
        'Tidak ada yang perlu dihafal. Kalau ragu, berhenti, baca bagian <b>Bab 6 (masalah umum)</b>, atau hubungi pengembang.'),
      P('Tiga tahap yang akan Anda lakukan', H2)]
s += table(['Tahap', 'Apa yang dilakukan', 'Seberapa sering'], [
    ['<b>A. Siapkan komputer</b> (Bab 2)', 'Memasang program yang dibutuhkan dan menyalin folder website dari flashdisk.', '<b>Sekali saja</b>'],
    ['<b>B. Ubah isi website</b> (Bab 3 dan 4)', 'Menjalankan website di komputer, lalu mengganti teks atau gambar dan melihat hasilnya.', 'Setiap kali ada perubahan'],
    ['<b>C. Tayangkan</b> (Bab 5)', 'Membuat berkas hasil (folder dist), dibungkus zip, diunggah ke hosting, lalu diekstrak.', 'Setiap kali ingin perubahan terlihat di internet'],
], [.28, .50, .22])
s += [P('<b>Penting:</b> mengubah teks di komputer <b>tidak</b> langsung mengubah website yang tayang. Website baru berubah setelah tahap C (unggah). Jadi Anda bebas mencoba di komputer tanpa takut merusak website asli.', BODY)]
s += [P('Istilah yang akan sering muncul', H2)]
s += table(['Istilah', 'Artinya (versi sederhana)'], [
    ['<b>Folder proyek</b>', 'Folder bernama <i>mec-academy</i> berisi seluruh bahan website. Ini yang Anda terima lewat flashdisk.'],
    ['<b>Node.js</b>', 'Program gratis yang dibutuhkan untuk menjalankan dan "membungkus" website. Dipasang sekali, setelah itu tidak perlu disentuh.'],
    ['<b>VS Code</b>', 'Aplikasi untuk membuka dan mengedit berkas website (seperti Word, tapi untuk berkas website).'],
    ['<b>Terminal</b>', 'Jendela tempat mengetik perintah singkat. Anda hanya perlu menyalin-tempel beberapa perintah dari panduan ini.'],
    ['<b>Build dan dist</b>', 'Build = proses mengubah bahan website menjadi berkas siap tayang. Hasilnya masuk ke folder <i>dist</i>, yang diunggah ke hosting.'],
    ['<b>cPanel</b>', 'Halaman pengelola hosting (Rumahweb). Di sana Anda mengunggah berkas website.'],
    ['<b>public_html</b>', 'Folder di hosting tempat website tayang. Semua berkas website harus berada di sini.'],
], [.24, .76])
s += [P('Yang perlu disiapkan', H2),
      P('Komputer Windows 10/11 (catatan Mac disertakan), <b>koneksi internet</b>, ruang kosong sekitar 1 GB, flashdisk berisi folder <i>mec-academy</i> dari pengembang, dan nama pengguna serta kata sandi <b>cPanel Rumahweb</b> (diberikan terpisah oleh pemilik). Tahap A butuh sekitar 30 menit.')]

# ---------------------------------------------------------------- BAB 2
s += chapter(2, 'Menyiapkan komputer (sekali saja)', 'Pasang dua program gratis, satu plugin, lalu salin folder website. Setelah bab ini selesai, Anda tidak perlu mengulanginya.')
s += step(1, 'Pasang Node.js', 
          P('Buka <b>nodejs.org</b> di browser. Klik tombol hijau <b>"Download Node.js (LTS)"</b>. Pastikan nomor versinya <b>22 atau lebih tinggi</b> (misalnya 22.x atau 24.x). Buka berkas yang terunduh, lalu klik <b>Next</b> sampai selesai dan <b>Install</b>. Semua pilihan boleh dibiarkan bawaan.'),
          P('<b>Cek berhasil atau belum:</b> setelah langkah 6 nanti, ketik perintah di bawah. Kalau muncul nomor versi, berarti berhasil.'),
          *code('node -v'), P('Hasilnya misalnya ' + C('v22.12.0') + ' atau lebih tinggi. Kalau tertulis versi di bawah 22, pasang ulang dari nodejs.org.', SMALL))
s += step(2, 'Pasang Visual Studio Code (VS Code)',
          P('Buka <b>code.visualstudio.com</b>, klik <b>Download</b>, jalankan berkas yang terunduh. Saat ada pilihan, centang <b>"Add to PATH"</b> dan <b>"Register Code as an editor for supported file types"</b> (kalau muncul), lalu <b>Next</b> dan <b>Install</b>.'),
          P('<b>Mac:</b> buka berkas unduhan, seret ikon VS Code ke folder Applications. Untuk Node.js di Mac, pakai penginstal .pkg dari nodejs.org.', SMALL))
s += step(3, 'Pasang plugin (extension) VS Code',
          P('Buka VS Code. Di bilah kiri klik ikon <b>kotak-kotak</b> (Extensions), atau tekan ' + C('Ctrl+Shift+X') + '. Ketik nama plugin di kotak pencarian, klik <b>Install</b> pada hasil yang benar (penerbit tertulis di bawah nama).'),
          *table(['Plugin', 'Ketik di pencarian', 'Fungsi', 'Wajib?'], [
              ['<b>Astro</b>', 'Astro (penerbit: Astro)', 'Mewarnai dan merapikan berkas website agar mudah dibaca.', '<b>Ya</b>'],
              ['<b>Indonesian Language Pack</b>', 'Indonesian Language Pack (penerbit: Microsoft)', 'Menu VS Code berbahasa Indonesia. Setelah dipasang, klik "Change Language and Restart".', 'Disarankan'],
              ['<b>Tailwind CSS IntelliSense</b>', 'Tailwind CSS IntelliSense', 'Membantu bila suatu saat mengubah tampilan.', 'Opsional'],
          ], [.22, .26, .36, .16], w=CW - 9 * mm))
s += step(4, 'Salin folder website dari flashdisk ke komputer',
          P('Colokkan flashdisk. Buka <b>File Explorer</b> (Windows) lalu salin folder <b>mec-academy</b> ke tempat yang mudah, misalnya <b>drive C:</b> sehingga alamatnya menjadi ' + C('C:\\mec-academy') + '. Cara menyalin: klik kanan folder &gt; <b>Copy</b>, buka drive C:, klik kanan area kosong &gt; <b>Paste</b>.'),
          P('Kalau berkasnya berupa <b>.zip</b>: klik kanan &gt; <b>Extract All</b> &gt; pilih drive C: &gt; <b>Extract</b>.'),
          *box9('warn', 'Salin ke komputer, jangan dijalankan langsung dari flashdisk', 'Menjalankan website langsung dari flashdisk lambat dan sering gagal. Hindari juga folder OneDrive (Desktop/Documents).'),
          P('<b>Cek folder sudah benar (penting):</b> buka folder <i>mec-academy</i>. Di dalamnya harus <b>langsung</b> terlihat berkas ' + C('package.json') + ' dan folder <i>src</i> dan <i>public</i>. Kalau yang terlihat hanya <b>satu folder lagi bernama mec-academy</b> (folder berlapis, ini sering terjadi saat Extract All), buka folder dalam itu. <b>Folder yang berisi package.json itulah folder proyek</b>, dan hanya folder itu yang boleh dibuka di VS Code.'))
s += step(5, 'Buka folder website di VS Code',
          P('Di VS Code klik menu <b>File &gt; Open Folder...</b> (Buka Folder). Pilih folder yang <b>berisi package.json</b> (misalnya <i>C:\\mec-academy</i>), klik <b>Select Folder</b>. Nama folder itu akan tampil di judul VS Code. Jika muncul pertanyaan <b>"Do you trust the authors?"</b>, klik <b>"Yes, I trust the authors"</b>.'),
          P('Di bilah kiri harus terlihat daftar <i>public</i>, <i>src</i>, <i>package.json</i>, dan seterusnya (bagian ini disebut <b>Explorer</b>). Kalau yang terlihat hanya satu folder <i>mec-academy</i> lagi, berarti folder yang dibuka salah: tutup folder (File &gt; Close Folder) dan buka folder dalamnya.'))
s += step(6, 'Buka Terminal di VS Code',
          P('Klik menu <b>Terminal &gt; New Terminal</b>. Sebuah panel akan terbuka di bagian bawah. Di situlah perintah diketik. Anda hanya perlu <b>menyalin perintah, menempelkannya dengan klik kanan, lalu menekan Enter</b>.'),
          *box9('warn', 'Kalau muncul tulisan "running scripts is disabled" (merah)', 'Ini hal umum di Windows. Di panel Terminal klik tanda panah kecil <b>&#9662;</b> di sebelah tombol <b>+</b>, pilih <b>Command Prompt</b>, lalu ulangi perintahnya di jendela baru itu. Jangan ubah pengaturan lain.'))
s += step(7, 'Pasang bahan-bahan website (npm install)',
          P('Di Terminal ketik perintah berikut lalu Enter. Butuh internet dan sekitar 1 sampai 3 menit. <b>Cukup sekali.</b>'),
          *code('npm install'),
          P('Kalau langsung muncul tulisan merah <b>ENOENT ... package.json</b>, Terminal terbuka di folder yang salah. Lihat Bab 6, baris pertama.', SMALL),
          P('Selama berjalan akan muncul banyak tulisan, termasuk tulisan kuning <i>"npm warn"</i> atau <i>"deprecated"</i>. <b>Itu normal</b>, abaikan. Selesai bila kursor kembali dan muncul tulisan seperti ' + C('added 296 packages') + '. Sebuah folder baru bernama <i>node_modules</i> akan muncul di Explorer. Jangan diubah atau dihapus.'))
s += [P('Apakah ada pengaturan lain (env) yang dibutuhkan?', H2),
      P('<b>Tidak ada.</b> Website ini tidak memakai database, kata sandi, atau berkas pengaturan rahasia (.env).')]
s += [P('Cukup <b>Node.js 22+</b>, <b>VS Code + plugin Astro</b>, <b>folder proyek</b>, dan <b>node_modules</b> (dibuat otomatis oleh langkah 7). <b>Tidak perlu</b> database, API key, atau berkas .env.')]

# ---------------------------------------------------------------- BAB 3
s += chapter(3, 'Menjalankan website di komputer', 'Cara melihat website di komputer Anda sendiri sebelum diunggah ke internet. Lakukan setiap kali mulai bekerja.')
s += step(1, 'Jalankan',
          P('Pastikan VS Code terbuka di folder proyek, lalu buka Terminal (' + C('Terminal &gt; New Terminal') + ') dan ketik:'),
          *code('npm run dev'),
          P('Tunggu beberapa detik sampai muncul tulisan seperti berikut:'),
          *code('  Local    http://localhost:4321/'))
s += step(2, 'Buka di browser',
          P('Buka Chrome atau Edge, ketik di kolom alamat ' + C('localhost:4321') + ' lalu Enter. Website MEC Academy tampil. Ini <b>hanya terlihat di komputer Anda</b>, bukan di internet.'),
          P('Tidak ada tampilan? Cek apakah Terminal masih menampilkan tulisan <i>Local</i> di atas. Kalau ada alamat lain (misalnya ' + C('localhost:4322') + '), pakai alamat itu.', SMALL))
s += step(3, 'Biarkan terbuka sambil mengubah isi',
          P('Selama Terminal berjalan, <b>setiap kali Anda menyimpan berkas</b> (' + C('Ctrl+S') + '), halaman di browser berubah sendiri dalam beberapa detik. Kalau tidak berubah, tekan ' + C('F5') + '.'))
s += step(4, 'Berhenti',
          P('Klik di panel Terminal, lalu tekan ' + C('Ctrl+C') + '. Kalau ditanya "Terminate batch job (Y/N)?" ketik ' + C('Y') + ' lalu Enter. Tutup VS Code seperti biasa. Esok harinya cukup ulangi dari langkah 1 (tidak perlu npm install lagi).'))
s += box('tip', 'Bekerja dengan aman', 'Sebelum mulai mengubah, <b>salin seluruh folder mec-academy</b> dan beri nama baru, misalnya <i>mec-academy-cadangan</i>. Kalau ada yang berantakan, hapus folder yang rusak dan salin lagi dari cadangan. Setiap perubahan juga bisa dibatalkan dengan ' + C('Ctrl+Z') + '.')

# ---------------------------------------------------------------- BAB 4
s += chapter(4, 'Mengubah isi website', 'Contoh perubahan paling sederhana: teks, nomor kontak, tautan, dan gambar. Setiap contoh menyebut berkas mana yang dibuka dan bagian mana yang diubah.')
s += [P('Aturan emas', H2)]
s += bl(['Ubah <b>hanya tulisan yang terlihat</b> di antara tanda kutip ' + C('" "') + ' atau ' + C("' '") + ', atau di antara tanda &gt; dan &lt;.',
         '<b>Jangan menghapus</b> tanda aneh di sekitar teks: ' + C('&lt; &gt; { } " \' ,') + ' dan tulisan seperti ' + C('class="..."') + '.',
         'Ubah satu hal, simpan (' + C('Ctrl+S') + '), lihat browser. Kalau aman, lanjutkan ke perubahan berikutnya.',
         'Kalau tampilan jadi error (halaman merah), tekan ' + C('Ctrl+Z') + ' di berkas itu sampai kembali normal.'])
s += [P('Cara cepat menemukan teks di seluruh website', H2),
      P('Tidak perlu tahu teks itu ada di berkas mana. Di VS Code tekan ' + C('Ctrl+Shift+F') + ' (Pencarian), ketik <b>sebagian teks yang terlihat di website</b> (misalnya <i>Jadi mekanik</i>), lalu Enter. Daftar berkas yang memuat teks itu muncul. <b>Klik salah satu hasil</b>, berkas terbuka dan teksnya tersorot. Ubah, lalu simpan.'),
      P('Mau mengganti satu tulisan di <b>banyak tempat sekaligus</b> (misalnya alamat Instagram)? Tekan ' + C('Ctrl+Shift+H') + ', isi kotak atas dengan teks lama dan kotak bawah dengan teks baru, lalu klik ikon <b>"Replace All"</b> (dua panah) di sebelah kotak bawah.')]
s += box('warn', 'Kalau pencarian "tidak menemukan" tulisan yang jelas-jelas terlihat', 'Ada dua penyebab umum. <b>(1)</b> Anda memakai ' + C('Ctrl+F') + ' (hanya mencari di satu berkas yang sedang dibuka). Pakai ' + C('Ctrl+Shift+F') + ' untuk mencari di seluruh website. <b>(2)</b> Satu kalimat di website bisa <b>tersusun dari dua tempat</b>, misalnya "MEC Academy, " ada di satu berkas dan "Lembaga Pendidikan dan Pelatihan..." ada di berkas lain. Mencari kalimat utuh tidak ketemu. Carilah <b>potongan pendek</b> saja, misalnya ' + C('Lembaga Pendidikan') + ', lalu lihat semua hasilnya.')
s += [CondPageBreak(60 * mm), P('Contoh 1: ganti judul besar di beranda', H2)]
s += [P('Buka ' + C('src/pages/index.astro') + ' (Explorer: klik <i>src</i>, lalu <i>pages</i>, lalu <i>index.astro</i>). Cari baris ini (' + C('Ctrl+F') + ' lalu ketik <i>Jadi mekanik</i>):'),
      *code('Mulai langkahmu.&lt;br /&gt;Jadi mekanik&lt;br /&gt;&lt;em&gt;alat berat.&lt;/em&gt;', CW),
      P('Artinya: ' + C('&lt;br /&gt;') + ' = pindah baris, ' + C('&lt;em&gt;...&lt;/em&gt;') + ' = bagian yang berwarna emas. Ubah hanya kata-katanya, misalnya:'),
      *code('Mulai langkahmu hari ini.&lt;br /&gt;Jadi mekanik&lt;br /&gt;&lt;em&gt;alat berat.&lt;/em&gt;', CW)]
s += [CondPageBreak(90 * mm), P('Contoh 2: pindah baris (Enter), ukuran, warna, dan tebal tulisan', H2),
      P('Menekan <b>Enter</b> di berkas website <b>tidak</b> membuat baris baru di tampilan. Itu hanya merapikan kode. Untuk pindah baris di halaman, tulis ' + C('&lt;br /&gt;') + ' di tempat yang diinginkan. Contoh di beranda, kalimat di bawah judul besar:'),
      *code('&lt;p class="hero-hook"&gt;MEC Academy, {content.institution}&lt;/p&gt;', CW),
      P('Tulisan ' + C('{content.institution}') + ' berarti "isi tulisan <i>Lembaga Pendidikan dan Pelatihan Keterampilan Teknik Alat Berat</i> yang diambil dari berkas ' + C('src/data/content.json') + '". <b>Jangan dihapus tanda kurung kurawalnya.</b> Agar tulisannya turun ke baris kedua, sisipkan ' + C('&lt;br /&gt;') + ' sebelum tulisan itu:'),
      *code('&lt;p class="hero-hook"&gt;MEC Academy,&lt;br /&gt;{content.institution}&lt;/p&gt;', CW),
      P('Hasilnya: baris pertama <b>MEC Academy,</b> dan baris kedua <b>Lembaga Pendidikan dan Pelatihan Keterampilan Teknik Alat Berat</b>. Catatan: ' + C('&lt;br /&gt;') + ' hanya berfungsi di berkas halaman (.astro). Di dalam ' + C('content.json') + ' tidak berfungsi.'),
      P('Mengubah ukuran, warna, dan tebal tulisan', H3),
      P('Tambahkan atribut ' + C('style="..."') + ' di dalam tanda pembuka, setelah ' + C('class="..."') + ', <b>dipisah spasi</b>. Setiap pengaturan diakhiri titik koma:'),
      *code('&lt;p class="hero-hook" style="font-size:22px; color:#cdbe86; font-weight:700;"&gt;', CW),
      *table(['Ingin mengubah', 'Tulis', 'Contoh'], [
          ['Ukuran huruf', C('font-size:...px;'), C('font-size:22px;') + ' (lebih besar = angka lebih besar)'],
          ['Warna huruf', C('color:#......;'), C('color:#cdbe86;') + ' (emas)'],
          ['Tebal atau tipis', C('font-weight:...;'), C('font-weight:700;') + ' tebal, ' + C('400') + ' normal'],
          ['Jarak antarbaris', C('line-height:...;'), C('line-height:1.6;')],
          ['Jarak antarhuruf', C('letter-spacing:...px;'), C('letter-spacing:1px;')],
          ['Lebar blok teks', C('max-width:...px;'), C('max-width:600px;') + ' (tulisan turun lebih cepat)'],
          ['Jarak ke atas', C('margin-top:...px;'), C('margin-top:16px;')],
      ], [.26, .30, .44]),
      P('Warna yang dipakai website ini (latar website gelap, jadi untuk tulisan pilih warna terang):', H3),
      *table(['Nama', 'Kode warna', 'Cocok untuk'], [
          ['Emas', C('#cdbe86'), 'Penekanan, kata kunci'],
          ['Krem terang', C('#f3f0e4'), 'Tulisan utama di latar gelap'],
          ['Hijau abu muda', C('#c0cbc0'), 'Tulisan pendukung'],
          ['Hijau tua', C('#265154'), 'Tulisan di latar terang (krem)'],
          ['Hijau sangat tua', C('#061f23'), 'Tulisan di latar terang atau tombol emas'],
      ], [.26, .24, .50]),
      *box('warn', 'Satu tanda, satu style', 'Jika tanda yang Anda ubah <b>sudah punya</b> ' + C('style="..."') + ', jangan buat yang kedua. Tambahkan pengaturan baru <b>di dalam</b> tanda kutip yang sama. Angka ukuran dan warna berlaku sama di komputer dan HP, jadi cek hasilnya juga lewat HP sebelum tayang.')]
s += [CondPageBreak(70 * mm), P('Contoh 3: ganti nomor WhatsApp, email, dan alamat', H2),
      P('Buka ' + C('src/data/content.json') + ' lalu cari tulisan ' + C('"contact"') + ' (' + C('Ctrl+F') + ').'),
      *code('"phone": "+62 822 2998 5588",\n"whatsapp": "https://wa.me/6282229985588",\n"email": "malangeducationcenter@gmail.com",\n"address": "Jl. Jatisari No. 07, ...",', CW),
      *table(['Baris', 'Cara mengisi'], [
          ['<b>phone</b>', 'Nomor yang tampil di website. Bebas ditulis dengan spasi.'],
          ['<b>whatsapp</b>', 'Format <b>https://wa.me/</b> diikuti nomor <b>tanpa +, tanpa spasi, tanpa 0 di depan</b>, diawali 62. Contoh nomor 0812 3456 7890 menjadi ' + C('https://wa.me/6281234567890') + '.'],
          ['<b>email</b>, <b>address</b>', 'Ganti isi di antara tanda kutip.'],
      ], [.22, .78]),
      *box9('warn', 'Tanda kutip dan koma harus tetap ada', 'Setiap baris diakhiri koma (kecuali baris terakhir dalam kelompoknya) dan teksnya dibungkus tanda kutip. Kalau terhapus, website akan menampilkan layar error. Cukup ' + C('Ctrl+Z') + ' untuk membatalkan.')]
s += [CondPageBreak(70 * mm), P('Contoh 4: ganti tautan formulir pendaftaran, media sosial, dan jam buka', H2),
      P('Buka ' + C('src/lib/site.ts') + '. Di bagian atas ada daftar yang mudah dibaca:'),
      *code("registerFormUrl: 'https://forms.gle/...',     &lt;- tautan formulir pendaftaran\ninstagramUrl: 'https://www.instagram.com/...',\ntiktokUrl: 'https://www.tiktok.com/@...',\nhoursLabel: 'Senin–Jumat, 08.00–16.00 WIB',", CW),
      P('Ganti hanya alamat atau tulisan di antara tanda kutip tunggal. Alamat media sosial muncul <b>dua kali</b> di berkas yang sama (satu di ' + C('instagramUrl') + ', satu lagi di daftar ' + C('social') + '). Cara paling aman: gunakan <b>Ctrl+Shift+H (Replace All)</b> dengan alamat lama dan alamat baru, supaya semuanya berganti sekaligus.')]
s += [CondPageBreak(75 * mm), P('Contoh 5: ganti gambar', H2),
      P('Semua foto website ada di folder ' + C('src/assets/images') + '. Cara paling mudah dan aman: <b>ganti berkas dengan nama dan format yang sama persis.</b>'),
      *bl(['Siapkan foto baru. Pilih foto <b>mendatar</b> (lebar lebih besar dari tinggi), lebar minimal 1600 piksel, ukuran sebaiknya di bawah 1 MB. Untuk mengecilkan ukuran gratis, buka <b>squoosh.app</b>, seret foto, atur kualitas sekitar 80, lalu simpan.',
            'Ubah nama foto baru menjadi <b>sama persis</b> dengan foto lama, misalnya ' + C('hero.jpg') + ' (huruf kecil, ekstensi .jpg).',
            'Di File Explorer, buka <i>mec-academy &gt; src &gt; assets &gt; images</i>. Salin foto baru ke situ, saat ditanya pilih <b>"Replace the file in the destination"</b>.',
            'Lihat browser. Gambar berubah otomatis.']),
      *box9('tip', 'Pastikan ekstensi benar', 'Di File Explorer buka <b>View &gt; Show &gt; File name extensions</b> supaya terlihat ".jpg". Kesalahan umum: nama menjadi ' + C('hero.jpg.jpg') + ' atau ' + C('Hero.JPG') + '. Foto instruktur berformat <b>.webp</b>, jadi gantinya juga harus .webp (ubah format di squoosh.app dengan memilih "WebP").'),
      P('Daftar foto yang paling sering diganti:', H3),
      *table(['Nama berkas', 'Dipakai di'], [
          [C('hero.jpg'), 'Foto cadangan di latar bagian paling atas beranda (tampil sebelum video berjalan, atau jika video tidak bisa diputar)'],
          [C('building.jpg'), 'Foto gedung MEC Academy'],
          [C('film.jpg'), 'Latar bagian company profile di beranda'],
          [C('alumni.jpg') + ', ' + C('alumni2.jpg') + ', ' + C('alumni-ojt1.jpg') + ' sampai ' + C('alumni-ojt5.jpg'), 'Foto bab alumni dan OJT'],
          [C('classroom.jpg') + ', ' + C('practice.jpg') + ', ' + C('ojt.jpg') + ', ' + C('workshop.jpg') + ', ' + C('engine.jpg'), 'Foto tahapan belajar dan praktik'],
          [C('gallery-01.jpg') + ' sampai ' + C('gallery-20.jpg'), 'Galeri fasilitas dan kegiatan'],
          [C('trainer-nama.webp'), 'Foto masing-masing instruktur (format .webp)'],
      ], [.46, .54])]
s += [CondPageBreak(95 * mm), P('Contoh 6: foto berbeda untuk setiap halaman modul', H2),
      P('Setiap halaman modul punya <b>foto header</b> (latar bagian atas). Modul yang belum diatur memakai foto bawaan yang sama (' + C('workshop.jpg') + '), sehingga semua terlihat sama. <b>Jangan mengganti workshop.jpg</b> untuk ini, karena foto itu dipakai di banyak tempat. Aturlah per modul lewat berkas ' + C('src/data/module-images.ts') + ':'),
      *bl(['Siapkan foto (mendatar, lebar minimal 1600 piksel, di bawah 1 MB). Beri nama sesuai modul, misalnya ' + C('modul-basic-safety.jpg') + ', lalu salin ke ' + C('src/assets/images') + '.',
            'Buka ' + C('src/data/module-images.ts') + '. Di dalam tanda kurung kurawal ada contoh yang diawali ' + C('//') + '. Hapus ' + C('//') + ' di depannya lalu sesuaikan, atau tambahkan baris seperti ini:']),
      *code("'basic-safety': {\n  image: 'modul-basic-safety',\n  alt: 'Siswa MEC mempelajari keselamatan kerja',\n},", CW),
      *bl(['<b>Kata pertama</b> (' + C("'basic-safety'") + ') adalah kode alamat modul, dilihat di tabel di bawah. <b>image</b> = nama foto tanpa .jpg. <b>alt</b> = deskripsi singkat foto (untuk pembaca layar dan Google). Setiap baris diakhiri koma.',
            'Simpan, lalu buka alamat modulnya, misalnya ' + C('localhost:4321/program/basic-mechanic-course/modul/basic-safety/') + '.']),
      *table(['Modul', 'Kode alamat', 'Modul', 'Kode alamat'], MODUL_ROWS, [.26, .24, .26, .24]),
      *box('tip', 'Apakah akan muncul foto kedua di bawah, seperti modul Diesel Engine?', '<b>Tidak.</b> Mengisi <i>module-images.ts</i> hanya mengganti foto <b>header</b> (latar atas). Foto kedua di bagian "Tentang modul ini" hanya ada pada <b>empat modul sistem</b> (Diesel Engine, Hydraulic System, Torqflow Drive System, Electrical System). Fotonya diatur di ' + C('src/data/systems.ts') + ' (baris <i>image</i>), dan juga dipakai di bagian "Jelajahi sistem" di beranda. Mengubah baris <i>image</i> di sana mengganti foto kedua dan foto di beranda sekaligus.')]
s += [CondPageBreak(95 * mm), P('Contoh 7: tambah atau hapus instruktur', H2),
      P('Data instruktur ada di ' + C('src/data/content.json') + '. Cari tulisan ' + C('"instructors"') + '. Setiap instruktur adalah satu <b>blok</b> dari ' + C('{') + ' sampai ' + C('}') + ':'),
      *code('{\n  "name": "Moh. Andy Prastyawan",\n  "asset": "trainer-andy",\n  "role": "Mekanik",\n  "company": "PT Pama Persada Nusantara",\n  "credentials": ["BNSP ToT Level IV", "Asesor Kompetensi"]\n},', CW),
      P('<b>Menambah:</b>', H3),
      *bl(['Siapkan foto potret tegak (wajah di tengah atas, latar polos lebih baik), sekitar 800 x 1000 piksel. Beri nama ' + C('trainer-namabaru.jpg') + ' (atau .webp) dan salin ke ' + C('src/assets/images') + '.',
            'Di ' + C('content.json') + ', <b>salin satu blok utuh</b> (dari { sampai } termasuk koma di akhir), tempel tepat di bawahnya, lalu ubah isinya. Isian <b>asset</b> = nama foto <b>tanpa</b> ekstensi (' + C('trainer-namabaru') + '). <b>credentials</b> adalah daftar, dipisah koma, tiap item dalam tanda kutip. Bila ada angka ' + C('"page": 6') + ', boleh dibiarkan (tidak dipakai).',
            'Simpan. Kartu instruktur baru otomatis muncul di <b>beranda</b> (bab instruktur) dan halaman <b>Instruktur</b>, dan halaman profilnya otomatis dibuat di ' + C('/instruktur/nama-instruktur/') + '. Cek tampilan beranda, karena jumlah kartu mempengaruhi tata letak.']),
      P('<b>Menghapus:</b> hapus satu blok utuh dari { sampai } (dan koma setelahnya). Foto boleh dibiarkan. Halaman profilnya otomatis hilang. Pastikan antarblok tetap dipisah koma, dan <b>blok paling akhir tidak memakai koma</b>.', BODY)]
s += [CondPageBreak(95 * mm), P('Contoh 8: tambah atau hapus foto kegiatan dan galeri', H2),
      P('Ada dua daftar foto kegiatan, masing-masing punya berkas data sendiri:', BODY),
      *table(['Tampil di', 'Data', 'Folder foto', 'Isi satu blok'], [
          ['Halaman <b>Industri</b> (Kegiatan industri) dan tiga kartu di <b>beranda</b>', C('src/data/content.json') + ' bagian ' + C('"events"'), C('src/assets/images'), C('name') + ', ' + C('company') + ', ' + C('asset') + ' (nama foto tanpa .jpg)'],
          ['Halaman <b>Fasilitas</b> (Galeri kegiatan, bisa diperbesar)', C('src/data/gallery.json'), C('src/assets/images'), C('name') + ', ' + C('caption') + ' (tulisan di bawah foto), ' + C('asset')],
      ], [.25, .27, .22, .26]),
      P('<b>Menambah kegiatan industri:</b>', H3),
      *code('{\n  "name": "Kunjungan industri ke MEC",\n  "company": "PT Nama Perusahaan",\n  "asset": "event-baru"\n},', CW),
      *bl(['Salin foto (mendatar, lebar 1600 piksel atau lebih) ke ' + C('src/assets/images') + ' dengan nama ' + C('event-baru.jpg') + '.',
            'Di ' + C('content.json') + ' bagian ' + C('"events"') + ', salin satu blok, tempel, lalu ubah isinya. Halaman <b>Industri</b> menampilkan semua kegiatan otomatis, dan daftar nama perusahaan di beranda ikut bertambah.',
            '<b>Beranda hanya menampilkan 3 kartu.</b> Pilihannya ada di ' + C('src/pages/index.astro') + ', baris yang diawali ' + C("const events = ['event-komatsu', 'event-sinarindo', 'event-ppa']") + '. Ganti salah satu nama dengan nama foto kegiatan baru (tanpa .jpg).']),
      P('<b>Menambah foto galeri:</b> salin foto dengan nama berurutan, misalnya ' + C('gallery-21.jpg') + ', lalu di ' + C('gallery.json') + ' salin satu blok dan ubah <b>caption</b> dan <b>asset</b> (' + C('gallery-21') + '). Foto baru otomatis muncul di halaman Fasilitas.', BODY),
      P('<b>Menghapus foto:</b> hapus <b>blok</b>-nya dari berkas data (dari { sampai }). Aman. Jangan menghapus <b>berkas fotonya</b> kecuali Anda yakin: beberapa foto dipakai juga di tempat lain di beranda (misalnya ' + C('gallery-01') + ' dan ' + C('gallery-02') + '). Kalau sesudah menghapus foto muncul pesan ' + C('Image not found: nama') + ' saat build, kembalikan foto bernama itu.', BODY),
      *box('tip', 'Foto alumni berbeda', 'Foto di halaman <b>Alumni</b> tidak diatur dari kode. Admin MEC mengunggahnya lewat halaman pengelola foto tersembunyi di <i>malangeducationcenter.com/kelola-foto/</i> (perlu kata sandi dari pemilik), tanpa membuka VS Code.')]
s += [CondPageBreak(45 * mm), P('Contoh 9: menu di bagian atas (termasuk "Learning")', H2),
      P('Menu atas dan menu layar penuh ada di ' + C('src/components/Header.astro') + ', dalam dua daftar (' + C('nav') + ' dan ' + C('menuItems') + '). Satu menu = satu baris. Menu <b>Learning</b> mengarah ke portal e-learning, alamatnya diatur di satu tempat: ' + C('src/lib/site.ts') + ' baris ' + C('learningUrl') + '. Untuk mengganti tujuannya cukup ubah alamat itu. Untuk <b>menghapus</b> menu Learning, hapus dua baris yang berisi ' + C('site.learningUrl') + ' di ' + C('Header.astro') + '.'),
      P('Menu baru ditambah dengan menyalin satu baris di setiap daftar: ' + C("['/alamat/', 'Nama menu'],") + ' (di daftar kedua ada tambahan tulisan deskripsi). Alamat internal dimulai garis miring, alamat luar dimulai ' + C('https://') + ' dan otomatis dibuka di tab baru.')]
s += [CondPageBreak(38 * mm), P('Contoh 10: ganti video di bagian atas beranda', H2),
      P('Video latar dan tombol "Tonton company profile" memakai kode video YouTube. Kode video adalah bagian setelah ' + C('v=') + ' di alamat video, misalnya ' + C('https://www.youtube.com/watch?v=ZV39to3Qfz8') + ' memiliki kode ' + C('ZV39to3Qfz8') + '. Tekan ' + C('Ctrl+Shift+H') + ', isi kode lama dan kode baru, lalu <b>Replace All</b>. Pastikan video di YouTube diizinkan untuk disematkan (embed).')]
s += box('stop', 'Hindari hal berikut', '<b>Jangan</b> menghapus atau mengganti nama folder <i>src</i>, <i>public</i>, <i>node_modules</i>, atau berkas <i>package.json</i> dan <i>astro.config.mjs</i>. <b>Jangan</b> mengetik di berkas yang tidak dikenal. Bila ragu, tanyakan ke pengembang sebelum mengubah.')

# ---------------------------------------------------------------- BAB 5
s += chapter(5, 'Menayangkan perubahan ke internet', 'Setelah puas dengan tampilan di komputer: buat folder dist, bungkus menjadi zip, unggah ke cPanel, lalu ekstrak.')
s += [P('Tahap 1: membuat berkas siap tayang (build)', H2)]
s += step(1, 'Hentikan website lokal bila masih berjalan', P('Klik panel Terminal lalu tekan ' + C('Ctrl+C') + ' (jawab Y bila ditanya).'))
s += step(2, 'Jalankan build',
          P('Di Terminal ketik lalu Enter. Butuh sekitar 10 sampai 30 detik.'), *code('npm run build'),
          P('Berhasil bila di akhir tertulis ' + C('Complete!') + ' dan muncul folder <b>dist</b> di Explorer. Jika ada tulisan <b>error</b> berwarna merah, jangan lanjut. Batalkan perubahan terakhir (' + C('Ctrl+Z') + ') lalu ulangi, atau lihat Bab 6.'))
s += step(3, 'Lihat hasil build sebelum diunggah (disarankan)',
          *code('npm run preview'), P('Buka ' + C('localhost:4321') + ', periksa halaman yang Anda ubah, lalu hentikan dengan ' + C('Ctrl+C') + '.'))
s += [CondPageBreak(60 * mm), P('Tahap 2: membuat zip dari isi folder dist', H2)]
s += step(4, 'Tampilkan berkas tersembunyi',
          P('Di dalam folder <i>dist</i> ada berkas penting bernama ' + C('.htaccess') + ' (titik di depan, <b>tersembunyi</b>). Berkas ini wajib ikut. Di File Explorer buka folder <i>mec-academy &gt; dist</i>, klik <b>View &gt; Show &gt; Hidden items</b> (Windows 11) atau centang <b>Hidden items</b> (Windows 10). Berkas ' + C('.htaccess') + ' akan terlihat agak pudar.'),
          P('<b>Mac:</b> di Finder tekan ' + C('Cmd+Shift+.') + ' untuk menampilkan berkas tersembunyi.', SMALL))
s += step(5, 'Pilih semua isi dist lalu jadikan zip',
          P('Di dalam folder <i>dist</i> (jangan di luarnya!) tekan ' + C('Ctrl+A') + ' untuk memilih semua. Klik kanan pada salah satu berkas yang terpilih, lalu <b>Compress to ZIP file</b> (Windows 11) atau <b>Send to &gt; Compressed (zipped) folder</b> (Windows 10). Beri nama ' + C('update-web.zip') + '.'),
          P('Pindahkan zip itu ke tempat yang mudah dicari, misalnya <b>Desktop</b>. <b>Mac:</b> pilih semua isi dist, klik kanan &gt; <b>Compress</b>.', SMALL),
          *box9('warn', 'Yang di-zip adalah ISI dist, bukan folder dist-nya', 'Cek dulu: klik dua kali zip yang jadi. Yang terlihat pertama haruslah ' + C('index.html') + ', folder <i>_astro</i>, <i>artikel</i>, dan seterusnya, <b>bukan</b> satu folder bernama dist. Berkas ' + C('.htaccess') + ' juga harus ada di situ.'))
s += [CondPageBreak(70 * mm), P('Tahap 3: unggah dan ekstrak di cPanel', H2)]
s += step(6, 'Masuk ke cPanel',
          P('Buka <b>new.clientzone.rumahweb.com</b> dan login dengan akun Rumahweb milik MEC. Pilih layanan <b>Hosting</b> yang dipakai website, lalu klik <b>Login cPanel</b>. (Atau buka alamat cPanel yang diberikan pemilik.) Di halaman cPanel, cari dan klik <b>File Manager</b>.'))
s += step(7, 'Buka folder public_html dan tampilkan berkas tersembunyi',
          P('Di panel kiri File Manager, klik <b>public_html</b>. Klik tombol <b>Settings</b> (kanan atas), centang <b>"Show Hidden Files (dotfiles)"</b>, lalu <b>Save</b>. Anda akan melihat isi website yang sedang tayang (index.html, folder artikel, alumni-foto, dan lain-lain).'))
s += step(8, 'Cadangkan dulu (disarankan)',
          P('Klik <b>Select All</b>, lalu <b>Compress</b> di bar atas, pilih <b>Zip Archive</b>, beri nama ' + C('cadangan-TANGGAL.zip') + ' (misalnya cadangan-2026-10-30.zip), klik <b>Compress File(s)</b>. Setelah jadi, klik kanan zip itu &gt; <b>Download</b> untuk menyimpannya di komputer, lalu hapus zip dari server. Kalau ada masalah, cadangan inilah penyelamat.'))
s += step(9, 'Unggah zip',
          P('Klik <b>Upload</b> di bar atas. Di halaman baru, seret berkas ' + C('update-web.zip') + ' ke kotak (atau klik <b>Select File</b>). Tunggu bar hijau mencapai <b>100%</b>. Batas ukuran unggah cukup besar, jadi tidak perlu dipecah. Setelah selesai, klik <b>Go Back to ...public_html</b> di bagian bawah.'))
s += step(10, 'Ekstrak di public_html',
          P('Kembali di File Manager folder <i>public_html</i>: klik <b>sekali</b> pada ' + C('update-web.zip') + ', lalu klik <b>Extract</b> di bar atas (atau klik kanan &gt; Extract). Di jendela yang muncul, pastikan kolom tujuan berisi ' + C('/public_html') + ', klik <b>Extract File(s)</b>. Berkas lama otomatis tertimpa oleh yang baru. Klik <b>Close</b> saat selesai.'))
s += step(11, 'Bersihkan',
          P('Klik kanan ' + C('update-web.zip') + ' di server &gt; <b>Delete</b> (centang <b>Skip the trash</b> bila mau langsung hapus). Jika ada folder asing bernama <i>__MACOSX</i> (muncul dari komputer Mac), hapus juga.'))
s += box('stop', 'Jangan menghapus ini di public_html', '<b>alumni-foto</b> dan <b>kelola-foto</b> (foto alumni dan halaman pengelola foto), <b>.well-known</b> (sertifikat keamanan HTTPS), <b>cgi-bin</b>, dan berkas <b>.htaccess</b>. Tidak perlu menghapus apa pun sebelum mengekstrak. Berkas lama yang tidak ada lagi di versi baru dibiarkan saja.')
s += step(12, 'Periksa berkas .htaccess',
          P('Klik kanan ' + C('.htaccess') + ' &gt; <b>View</b>. Pastikan di bagian bawah ada tulisan ' + C('ea-php83') + '. Itu pengaturan PHP 8.3 yang dibutuhkan halaman pengelola foto. Hanya dilihat, <b>jangan diubah</b>.'))
s += step(13, 'Periksa website yang tayang',
          P('Buka <b>malangeducationcenter.com</b>, tekan ' + C('Ctrl+F5') + ' (muat ulang tanpa cache). Periksa:'),
          *bl(['Perubahan yang Anda buat terlihat.', 'Beranda, <i>Program</i>, <i>Alumni</i>, <i>Kontak</i> terbuka tanpa error, dan tombol WhatsApp membuka nomor yang benar (coba juga lewat HP).', '<i>malangeducationcenter.com/kelola-foto/</i> menampilkan halaman login (bukan error).']),
          P('Belum berubah? Tunggu 1 sampai 2 menit, atau buka di jendela penyamaran (' + C('Ctrl+Shift+N') + ').', SMALL))
# ---------------------------------------------------------------- BAB 6
s += chapter(6, 'Masalah umum dan jawabannya', 'Cari gejala yang sama, ikuti tindakannya. Kalau masih buntu, jangan menebak, hubungi pengembang dan kirim foto layar pesan error.')
s += table(['Gejala', 'Penyebab dan tindakan'], [
    ['<b>ENOENT ... could not read package.json</b> saat npm install atau npm run dev', 'Terminal tidak berada di folder proyek. Biasanya folder berlapis (<i>mec-academy\\mec-academy</i>). Di Terminal ketik ' + C('dir') + ': harus terlihat <i>package.json</i>. Kalau tidak, ketik ' + C('cd mec-academy') + ' lalu Enter dan ' + C('dir') + ' lagi. Atau tutup folder (File &gt; Close Folder) dan buka folder dalamnya lewat File &gt; Open Folder.'],
    ['<b>"npm" is not recognized</b> / "node tidak dikenali"', 'Node.js belum terpasang atau VS Code belum dimulai ulang sesudahnya. Pasang Node.js (Bab 2 langkah 1), <b>tutup semua VS Code</b>, buka lagi.'],
    ['<b>"running scripts is disabled on this system"</b>', 'Ganti jenis terminal ke Command Prompt (Bab 2 langkah 6).'],
    ['<b>npm install</b> lama atau gagal jaringan', 'Cek internet. Ulangi perintah. Jika masih gagal, pindahkan folder ke drive C: dan coba lagi.'],
    ['<b>localhost:4321</b> tidak terbuka', 'Pastikan Terminal masih menjalankan <i>npm run dev</i> dan tulisan <i>Local</i> masih muncul. Pakai alamat yang ditampilkan Terminal.'],
    ['Halaman error merah / layar penuh pesan', 'Perubahan terakhir salah (tanda kutip, koma, atau &lt; &gt; terhapus). Tekan Ctrl+Z di berkas itu sampai kembali, simpan.'],
    ['Gambar baru tidak muncul atau "Image not found"', 'Nama atau ekstensi tidak sama persis dengan berkas lama (huruf besar, .jpg.jpg, atau jpg vs webp).'],
    ['Error menyebut <b>JSON</b> atau <b>content.json</b> / <b>gallery.json</b>', 'Ada koma atau tanda kurung yang hilang atau berlebih saat menyalin blok. Setiap blok dipisah koma dan blok terakhir tanpa koma. Tekan Ctrl+Z sampai build normal.'],
    ['<b>npm run build</b> menampilkan error merah', 'Biasanya karena perubahan terakhir. Batalkan dengan Ctrl+Z lalu build ulang.'],
    ['Setelah unggah, website putih atau error 500', 'Kemungkinan .htaccess terhapus atau rusak. Ekstrak ulang zip, cek Show Hidden Files, lihat langkah 12. Bila tetap, pulihkan dari cadangan (langkah 8) dan hubungi pengembang.'],
    ['Perubahan tidak terlihat di website', 'Tekan Ctrl+F5, tunggu 2 menit, atau jendela penyamaran. Pastikan zip diekstrak ke <i>public_html</i> (bukan subfolder).'],
    ['Website menampilkan folder bernama dist di alamatnya', 'Zip dibuat dari folder dist, bukan dari <b>isi</b>-nya. Hapus folder <i>dist</i> di server, buat zip lagi dari <b>isi</b> dist (langkah 5).'],
    ['<b>/kelola-foto/</b> error 500', 'Di cPanel buka <b>MultiPHP Manager</b>, pilih domain malangeducationcenter.com, ubah PHP ke <b>8.3</b>. Pastikan .htaccess tidak terhapus.'],
    ['Zip gagal diunggah atau macet', 'Ulangi unggah. Cek sisa kuota disk di cPanel (kolom statistik di sisi kanan).'],
], [.34, .66])

# ---------------------------------------------------------------- BAB 7
s += chapter(7, 'Lembar contekan', 'Satu halaman untuk dicetak. Simpan di dekat komputer.')
s += [P('Perintah yang dipakai', H2)]
s += table(['Perintah', 'Kapan dipakai'], [
    [C('npm install'), 'Sekali saja, setelah folder disalin dari flashdisk.'],
    [C('npm run dev'), 'Menjalankan website di komputer untuk mengubah dan melihat hasilnya (buka localhost:4321). Berhenti dengan Ctrl+C.'],
    [C('npm run build'), 'Membuat folder <i>dist</i> siap tayang.'],
    [C('npm run preview'), 'Melihat hasil build sebelum diunggah.'],
], [.30, .70])
s += [P('Peta folder: apa isinya', H2)]
s += table(['Lokasi', 'Isi'], [
    [C('src/pages/'), 'Halaman-halaman website (beranda = index.astro, Tentang, Kontak, FAQ, dan seterusnya).'],
    [C('src/data/content.json'), 'Banyak teks utama: kontak, instruktur, modul, kegiatan.'],
    [C('src/data/faq.ts'), 'Tanya jawab (FAQ).'],
    [C('src/lib/site.ts'), 'Tautan formulir, media sosial, jam buka, alamat portal Learning.'],
    [C('src/data/gallery.json'), 'Daftar foto galeri kegiatan (halaman Fasilitas).'],
    [C('src/data/module-images.ts'), 'Foto header per modul.'],
    [C('src/components/Header.astro'), 'Menu di bagian atas.'],
    [C('src/content/articles/'), 'Artikel blog (satu berkas per artikel).'],
    [C('src/assets/images/'), 'Semua foto website.'],
    [C('public/'), 'Berkas yang diunggah apa adanya (ikon, robots.txt, halaman pengelola foto).'],
    [C('dist/'), 'Hasil build. <b>Ini yang diunggah ke hosting</b>, dibuat otomatis.'],
    [C('node_modules/'), 'Bahan program. Dibuat otomatis, jangan diubah.'],
], [.34, .66])
s += [P('Urutan setiap update', H2)]
s += bl(['<b>1.</b> Buka VS Code, buka folder, buka Terminal, ketik ' + C('npm run dev') + '.',
         '<b>2.</b> Ubah teks atau gambar, simpan, lihat di ' + C('localhost:4321') + '.',
         '<b>3.</b> ' + C('Ctrl+C') + ', lalu ketik ' + C('npm run build') + ' sampai tertulis Complete.',
         '<b>4.</b> Buka folder <i>dist</i>, tampilkan berkas tersembunyi, pilih semua, jadikan zip.',
         '<b>5.</b> cPanel &gt; File Manager &gt; <i>public_html</i> &gt; (cadangkan) &gt; Upload zip &gt; Extract ke <i>/public_html</i> &gt; hapus zip.',
         '<b>6.</b> Buka website, tekan Ctrl+F5, periksa hasilnya.'])
s += [P('<b>Keamanan:</b> simpan kata sandi cPanel di tempat aman (jangan lewat grup chat), ganti bila ada yang berhenti mengelola, dan simpan salinan folder <i>mec-academy</i> serta <i>alumni-foto</i> secara berkala.', SMALL)]

# ---------------------------------------------------------------- HALAMAN
def cover(c, d):
    c.saveState()
    c.setFillColor(DEEP); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(0, 0, W, 78 * mm, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(2); c.line(ML, H - 52 * mm, ML + 38 * mm, H - 52 * mm)
    c.setFillColor(GOLD); c.setFont('Inter-SB', 9.5); c.drawString(ML, H - 62 * mm, 'PANDUAN PENGELOLA WEBSITE')
    c.setFillColor(WHITE); c.setFont('Inter-B', 31)
    for i, ln in enumerate(['Mengelola website', 'MEC Academy', 'dari nol']): c.drawString(ML, H - (84 + i * 14) * mm, ln)
    c.setFont('Inter', 12); c.setFillColor(colors.HexColor('#C9D6D5'))
    for i, ln in enumerate(['Pasang di komputer, ubah teks dan gambar,', 'lalu tayangkan lewat cPanel.', 'Tanpa perlu bisa coding.']): c.drawString(ML, H - (136 + i * 6.4) * mm, ln)
    c.setFillColor(GOLD); c.setFont('Inter-SB', 9); c.drawString(ML, 56 * mm, 'malangeducationcenter.com')
    c.setFillColor(colors.HexColor('#C9D6D5')); c.setFont('Inter', 9)
    c.drawString(ML, 49 * mm, 'Versi 26 Oktober 2026 · untuk Windows 10/11 (catatan Mac disertakan)')
    c.drawString(ML, 43 * mm, 'Tidak berisi kata sandi. Kata sandi diberikan terpisah oleh pemilik.')
    c.restoreState()
def foot(c, d):
    c.saveState(); c.setFont('Inter', 7.8); c.setFillColor(MUTE)
    c.drawString(ML, 12 * mm, 'MEC Academy · Panduan pengelola website'); c.drawRightString(W - ML, 12 * mm, f'Halaman {d.page - 1}')
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(ML, H - 12 * mm, ML + 26 * mm, H - 12 * mm); c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=ML, topMargin=18 * mm, bottomMargin=19 * mm,
                      title='Panduan Pengelola Website MEC Academy', author='Achmad Hanim', subject='Pasang, ubah, dan tayangkan website tanpa coding')
fr = lambda: Frame(ML, 19 * mm, CW, H - 37 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='cover', frames=[fr()], onPage=cover), PageTemplate(id='main', frames=[fr()], onPage=foot)])
doc.build(s)
print('OK', OUT)
