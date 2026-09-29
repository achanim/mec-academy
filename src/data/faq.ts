import content from './content.json';

/** FAQ hanya memuat fakta dari company profile; biaya/jadwal sengaja diarahkan ke tim MEC. */
export const faq: { q: string; a: string; home?: boolean }[] = [
  { q: 'Apa itu Basic Mechanic Course (BMC)?', a: 'BMC adalah program pelatihan dasar mekanik alat berat di MEC Academy, Malang: 16 modul pembelajaran, praktik komponen, pembentukan karakter, dan On the Job Training.', home: true },
  { q: 'Apa saja tahapan seleksinya?', a: `${content.stages[0].items.join(', ')}. Setelah itu peserta mengikuti in-class training dan On the Job Training.`, home: true },
  { q: 'Apa saja yang dipelajari di BMC?', a: `Ada ${content.modules.length} modul, antara lain ${content.modules.slice(0, 5).join(', ')}, dan seterusnya sampai ${content.modules.at(-1)}. Praktik memakai komponen seperti ${content.components.slice(0, 3).join(', ')}.`, home: true },
  { q: 'Apakah ada On the Job Training (OJT)?', a: `Ya. ${content.stages[2].items.join('; ')}.` },
  { q: 'Fasilitas apa saja yang tersedia?', a: `${content.facilities.join('; ')}.`, home: true },
  { q: 'Siapa yang mengajar?', a: 'Instruktur berpengalaman di industri alat berat dengan kompetensi seperti BNSP ToT Level III/IV, Pengawas Operasional Pertama, Asesor Kompetensi, dan Sertifikasi K3 Umum. Profil lengkap ada di halaman Instruktur.' },
  { q: 'Berapa biaya dan kapan jadwal terdekat?', a: 'Informasi biaya dan jadwal terbaru dikonfirmasi langsung oleh tim MEC agar selalu akurat. Hubungi lewat WhatsApp atau email di halaman Kontak.', home: true },
  { q: 'Apakah ada jaminan penempatan kerja?', a: 'Situs ini tidak menyatakan jaminan penempatan kerja. Kegiatan bersama perusahaan yang ditampilkan adalah dokumentasi kunjungan dan penyerahan komponen. Tanyakan alur OJT dan peluang kerja langsung ke tim MEC.' },
  { q: 'Bagaimana cara mengakses assessment online?', a: 'Akun (username dan password) diberikan oleh tim assessor MEC Academy. Setelah menerimanya, masuk lewat halaman Assessment.' },
];
