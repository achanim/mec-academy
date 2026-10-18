import content from '../data/content.json';

export const site = {
  name: 'MEC Academy',
  url: 'https://malangeducationcenter.com',
  description:
    'Basic Mechanic Course MEC Academy: praktik komponen, instruktur industri, dan pembentukan karakter untuk calon mekanik alat berat di Malang.',
  registerMessage:
    'Halo MEC Academy, saya ingin mendaftar program Basic Mechanic Course (BMC). Mohon informasi jadwal, biaya, persyaratan, dan alur seleksinya.',
  assessmentUrl: 'https://malangeducationcentreacademy.my.id/assessment/',
  // Formulir pendaftaran angkatan berjalan (Google Form). Diperbarui MEC tiap angkatan.
  registerFormUrl: 'https://forms.gle/HoMKfnvuJLiLXtvWA',
  mapsUrl: 'https://maps.app.goo.gl/EThQMpHZzWx9vvUr8',
  googleProfileUrl: 'https://share.google/hhJuteGRUgX3LXx7g',
  // Profil sosial resmi (schema.org sameAs). Info dari MEC, 18 Okt 2026. TikTok: coming soon (belum ada akun).
  social: ['https://www.instagram.com/academy_mec/', 'https://www.linkedin.com/company/cv-mec-academy/'] as string[],
  hoursLabel: 'Senin–Jumat, 08.00–16.00 WIB',
  // Isi bila sudah ada data resmi; kosong = tidak ditampilkan di data terstruktur.
  geo: null as null | { lat: number; lng: number },
  openingHours: [{ days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], opens: '08:00', closes: '16:00' }] as { days: string[]; opens: string; closes: string }[],
  // Verifikasi kepemilikan (isi nilai content dari meta tag Google Search Console / Bing Webmaster; kosong = tidak dirender)
  verification: { google: '', bing: '' },
  // Analitik ramah privasi (mis. Plausible/Umami). Kosong = tidak ada skrip. Contoh Plausible: { src: 'https://plausible.io/js/script.js', attrs: { 'data-domain': 'malangeducationcenter.com' } }
  analytics: { src: '', attrs: {} as Record<string, string> },
  ...content.contact,
};
// Setiap pesan WhatsApp dari website diberi penanda sumber supaya tim MEC tahu pengirim datang dari web.
export const waSource = `Saya menemukan MEC Academy lewat website (${site.url.replace('https://', '')}).`;
export const waLink = (msg = site.registerMessage) => `${site.whatsapp}?text=${encodeURIComponent(`${msg}\n\n${waSource}`)}`;
export const slugify = (s: string) =>
  s.toLowerCase().replace(/&/g, 'dan').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
export const modules = (content.modules as string[]).map((title, i) => ({ title, slug: slugify(title), n: i + 1 }));
