import { describe, it, expect } from 'vitest';
import { slugify, modules } from '../src/lib/site';

describe('slugify', () => {
  it('normalizes module titles', () => {
    expect(slugify('Basic tools & equipment')).toBe('basic-tools-dan-equipment');
    expect(slugify('Aksesoris (AC - ALS) & safety')).toBe('aksesoris-ac-als-dan-safety');
  });
});
describe('modules', () => {
  it('has 16 unique slugs', () => {
    expect(modules).toHaveLength(16);
    expect(new Set(modules.map((m) => m.slug)).size).toBe(16);
  });
});
