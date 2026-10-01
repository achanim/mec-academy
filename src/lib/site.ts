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
export const waLink = (msg = site.registerMessage) => `${site.whatsapp}?text=${encodeURIComponent(msg)}`;
export const slugify = (s: string) =>
  s.toLowerCase().replace(/&/g, 'dan').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
export const modules = (content.modules as string[]).map((title, i) => ({ title, slug: slugify(title), n: i + 1 }));
