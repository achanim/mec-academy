import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/articles' }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(70),
      description: z.string().min(50).max(170),
      publishedAt: z.coerce.date(),
      updatedAt: z.coerce.date().optional(),
      author: z.string().default('Tim MEC Academy'),
      category: z.enum(['karier', 'teknis', 'k3-budaya-kerja', 'industri', 'info-bmc', 'alumni']),
      tags: z.array(z.string()).default([]),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
      relatedModules: z.array(z.string()).default([]),
      draft: z.boolean().default(false),
    }),
});
export const collections = { articles };
