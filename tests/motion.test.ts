import { describe, it, expect } from 'vitest';
import { smooth, clamp, chapterState, railOffset, railProgress, railIndex, motionAllowed, indexFromProgress, choreography, bump } from '../src/scripts/motion';

describe('motion math', () => {
  it('smooth clamps and is monotonic', () => {
    expect(smooth(0, 1, -1)).toBe(0);
    expect(smooth(0, 1, 2)).toBe(1);
    expect(smooth(0, 1, 0.5)).toBeCloseTo(0.5);
    expect(smooth(0, 1, 0.3)).toBeLessThan(smooth(0, 1, 0.6));
  });
  it('chapterState progress spans the pinned travel', () => {
    const vh = 900, top = 1000, h = vh * 2.5;
    expect(chapterState(top, top, h, vh).progress).toBe(0);
    expect(chapterState(top + (h - vh), top, h, vh).progress).toBe(1);
    expect(chapterState(top - 2000, top, h, vh).enter).toBe(0);
    expect(chapterState(top, top, h, vh).enter).toBe(1);
  });
  it('rail progress round-trips with offset/index', () => {
    const count = 4, w = 700, gap = 24, vw = 1400, track = count * w + (count - 1) * gap;
    for (let i = 0; i < count; i++) {
      const p = railProgress(i, count, w, gap, track, vw);
      expect(railIndex(railOffset(p, track, vw), w, gap, count, vw)).toBe(i);
    }
    expect(railOffset(0, track, vw)).toBe(-0);
  });
  it('motionAllowed gates on env', () => {
    const ok = { width: 1440, height: 900, reduced: false, coarse: false, saveData: false };
    expect(motionAllowed(ok)).toBe(true);
    expect(motionAllowed({ ...ok, reduced: true })).toBe(false);
    expect(motionAllowed({ ...ok, coarse: true })).toBe(false);
    expect(motionAllowed({ ...ok, width: 800 })).toBe(false);
  });
  it('indexFromProgress stays in range', () => {
    expect(indexFromProgress(0, 4)).toBe(0);
    expect(indexFromProgress(1, 4)).toBe(3);
    expect(indexFromProgress(0.5, 4)).toBe(2);
  });
  it('choreography exposes hero + character values', () => {
    expect(choreography('hero', 1, 1).frame).toBe(1);
    expect(choreography('character', 0.9, 1).prayer).toBeCloseTo(1, 1);
    expect(bump(0, 0.1, 0.5)).toBe(0);
    expect(clamp(5)).toBe(1);
  });
});
