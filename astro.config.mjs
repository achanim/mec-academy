import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://malangeducationcenter.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap({ filter: (p) => !/\/(404|500)\/?$/.test(p) })],
  vite: { plugins: [tailwindcss()] },
});
