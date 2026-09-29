import type { ImageMetadata } from 'astro';
const all = import.meta.glob<{ default: ImageMetadata }>('../assets/images/*.{jpg,webp}', { eager: true });
export function img(name: string): ImageMetadata {
  const hit = Object.entries(all).find(([p]) => p.endsWith(`/${name}.jpg`) || p.endsWith(`/${name}.webp`));
  if (!hit) throw new Error(`Image not found: ${name}`);
  return hit[1].default;
}

/** Titik fokus (object-position) per foto supaya wajah/komponen tidak terpotong saat di-crop. */
const focus: Record<string, string> = {
  hero: '62% 40%', classroom: '50% 45%', practice: '55% 40%', ojt: '50% 50%', engine: '50% 45%', hydraulic: '50% 45%',
  workshop: '50% 40%', 'gallery-01': '50% 30%', 'gallery-02': '50% 45%', building: '50% 60%', teaching: '50% 40%',
  'event-komatsu': '50% 38%', 'event-sinarindo': '50% 58%', 'event-ppa': '50% 64%', 'event-ut': '50% 45%',
  alumni: '50% 55%', alumni2: '50% 50%', film: '50% 40%', prayer: '65% 50%', bintalsik: '50% 45%',
};
export const pos = (name: string) => `object-position: ${focus[name] ?? '50% 40%'}`;
