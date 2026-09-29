# TODO — MEC Academy

Diperbarui: 2026-09-29 · Branch: `claude/new-repo-infra-tech-stack-e62imy`

## Selesai
- [x] Plan infra & tech stack (`docs/PLAN.md`)
- [x] Fase 0 — scaffold Astro 7 + Tailwind 4 + MDX, CI, vitest
- [x] Fase 1 — ekstraksi aset & konten dari preview (21 MB → 7 MB master, font woff2)
- [x] Halaman inti: beranda (12 bab), BMC, 16 modul, tahapan, fasilitas, instruktur, tentang, assessment, kontak
- [x] Sistem artikel (MDX, kategori, FAQ/BlogPosting/Breadcrumb JSON-LD), RSS, sitemap, Pagefind

- [x] Animasi scroll ala preview: 7 chapter pinned (hero, challenge, journey, machine, learning, character, film), kamera zoom, hero-frame, word-mask, rail horizontal, tab mesin otomatis 3D, wipe karakter, zoom video; fallback mobile/reduced-motion/layar pendek (`src/scripts/motion.ts`, `home.ts`)

## Sedang dikerjakan
- (kosong)

## Berikutnya (perlu keputusan/data dari klien)
- [ ] Domain final → ganti placeholder `mecacademy.id` di `astro.config.mjs`, `src/lib/site.ts`, `public/robots.txt`
- [ ] Deploy Cloudflare Pages (connect repo, `NODE_VERSION=22`), DNS, redirect dari domain lama
- [ ] **Font**: ternyata bukan font custom MEC — MECBody/Bold = Nimbus Sans, MECDisplay = Nimbus Sans Narrow Bold (lisensi AGPL-3 + font exception, exception hanya menyebut PDF/PostScript → abu-abu untuk web), MECMono = DejaVu Sans Mono (Bitstream Vera, aman). Putuskan: ganti Nimbus dengan font OFL (mis. Archivo / Archivo Narrow / Inter, dari Google Fonts, self-host) atau tetap pakai + minta review legal. Teks lisensi sudah ada di `public/licenses/`.
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
