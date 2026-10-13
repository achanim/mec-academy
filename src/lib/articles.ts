import { getCollection } from 'astro:content';
export const categories: Record<string, string> = {
  karier: 'Karier Mekanik Alat Berat',
  teknis: 'Pengetahuan Teknis',
  'k3-budaya-kerja': 'K3 & Budaya Kerja',
  industri: 'Industri & Pertambangan',
  'info-bmc': 'Info BMC & OJT',
  alumni: 'Cerita Alumni',
};
// Halaman kategori baru diindeks Google bila isinya cukup (hindari konten tipis); selaras dengan filter sitemap di astro.config.mjs
export const MIN_ARTICLES = 3;
export async function publishedArticles() {
  const all = await getCollection('articles', (a) => !a.data.draft && a.data.publishedAt <= new Date());
  return all.sort((a, b) => +b.data.publishedAt - +a.data.publishedAt);
}
export const readingMinutes = (body = '') => Math.max(1, Math.round(body.split(/\s+/).length / 200));
