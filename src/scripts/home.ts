import { chapterState, choreography, damp, indexFromProgress, motionAllowed, railIndex, railOffset, railProgress } from './motion';

const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const coarse = matchMedia('(pointer: coarse)');
const saveData = () => !!(navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData;

/* ---------- reveal sederhana (mode non-pinned) ---------- */
if (!reduced.matches && 'IntersectionObserver' in window) {
  root.classList.add('motion-ok');
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  document.querySelectorAll('[data-reveal]').forEach((t) => io.observe(t));
}

/* ---------- tab sistem mesin ---------- */
const tabs = [...document.querySelectorAll<HTMLButtonElement>('[data-tab]')];
const panels = [...document.querySelectorAll<HTMLElement>('[data-panel]')];
let tabIndex = 0;
function selectTab(i: number, focus = false) {
  tabIndex = i;
  tabs.forEach((t, n) => { t.setAttribute('aria-selected', String(n === i)); t.tabIndex = n === i ? 0 : -1; });
  panels.forEach((p, n) => (p.hidden = n !== i));
  if (focus) tabs[i].focus();
}
tabs.forEach((t, i) => {
  t.addEventListener('click', () => selectTab(i));
  t.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); selectTab((i + 1) % tabs.length, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); selectTab((i - 1 + tabs.length) % tabs.length, true); }
  });
});

/* ---------- video facade ---------- */
document.querySelectorAll<HTMLButtonElement>('[data-video]').forEach((b) => b.addEventListener('click', () => {
  const f = document.createElement('iframe');
  f.src = `https://www.youtube-nocookie.com/embed/${b.dataset.video}?autoplay=1&rel=0`;
  f.title = 'Company Profile MEC Academy';
  f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
  f.allowFullscreen = true;
  f.className = 'absolute inset-0 h-full w-full';
  b.replaceWith(f);
}));

/* ---------- koreografi scroll (pinned) ---------- */
interface Ch { el: HTMLElement; id: string; top: number; height: number; p: number; ready: boolean }
let chapters: Ch[] = [];
let active = false;
let raf = 0, last = 0;
let px = 0, py = 0, tx = 0, ty = 0;

const rail = document.querySelector<HTMLElement>('[data-rail]');
const railBar = document.querySelector<HTMLElement>('[data-rail-bar]');
const railLabel = document.querySelector<HTMLElement>('[data-rail-label]');
const cards = rail ? [...rail.children] as HTMLElement[] : [];

function splitWords() {
  document.querySelectorAll<HTMLElement>('[data-split]').forEach((h) => {
    if (h.dataset.splitDone) return;
    h.dataset.splitDone = '1';
    const text = h.textContent ?? '';
    h.setAttribute('aria-label', text);
    h.replaceChildren(...text.split(/\s+/).filter(Boolean).flatMap((w, i, all) => {
      const outer = document.createElement('span'); outer.className = 'wm'; outer.setAttribute('aria-hidden', 'true');
      const inner = document.createElement('span'); inner.style.setProperty('--i', String(i)); inner.textContent = w; outer.append(inner);
      return i < all.length - 1 ? [outer, document.createTextNode(' ')] : [outer];
    }));
  });
}

function teardown() {
  active = false;
  cancelAnimationFrame(raf);
  root.classList.remove('motion-ready');
  chapters.forEach(({ el }) => { el.classList.remove('motion-scene'); el.removeAttribute('style'); });
  chapters = [];
  root.style.removeProperty('--px'); root.style.removeProperty('--py');
}

function setup() {
  teardown();
  const ok = motionAllowed({ width: innerWidth, height: innerHeight, reduced: reduced.matches, coarse: coarse.matches, saveData: saveData() });
  if (!ok) return;
  // Chapter hanya di-pin bila kontennya muat dalam satu layar
  const els = [...document.querySelectorAll<HTMLElement>('[data-chapter]')].filter((el) => {
    const inner = el.querySelector<HTMLElement>('.scene-inner');
    return inner ? inner.offsetHeight + 152 <= innerHeight : false;
  });
  if (!els.length) return;
  splitWords();
  els.forEach((el) => { el.style.setProperty('--span', el.dataset.span ?? '1.6'); el.classList.add('motion-scene'); });
  root.classList.add('motion-ready');
  active = true;
  requestAnimationFrame(() => {
    measure(els);
    chapters.forEach((c) => (c.ready = false));
    kick();
  });
}

function measure(els: HTMLElement[]) {
  chapters = els.map((el) => ({ el, id: el.dataset.chapter!, top: el.getBoundingClientRect().top + scrollY, height: el.offsetHeight, p: 0, ready: false }));
}

