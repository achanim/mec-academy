import { chapterState, choreography, clamp, damp, indexFromProgress, motionAllowed, railIndex, railOffset, railProgress, zoomPortal } from './motion';

const root = document.documentElement;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const coarse = matchMedia('(pointer: coarse)');
const saveData = () => !!(navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData;
const calm = () => root.classList.contains('calm');

/* ---------- reveal sederhana (mode non-pinned) ---------- */
if (!reduced.matches && 'IntersectionObserver' in window) {
  root.classList.add('motion-ok');
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  document.querySelectorAll('[data-reveal]').forEach((t) => io.observe(t));
}

/* ---------- tab sistem mesin ---------- */
const tabs = [...document.querySelectorAll<HTMLButtonElement>('[data-tab]')];
const panels = [...document.querySelectorAll<HTMLElement>('[data-panel]')];
const infos = [...document.querySelectorAll<HTMLElement>('[data-info]')];
const stage = document.querySelector<HTMLElement>('[data-stage]');
let tabIndex = 0, autoTab = -1;
function selectTab(i: number, focus = false) {
  tabIndex = i;
  tabs.forEach((t, n) => { t.setAttribute('aria-selected', String(n === i)); t.tabIndex = n === i ? 0 : -1; });
  panels.forEach((p, n) => (p.hidden = n !== i));
  infos.forEach((p, n) => (p.hidden = n !== i));
  if (focus) tabs[i].focus();
}
tabs.forEach((t, i) => {
  t.addEventListener('click', () => selectTab(i));
  t.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); selectTab((i + 1) % tabs.length, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); selectTab((i - 1 + tabs.length) % tabs.length, true); }
  });
});
let rotate = 0;
document.querySelectorAll<HTMLButtonElement>('[data-rotate]').forEach((b) => b.addEventListener('click', () => {
  const v = Number(b.dataset.rotate);
  rotate = v === 0 ? 0 : clamp(rotate + v, -60, 60);
  stage?.style.setProperty('--rotate', `${rotate}deg`);
}));

/* ---------- video: dialog + skeleton + fallback error ---------- */
const vdlg = document.getElementById('video-dialog') as HTMLDialogElement | null;
const vbox = vdlg?.querySelector<HTMLElement>('.video-box');
function openVideo(id: string) {
  if (!vdlg || !vbox) return;
  vbox.replaceChildren();
  const watch = `https://www.youtube.com/watch?v=${id}`;
  const loading = document.createElement('div');
  loading.className = 'video-loading';
  loading.innerHTML = '<div class="spinner" role="status" aria-label="Memuat video"></div>';
  const f = document.createElement('iframe');
  f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
  f.title = 'Company Profile MEC Academy';
  f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
  f.className = 'absolute inset-0 h-full w-full';
  let done = false;
  const fail = () => {
    if (done) return; done = true;
    f.remove(); loading.remove();
    const err = document.createElement('div');
    err.className = 'video-error'; err.setAttribute('role', 'alert');
    err.innerHTML = `<p>Video tidak dapat dimuat.</p><a class="btn justify-self-center" href="${watch}" target="_blank" rel="noopener">Tonton di YouTube ↗</a>`;
    vbox.append(err);
  };
  f.addEventListener('load', () => { done = true; loading.remove(); });
  f.addEventListener('error', fail);
  setTimeout(fail, 12000);
  vbox.append(f, loading);
  vdlg.showModal();
  if (!navigator.onLine) fail();
}
document.querySelectorAll<HTMLElement>('[data-video-open]').forEach((b) => b.addEventListener('click', () => openVideo(b.dataset.videoOpen!)));
vdlg?.querySelector('.close-dialog')?.addEventListener('click', () => vdlg.close());
vdlg?.addEventListener('click', (e) => { if (e.target === vdlg) vdlg.close(); });
vdlg?.addEventListener('close', () => vbox?.replaceChildren());

