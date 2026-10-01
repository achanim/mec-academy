import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://malangeducationcenter.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [mdx(), sitemap({ filter: (p) => !/\/(404|500)\/?$/.test(p) })],
  vite: { plugins: [tailwindcss()] },
});
