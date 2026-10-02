# Paket Ringkas — pemetaan proposal ke situs

Branch `claude/proposal-paket-ringkas`. Proposal: `docs/Proposal-Website-MEC-Academy-Paket-Ringkas.pdf` (Rp 9.000.000, 10 hari kerja).

| Proposal | Di situs |
|---|---|
| Beranda 12 bagian sesuai desain | `src/pages/index.astro` |
| Animasi (gulir, zoom, daftar bergeser, tab mesin) | `src/scripts/home.ts`, `motion.ts` (dipertahankan; ada mode tenang & cadangan HP/reduced-motion) |
| Dialog: 16 modul, instruktur, fasilitas + galeri, tahapan, FAQ, kontak | `src/components/Dialogs.astro`, `src/scripts/dialogs.ts` |
| Tampilan HP/tablet/laptop | CSS responsif yang sama; audit 5 ukuran layar lolos |
| SEO dasar satu halaman + tampilan saat dibagikan | `Seo.astro`, JSON-LD WebSite/Organisasi/FAQPage, sitemap 1 URL |
| Pemasangan di hosting MEC | `public/.htaccess`, `docs/DEPLOY.md` |

## Dihapus dibanding branch multi-halaman
Layar intro "klik untuk mulai" (loader), blog/artikel + RSS, pencarian (Pagefind), dan halaman terpisah: program, 16 modul, tahapan, fasilitas, instruktur (+profil), industri, sumber, tentang, assessment, kontak, FAQ. Alamat lama dialihkan di `public/.htaccess` ke beranda + dialog yang sesuai (mis. `/instruktur/nur-wiranto/` menjadi `/#instruktur-nur-wiranto`).

## Konsekuensi (sudah tertulis di proposal, Bagian 5)
Google hanya melihat satu halaman, tanpa blog, tanpa tautan per modul di hasil pencarian; isi dialog ada di `<template>` pada HTML tetapi tidak dijamin terindeks sebagai halaman sendiri.

## Hasil uji (2026-10-02)
`astro check` 0 error · 10 tes lolos · audit situs 0 pelanggaran · Lighthouse mobile 99/100/100/100, desktop 100/100/100/100 (LCP 2,1 dtk / 0,5 dtk, CLS 0).
