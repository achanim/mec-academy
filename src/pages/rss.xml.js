import { publishedArticles } from '../lib/articles';
import { site } from '../lib/site';
const esc = (s) => s.replace(/[<>&"']/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' })[c]);
export async function GET(ctx) {
  const items = (await publishedArticles()).map((a) => `<item><title>${esc(a.data.title)}</title><link>${new URL(`/artikel/${a.id}/`, ctx.site)}</link><guid>${new URL(`/artikel/${a.id}/`, ctx.site)}</guid><pubDate>${a.data.publishedAt.toUTCString()}</pubDate><description>${esc(a.data.description)}</description></item>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>${site.name} — Artikel</title><link>${ctx.site}</link><description>${esc(site.description)}</description><language>id</language>${items}</channel></rss>`, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