/* ---------- status bab (dot, "01 / 12", progress) — selalu aktif ---------- */
const sections = [...document.querySelectorAll<HTMLElement>('[data-ch]')];
const dots = [...document.querySelectorAll<HTMLAnchorElement>('.chapter-nav a')];
const numEl = document.getElementById('chapter-number');
const titleEl = document.getElementById('chapter-title');
const statusEl = document.querySelector<HTMLElement>('.chapter-status');
let statusActive = -1, statusRaf = 0;
function updateStatus() {
  statusRaf = 0;
  const vh = innerHeight;
  let idx = 0;
  sections.forEach((s, i) => { if (s.getBoundingClientRect().top <= vh * 0.5) idx = i; });
  const r = sections[idx].getBoundingClientRect();
  root.style.setProperty('--local-p', String(clamp((vh * 0.5 - r.top) / Math.max(1, r.height))));
  if (idx !== statusActive) {
    statusActive = idx;
    const total = String(sections.length).padStart(2, '0');
    if (numEl) numEl.textContent = `${String(idx + 1).padStart(2, '0')} / ${total}`;
    if (titleEl) titleEl.textContent = sections[idx].dataset.ch ?? '';
    dots.forEach((d, i) => (i === idx ? d.setAttribute('aria-current', 'true') : d.removeAttribute('aria-current')));
    statusEl?.classList.toggle('on-light', sections[idx].classList.contains('on-paper'));
  }
}
const queueStatus = () => { if (!statusRaf) statusRaf = requestAnimationFrame(updateStatus); };
addEventListener('scroll', queueStatus, { passive: true });
addEventListener('resize', queueStatus);
updateStatus();

/* ---------- koreografi scroll (pinned) ---------- */
interface Ch { el: HTMLElement; id: string; top: number; height: number; p: number; ready: boolean }
let chapters: Ch[] = [];
let active = false;
let raf = 0, last = 0;
let px = 0, py = 0, tx = 0, ty = 0;
let heroBox: { x: number; y: number; width: number; height: number } | null = null;

const rail = document.querySelector<HTMLElement>('[data-rail]');
const railBar = document.querySelector<HTMLElement>('[data-rail-bar]');
const railLabel = document.querySelector<HTMLElement>('[data-rail-label]');
const railCount = document.querySelector<HTMLElement>('[data-rail-count]');
const cards = rail ? ([...rail.children] as HTMLElement[]) : [];

// Heading dipecah per kata; <em> dan <br> dipertahankan (aksen emas).
function splitWords() {
  let n = 0;
  document.querySelectorAll<HTMLElement>('[data-split]').forEach((h) => {
    if (h.dataset.splitDone) return;
    h.dataset.splitDone = '1';
    h.setAttribute('aria-label', (h.textContent ?? '').replace(/\s+/g, ' ').trim());
    n = 0;
    const walk = (node: Node, hl: boolean): Node[] => {
      const out: Node[] = [];
      node.childNodes.forEach((c) => {
        if (c.nodeType === Node.TEXT_NODE) {
          const words = (c.textContent ?? '').split(/\s+/).filter(Boolean);
          words.forEach((w) => {
            const outer = document.createElement('span'); outer.className = hl ? 'wm hl' : 'wm'; outer.setAttribute('aria-hidden', 'true');
            const inner = document.createElement('span'); inner.style.setProperty('--i', String(n++)); inner.textContent = w; outer.append(inner);
            out.push(outer, document.createTextNode(' '));
          });
        } else if (c.nodeName === 'BR') out.push(c.cloneNode());
        else if (c.nodeName === 'EM') out.push(...walk(c, true));
      });
      return out;
    };
    h.replaceChildren(...walk(h, false));
  });
}

function teardown() {
  active = false;
  cancelAnimationFrame(raf); raf = 0;
  root.classList.remove('motion-ready');
  chapters.forEach(({ el }) => { el.classList.remove('motion-scene'); el.removeAttribute('style'); });
  chapters = [];
  ['--px', '--py'].forEach((k) => root.style.removeProperty(k));
}

function setup() {
  teardown();
  const ok = !calm() && motionAllowed({ width: innerWidth, height: innerHeight, reduced: reduced.matches, coarse: coarse.matches, saveData: saveData() });
  if (!ok) return;
  // Chapter hanya di-pin bila kontennya muat dalam satu layar
  const els = [...document.querySelectorAll<HTMLElement>('[data-chapter]')].filter((el) => {
    const inner = el.querySelector<HTMLElement>('.scene-inner');
    return inner ? inner.offsetHeight + 172 <= innerHeight : false;
  });
  if (!els.length) return;
  splitWords();
  els.forEach((el) => { el.style.setProperty('--span', el.dataset.span ?? '1.6'); el.classList.add('motion-scene'); });
  root.classList.add('motion-ready');
  active = true;
  requestAnimationFrame(() => {
    measure(els);
    kick();
  });
}

function measure(els: HTMLElement[]) {
  chapters = els.map((el) => ({ el, id: el.dataset.chapter!, top: el.getBoundingClientRect().top + scrollY, height: el.offsetHeight, p: 0, ready: false }));
  const fr = document.querySelector<HTMLElement>('.hero-frame');
  heroBox = fr ? { x: fr.offsetLeft, y: fr.offsetTop, width: fr.offsetWidth, height: fr.offsetHeight } : null;
  queueStatus();
}

