import type { ImageMetadata } from 'astro';
const all = import.meta.glob<{ default: ImageMetadata }>('../assets/images/*.{jpg,webp}', { eager: true });
export function img(name: string): ImageMetadata {
  const hit = Object.entries(all).find(([p]) => p.endsWith(`/${name}.jpg`) || p.endsWith(`/${name}.webp`));
  if (!hit) throw new Error(`Image not found: ${name}`);
  return hit[1].default;
}
