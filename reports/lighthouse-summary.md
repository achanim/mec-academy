# Ringkasan Lighthouse

Dijalankan: 2026-10-18 · build produksi lokal · Lighthouse 13.5.0

Catatan: Lighthouse melewati layar intro (user-agent headless dianggap crawler). Angka lab (throttling simulasi), bukan data pengguna nyata.

| Perangkat | Halaman | Perf | A11y | BP | SEO | LCP (ms) | CLS | TBT (ms) | Status |
|---|---|---|---|---|---|---|---|---|---|
| mobile | `/` | 100 | 100 | 100 | 100 | 1882 | 0 | 5 | ✓ |
| desktop | `/` | 100 | 100 | 100 | 100 | 506 | 0.001 | 0 | ✓ |

Ambang: mobile perf ≥ 90, desktop perf ≥ 95; a11y/BP/SEO ≥ 95; LCP ≤ 2500/2000 ms; CLS ≤ 0.1; TBT ≤ 200 ms.
