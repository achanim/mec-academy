import content from '../data/content.json';

export const site = {
  name: 'MEC Academy',
  url: 'https://malangeducationcenter.com',
  description:
    'Basic Mechanic Course MEC Academy: praktik komponen, instruktur industri, dan pembentukan karakter untuk calon mekanik alat berat di Malang.',
  registerMessage:
    'Halo MEC Academy, saya ingin mendaftar program Basic Mechanic Course (BMC). Mohon informasi jadwal, biaya, persyaratan, dan alur seleksinya.',
  assessmentUrl: 'https://malangeducationcentreacademy.my.id/assessment/',
  ...content.contact,
};
// Setiap pesan WhatsApp dari website diberi penanda sumber supaya tim MEC tahu pengirim datang dari web.
export const waSource = `Saya menemukan MEC Academy lewat website (${site.url.replace('https://', '')}).`;
export const waLink = (msg = site.registerMessage) => `${site.whatsapp}?text=${encodeURIComponent(`${msg}\n\n${waSource}`)}`;
export const slugify = (s: string) =>
  s.toLowerCase().replace(/&/g, 'dan').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
export const modules = (content.modules as string[]).map((title, i) => ({ title, slug: slugify(title), n: i + 1 }));
