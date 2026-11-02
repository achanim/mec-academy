/**
 * Foto header per modul (opsional). Kunci = alamat modul (slug), mis. 'basic-safety'.
 * Nama berkas (image) = nama foto di src/assets/images tanpa .jpg, mis. 'safety' untuk safety.jpg.
 * Modul yang tidak ada di daftar ini memakai foto bawaan (workshop). Modul sistem (diesel-engine, dst.)
 * otomatis memakai foto dari src/data/systems.ts kecuali diisi di sini.
 */
export const moduleImages: Record<string, { image: string; alt: string }> = {
  // 'basic-safety': { image: 'safety', alt: 'Siswa MEC mempelajari keselamatan kerja' },
};
