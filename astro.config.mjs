import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { readdirSync, readFileSync } from 'node:fs';

// Hitung artikel terbit per kategori dari frontmatter (selaras dengan MIN_ARTICLES di src/lib/articles.ts)
const MIN_ARTICLES = 3;
const catCount = {};
for (const f of readdirSync('src/content/articles').filter((x) => /\.mdx?$/.test(x))) {
  const fm = readFileSync(`src/content/articles/${f}`, 'utf8').split('---')[1] ?? '';
  if (/^draft:\s*true/m.test(fm)) continue;
  const c = fm.match(/^category:\s*(\S+)/m)?.[1];
  if (c) catCount[c] = (catCount[c] ?? 0) + 1;
}
const thinCategory = (p) => { const m = p.match(/\/artikel\/kategori\/([^/]+)\/?$/); return !!m && (catCount[m[1]] ?? 0) < MIN_ARTICLES; };

export default defineConfig({
  site: 'https://malangeducationcenter.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [mdx(), sitemap({ filter: (p) => !/\/(404|500)\/?$/.test(p) && !thinCategory(p) })],
  vite: { plugins: [tailwindcss()] },
});