const railLeft = () => rail?.parentElement?.getBoundingClientRect().left ?? 0;
function railGeom() {
  if (!rail || !cards.length) return null;
  const width = cards[0].offsetWidth, gap = 24, track = cards.length * width + (cards.length - 1) * gap;
  return { width, gap, track, viewport: innerWidth - railLeft() };
}

function tick(now: number) {
  raf = 0;
  if (!active) return;
  const dt = last ? now - last : 16; last = now;
  const vh = innerHeight;
  let moving = false;
  for (const c of chapters) {
    const st = chapterState(scrollY, c.top, c.height, vh);
    if (c.ready && (st.local < -vh * 1.3 || st.local > st.travel + vh * 1.3)) continue;
    const target = st.progress;
    c.p = c.ready ? damp(c.p, target, dt) : target;
    c.ready = true;
    if (Math.abs(c.p - target) > 0.0005) moving = true;
    const v = choreography(c.id, c.p, st.enter);
    const s = c.el.style;
    s.setProperty('--enter', st.enter.toFixed(4));
    s.setProperty('--exit', st.exit.toFixed(4));
    for (const [k, val] of Object.entries(v)) s.setProperty(`--${k === 'camX' ? 'camx' : k === 'camY' ? 'camy' : k}`, val.toFixed(4));
    if (c.id === 'hero') {
      const z = zoomPortal(c.p, heroBox, { width: innerWidth, height: vh });
      s.setProperty('--zp', z.progress.toFixed(4)); s.setProperty('--zs', z.scale.toFixed(4));
      s.setProperty('--zx', `${z.x.toFixed(1)}px`); s.setProperty('--zy', `${z.y.toFixed(1)}px`); s.setProperty('--zc', z.caption.toFixed(3));
    }
    if (c.id === 'learning') {
      const g = railGeom();
      if (g) {
        const off = railOffset(c.p, g.track, g.viewport);
        s.setProperty('--rail-x', `${off.toFixed(1)}px`);
        const idx = railIndex(off, g.width, g.gap, cards.length, g.viewport);
        cards.forEach((card, n) => { const d = Math.abs(n - idx); card.style.setProperty('--card-d', String(Math.min(d, 2))); card.style.setProperty('--card-a', String(Math.sign(n - idx) * Math.min(d, 2) * 3)); });
        railBar?.style.setProperty('--rail-p', String(cards.length > 1 ? idx / (cards.length - 1) : 1));
        if (railLabel) railLabel.textContent = cards[idx].dataset.title ?? '';
        if (railCount) railCount.textContent = `0${idx + 1} / 0${cards.length}`;
      }
    }
    if (c.id === 'machine' && panels.length) {
      const i = indexFromProgress(c.p, panels.length);
      if (i !== autoTab) { autoTab = i; if (i !== tabIndex) selectTab(i); }
    }
  }
  px = damp(px, tx, dt, 120); py = damp(py, ty, dt, 120);
  root.style.setProperty('--px', px.toFixed(3)); root.style.setProperty('--py', py.toFixed(3));
  if (Math.abs(px - tx) > 0.001 || Math.abs(py - ty) > 0.001) moving = true;
  const doc = document.documentElement.scrollHeight - vh;
  root.style.setProperty('--page-p', String(doc > 0 ? scrollY / doc : 0));
  if (moving) kick();
}
function kick() { if (active && !raf) raf = requestAnimationFrame(tick); }

addEventListener('scroll', kick, { passive: true });
addEventListener('pointermove', (e) => { if (!active || e.pointerType !== 'mouse') return; tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2; kick(); }, { passive: true });
const safeSetup = () => { try { setup(); } catch (e) { console.error('[mec] animasi dinonaktifkan karena error:', e); teardown(); } };
let resizeT = 0;
addEventListener('resize', () => { clearTimeout(resizeT); resizeT = window.setTimeout(safeSetup, 200); });
addEventListener('mec:motion', safeSetup);
reduced.addEventListener?.('change', safeSetup);
document.fonts?.ready.then(() => active && safeSetup());

/* ---------- rail: tombol prev/next ---------- */
function goRail(dir: number) {
  if (!rail) return;
  if (!active) {
    rail.scrollBy({ left: dir * (cards[0].getBoundingClientRect().width + 24), behavior: reduced.matches ? 'auto' : 'smooth' });
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

/* ---------- animasi pembuka hero ---------- */
function playIntro() {
  if (reduced.matches || calm()) return;
  root.classList.add('intro');
  setTimeout(() => root.classList.remove('intro'), 2000);
}
addEventListener('mec:enter', playIntro);
if (!root.classList.contains('intro-pending')) playIntro();

safeSetup();
