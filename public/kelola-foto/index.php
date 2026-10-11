<?php
/**
 * Pintu masuk pengelola foto alumni. Sengaja ditulis dengan sintaks lama (kompatibel PHP 5.6+),
 * supaya pada PHP < 8.1 tampil pesan yang jelas, bukan HTTP 500 kosong. Aplikasi sebenarnya ada di app.php (butuh PHP 8.1+).
 */
$problems = array();
if (version_compare(PHP_VERSION, '8.1.0', '<')) {
    $problems[] = 'Versi PHP di server ini ' . PHP_VERSION . '; pengelola foto membutuhkan <b>PHP 8.1 atau lebih baru</b>. Di cPanel buka <b>MultiPHP Manager</b>, pilih domain ini, lalu ganti versi PHP ke 8.1 atau lebih tinggi (mis. ea-php83).';
}
if (!extension_loaded('gd') || !function_exists('imagecreatetruecolor')) {
    $problems[] = 'Ekstensi PHP <b>GD</b> (pengolah gambar) belum aktif. Di cPanel buka <b>MultiPHP INI Editor</b> atau <b>Select PHP Version &gt; Extensions</b>, aktifkan <code>gd</code>.';
}
if (!function_exists('random_bytes') || !function_exists('password_hash')) {
    $problems[] = 'Fungsi keamanan PHP (random_bytes/password_hash) tidak tersedia; perbarui versi PHP.';
}
if ($problems) {
    http_response_code(503);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Robots-Tag: noindex, nofollow, noarchive');
    header('Cache-Control: no-store');
    echo '<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>Server belum siap</title>'
       . '<style>body{font:16px/1.5 system-ui,sans-serif;background:#f4f1e8;color:#061f23;margin:0}main{max-width:640px;margin:40px auto;padding:0 20px}.c{background:#fff;border:1px solid #d9d4c3;border-radius:6px;padding:20px}li{margin:0 0 10px}</style></head><body><main><div class="c"><h1 style="font-size:22px;margin:0 0 10px">Server belum siap</h1><p>Pengelola foto belum bisa berjalan:</p><ul>';
    foreach ($problems as $p) echo '<li>' . $p . '</li>';
    echo '</ul><p style="color:#5b6b6c;font-size:14px">Setelah memperbaiki, muat ulang halaman ini. Foto dan pengaturan yang sudah ada tidak berubah.</p></div></main></body></html>';
    exit;
}
require __DIR__ . '/app.php';
