# TODO — MEC Academy

Diperbarui: 2026-09-29 · Branch: `claude/new-repo-infra-tech-stack-e62imy`

## Selesai
- [x] Plan infra & tech stack (`docs/PLAN.md`)
- [x] Fase 0 — scaffold Astro 7 + Tailwind 4 + MDX, CI, vitest
- [x] Fase 1 — ekstraksi aset & konten dari preview (21 MB → 7 MB master, font woff2)
- [x] Halaman inti: beranda (12 bab), BMC, 16 modul, tahapan, fasilitas, instruktur, tentang, assessment, kontak
- [x] Sistem artikel (MDX, kategori, FAQ/BlogPosting/Breadcrumb JSON-LD), RSS, sitemap, Pagefind

## Sedang dikerjakan
- [ ] **Animasi scroll ala preview** (pinned scene, kamera zoom, hero-frame, rail horizontal, character beats, portal video, word-mask heading) — desktop saja, fallback aman untuk mobile/reduced-motion

## Berikutnya (perlu keputusan/data dari klien)
- [ ] Domain final → ganti placeholder `mecacademy.id` di `astro.config.mjs`, `src/lib/site.ts`, `public/robots.txt`
- [ ] Deploy Cloudflare Pages (connect repo, `NODE_VERSION=22`), DNS, redirect dari domain lama
- [ ] Konfirmasi lisensi 4 font MEC (MECDisplay/Body/Bold/Mono) untuk penggunaan web
- [ ] Konfirmasi ejaan nama instruktur "Johan Winarto/Wiharto"
- [ ] Isi deskripsi/tujuan/materi 12 modul yang masih placeholder (4 modul sudah ada)
- [ ] Halaman detail instruktur `/instruktur/[slug]/` + `Person` JSON-LD
- [ ] Halaman industri & alumni (`/industri/`, `/alumni/`), `/faq/` + FAQPage JSON-LD
- [ ] CMS editor untuk artikel (Keystatic/Decap) — butuh keputusan hosting & login GitHub
- [ ] OG image dinamis per artikel (Satori) + OG default yang proper
- [ ] Riset keyword + kalender editorial; tulis 5–10 artikel awal per pilar topik
- [ ] Analytics (Plausible/Umami) + Google Search Console + sitemap submit
- [ ] Form lead (Cloudflare Worker + Turnstile) bila WhatsApp saja tidak cukup
- [ ] CSP header, Lighthouse CI budget, a11y test (axe) di CI, link-check
- [ ] Uptime monitoring
- [ ] Multi-bahasa (EN)? — putuskan sebelum struktur URL dikunci
