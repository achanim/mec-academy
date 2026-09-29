// Fungsi murni untuk koreografi scroll (di-port dari MECMotion preview). Tanpa DOM → mudah dites.
export const clamp = (n: number, min = 0, max = 1) => Math.min(max, Math.max(min, n));
export const smooth = (a: number, b: number, n: number) => { const t = clamp((n - a) / (b - a)); return t * t * (3 - 2 * t); };
export const mix = (a: number, b: number, p: number) => a + (b - a) * p;
/** Peredaman tak-tergantung-framerate menuju target. */
export const damp = (cur: number, target: number, dt: number, tau = 85) =>
  Math.abs(target - cur) < 0.0005 ? target : mix(cur, target, 1 - Math.exp(-clamp(dt, 0, 64) / tau));

export interface ChapterState { progress: number; enter: number; exit: number; local: number; travel: number }
/** scroll: posisi window; top: offset atas chapter; height: tinggi chapter (termasuk span pin). */
export function chapterState(scroll: number, top: number, height: number, viewport: number): ChapterState {
  const local = scroll - top;
  const travel = Math.max(1, height - viewport);
  return {
    local, travel,
    progress: clamp(local / travel),
    enter: smooth(-viewport * 0.85, -viewport * 0.12, local),
    exit: smooth(travel, travel + viewport * 0.85, local),
  };
}

/** Progress → translateX rail horizontal (negatif). */
export const railOffset = (p: number, track: number, viewport: number) => -Math.max(0, track - viewport) * smooth(0.1, 0.9, p);
export function railIndex(offset: number, width: number, gap: number, count: number, viewport: number) {
  const overflow = Math.max(0, count * width + (count - 1) * gap - viewport);
  if (-offset < 0.5) return 0;
  if (overflow && -offset >= overflow - 0.5) return count - 1;
  return clamp(Math.round((-offset + viewport / 2 - width / 2) / Math.max(1, width + gap)), 0, count - 1);
}
/** Kebalikan railOffset: progress yang menempatkan kartu `index` di tengah (untuk tombol prev/next). */
export function railProgress(index: number, count: number, width: number, gap: number, track: number, viewport: number) {
  const overflow = Math.max(0, track - viewport);
  if (!overflow || count < 2) return 0;
  const desired = clamp((index * (width + gap) + width / 2 - viewport / 2) / overflow);
  let a = 0.1, b = 0.9;
  for (let i = 0; i < 22; i++) { const m = (a + b) / 2; if (smooth(0.1, 0.9, m) < desired) a = m; else b = m; }
  return (a + b) / 2;
}

export interface MotionEnv { width: number; height: number; reduced: boolean; coarse: boolean; saveData: boolean }
/** Animasi pinned hanya di desktop, pointer halus, tanpa reduced-motion / save-data. */
export const motionAllowed = (e: MotionEnv) => e.width >= 1000 && e.height >= 700 && !e.reduced && !e.coarse && !e.saveData;

/** Pemilih indeks tab dari progress (untuk chapter machine). */
export const indexFromProgress = (p: number, count: number) => clamp(Math.floor(clamp(p, 0, 0.9999) * count), 0, count - 1);

/** Nilai turunan per chapter (semua 0..1 kecuali disebut lain). */
export function choreography(id: string, p: number, enter: number) {
  const advance = smooth(0.04, 0.94, p);
  const breathe = Math.sin(clamp(p) * Math.PI);
  const c: Record<string, number> = {
    gate: 1 - enter, advance, camY: -42 * advance, zoom: 1.06 + 0.1 * advance,
    s0: smooth(0.05, 0.35, p), s1: smooth(0.3, 0.6, p), s2: smooth(0.55, 0.85, p),
  };
  if (id === 'hero') Object.assign(c, { camX: -3.6 * advance, camY: -62 * advance, zoom: 1.05 + 0.21 * advance, frame: smooth(0.28, 0.68, p), word: smooth(0.1, 0.7, p) });
  if (id === 'machine') Object.assign(c, { orbit: mix(-8, 16, advance), depth: 70 * breathe });
  if (id === 'character') Object.assign(c, { zoom: 1.03 + 0.12 * advance, prayer: smooth(0.35, 0.84, p), b0: bump(p, 0.08, 0.3), b1: bump(p, 0.36, 0.6), b2: bump(p, 0.64, 0.92) });
  if (id === 'film') Object.assign(c, { zoom: 1.62 - 0.57 * advance, portal: 12 * (1 - smooth(0.02, 0.58, p)) });
  return c;
}
/** Fade-in/out berbentuk lonceng di antara a..b. */
export const bump = (p: number, a: number, b: number) => smooth(a, a + (b - a) * 0.3, p) * (1 - smooth(a + (b - a) * 0.7, b, p));

/** Zoom foto (hero-frame) sampai memenuhi layar. box = posisi & ukuran frame tanpa transform. */
export function zoomPortal(p: number, box: { x: number; y: number; width: number; height: number } | null, viewport: { width: number; height: number }) {
  if (!box || box.width <= 0 || box.height <= 0) return { progress: 0, scale: 1, x: 0, y: 0, caption: 1 };
  const t = smooth(0.56, 0.96, p);
  const cover = Math.max((viewport.width + 100) / box.width, (viewport.height + 100) / box.height) * 1.12;
  return { progress: t, scale: Math.pow(Math.max(1, cover), t), x: (viewport.width / 2 - box.x - box.width / 2) * t, y: (viewport.height / 2 - box.y - box.height / 2) * t, caption: 1 - smooth(0, 0.32, t) };
}