const vw = () => (rail?.parentElement?.getBoundingClientRect().left ?? 0);
function railGeom() {
  if (!rail || !cards.length) return null;
  const width = cards[0].offsetWidth, gap = 24, track = cards.length * width + (cards.length - 1) * gap;
  const viewport = innerWidth - vw();
  return { width, gap, track, viewport };
}

function tick(now: number) {
  raf = 0;
  if (!active) return;
  const dt = last ? now - last : 16; last = now;
  const vh = innerHeight;
  let moving = false;
  for (const c of chapters) {
    const st = chapterState(scrollY, c.top, c.height, vh);
    if (st.local < -vh * 1.3 || st.local > st.travel + vh * 1.3) { if (c.ready) continue; }
    const target = st.progress;
    c.p = c.ready ? damp(c.p, target, dt) : target;
    c.ready = true;
    if (Math.abs(c.p - target) > 0.0005) moving = true;
    const v = choreography(c.id, c.p, st.enter);
    const s = c.el.style;
    s.setProperty('--enter', st.enter.toFixed(4));
    s.setProperty('--exit', st.exit.toFixed(4));
    for (const [k, val] of Object.entries(v)) s.setProperty(`--${k === 'camX' ? 'camx' : k === 'camY' ? 'camy' : k}`, val.toFixed(4));
    if (c.id === 'learning') {
      const g = railGeom();
      if (g) {
        const off = railOffset(c.p, g.track, g.viewport);
        s.setProperty('--rail-x', `${off.toFixed(1)}px`);
        const idx = railIndex(off, g.width, g.gap, cards.length, g.viewport);
        cards.forEach((card, n) => { const d = Math.abs(n - idx); card.style.setProperty('--card-d', String(Math.min(d, 2))); card.style.setProperty('--card-a', String(Math.sign(n - idx) * Math.min(d, 2) * 3)); });
        railBar?.style.setProperty('--rail-p', String(cards.length > 1 ? idx / (cards.length - 1) : 1));
        if (railLabel) railLabel.textContent = `0${idx + 1} / 0${cards.length} ${cards[idx].dataset.title ?? ''}`;
      }
    }
    if (c.id === 'machine' && panels.length) {
      const i = indexFromProgress(c.p, panels.length);
      if (i !== autoTab) { autoTab = i; if (i !== tabIndex) selectTab(i); }
    }
  }
  // parallax pointer
  px = damp(px, tx, dt, 120); py = damp(py, ty, dt, 120);
  root.style.setProperty('--px', px.toFixed(3)); root.style.setProperty('--py', py.toFixed(3));
  if (Math.abs(px - tx) > 0.001 || Math.abs(py - ty) > 0.001) moving = true;
  const doc = document.documentElement.scrollHeight - vh;
  root.style.setProperty('--page-p', String(doc > 0 ? scrollY / doc : 0));
  if (moving) kick();
}
let autoTab = -1;
function kick() { if (active && !raf) raf = requestAnimationFrame(tick); }

addEventListener('scroll', kick, { passive: true });
addEventListener('pointermove', (e) => { if (!active || e.pointerType !== 'mouse') return; tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2; kick(); }, { passive: true });
let resizeT = 0;
addEventListener('resize', () => { clearTimeout(resizeT); resizeT = window.setTimeout(setup, 200); });
reduced.addEventListener?.('change', setup);
document.fonts?.ready.then(() => active && setup());

/* ---------- rail: tombol prev/next ---------- */
function goRail(dir: number) {
  if (!rail) return;
  if (!active) {
    const step = cards[0].getBoundingClientRect().width + 24;
    rail.scrollBy({ left: dir * step, behavior: reduced.matches ? 'auto' : 'smooth' });
    return;
  }
  const c = chapters.find((x) => x.id === 'learning'); const g = railGeom();
  if (!c || !g) return;
  const idx = railIndex(railOffset(c.p, g.track, g.viewport), g.width, g.gap, cards.length, g.viewport);
  const next = Math.min(cards.length - 1, Math.max(0, idx + dir));
  const p = railProgress(next, cards.length, g.width, g.gap, g.track, g.viewport);
  scrollTo({ top: c.top + p * (c.height - innerHeight), behavior: 'smooth' });
}
document.querySelector('[data-rail-prev]')?.addEventListener('click', () => goRail(-1));
document.querySelector('[data-rail-next]')?.addEventListener('click', () => goRail(1));

if (!reduced.matches) { root.classList.add('intro'); setTimeout(() => root.classList.remove('intro'), 2000); }
setup();
