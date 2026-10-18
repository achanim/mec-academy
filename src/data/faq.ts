import content from './content.json';

/** FAQ hanya memuat fakta dari company profile; biaya/jadwal sengaja diarahkan ke tim MEC. */
export const faq: { q: string; a: string; home?: boolean }[] = [
  { q: 'Apa itu MEC Academy?', a: 'MEC Academy adalah lembaga pendidikan dan pelatihan keterampilan teknik alat berat di Malang yang menyiapkan peserta untuk berkarier di dunia profesional. Saat ini program yang tersedia adalah Basic Mechanic Course (BMC).', home: true },
  { q: 'Apa itu Basic Mechanic Course (BMC)?', a: 'BMC adalah program pelatihan dasar mekanik alat berat di MEC Academy, Malang: 16 modul pembelajaran, praktik komponen, pembentukan karakter, dan On the Job Training.', home: true },
  { q: 'Apa saja tahapan seleksinya?', a: `${content.stages[0].items.join(', ')}. Setelah itu peserta mengikuti in-class training dan On the Job Training.`, home: true },
  { q: 'Apa saja yang dipelajari di BMC?', a: `Ada ${content.modules.length} modul, antara lain ${content.modules.slice(0, 5).join(', ')}, dan seterusnya sampai ${content.modules.at(-1)}. Praktik memakai komponen seperti ${content.components.slice(0, 3).join(', ')}.`, home: true },
  { q: 'Apa saja persyaratan menjadi siswa BMC?', a: `${content.requirements.admin.join('; ')}.` },
  { q: 'Berapa lama durasi pelatihan?', a: 'In-class training berlangsung 3 bulan, dilanjutkan On the Job Training (OJT) selama 6–12 bulan.' },
  { q: 'Apakah ada On the Job Training (OJT)?', a: `Ya, selama 6–12 bulan. ${content.stages[2].items.join('; ')}.` },
  { q: 'Fasilitas apa saja yang tersedia?', a: `${content.facilities.join('; ')}.`, home: true },
  { q: 'Siapa yang mengajar?', a: 'Instruktur berpengalaman di industri alat berat dengan kompetensi seperti BNSP ToT Level III/IV, Pengawas Operasional Pertama, Asesor Kompetensi, dan Sertifikasi K3 Umum. Profil lengkap ada di halaman Instruktur.' },
  { q: 'Kapan pendaftaran dibuka dan bagaimana caranya?', a: 'Kelas BMC angkatan 58 membuka pendaftaran pada 15 September sampai 30 Oktober 2026. Pendaftaran dilakukan lewat formulir pendaftaran yang tersedia di halaman Kontak; setelah mengisi, bergabunglah ke grup WhatsApp untuk mendapat info terbaru. Hubungi tim MEC lewat WhatsApp untuk jadwal angkatan berikutnya.', home: true },
  { q: 'Kapan jam operasional dan di mana lokasinya?', a: 'Tim MEC Academy melayani Senin sampai Jumat pukul 08.00–16.00 WIB. Lokasi dan petanya ada di halaman Kontak.' },
  { q: 'Berapa biaya pelatihan?', a: 'Informasi biaya dikonfirmasi langsung oleh tim MEC agar selalu akurat. Hubungi lewat WhatsApp atau email di halaman Kontak.' },
  { q: 'Bagaimana jika saya belum memenuhi persyaratan (usia, jurusan, tinggi badan, atau ijazah belum keluar)?', a: 'Konsultasikan kondisi Anda langsung dengan tim MEC lewat WhatsApp. Situs ini tidak menjanjikan pengecualian persyaratan; tim MEC yang menentukan.' },
  { q: 'Apakah ada jaminan penempatan kerja?', a: 'Situs ini tidak menyatakan jaminan penempatan kerja. Kegiatan bersama perusahaan yang ditampilkan adalah dokumentasi kunjungan dan penyerahan komponen. Tanyakan alur OJT dan peluang kerja langsung ke tim MEC.' },
  { q: 'Bagaimana cara mengakses assessment online?', a: 'Akun (username dan password) diberikan oleh tim assessor MEC Academy. Setelah menerimanya, masuk lewat halaman Assessment.' },
];
