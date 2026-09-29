import { modules } from './site';

/** Pengelompokan modul untuk tampilan (pengelompokan oleh tim web, bukan dari company profile). */
export const moduleGroups = [
  { title: 'Dasar & keselamatan', range: [1, 4], note: 'Fondasi sebelum menyentuh unit' },
  { title: 'Sistem penggerak & tenaga', range: [5, 9], note: 'Engine, hidrolik, kelistrikan, dan penyaluran tenaga' },
  { title: 'Kemudi, roda & undercarriage', range: [10, 12], note: 'Sistem kendali dan penopang unit' },
  { title: 'Perawatan & pendukung', range: [13, 16], note: 'Praktik perawatan, part book, dan perangkat pendukung' },
].map((g) => ({ ...g, items: modules.filter((m) => m.n >= g.range[0] && m.n <= g.range[1]) }));
