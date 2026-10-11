<?php
/**
 * Pengelola foto halaman Alumni (khusus admin MEC). Tidak ditautkan dari situs mana pun, tidak masuk sitemap, noindex.
 * - Foto disimpan di ../alumni-foto/ (di luar build, jadi tidak tertimpa saat deploy); daftar ada di manifest.json.
 * - Kata sandi disimpan sebagai hash di config.php (dibuat di server lewat penyiapan awal; tidak ada di repo).
 * Panduan: docs/ALUMNI-ADMIN.md
 */
declare(strict_types=1);

const MAX_PHOTOS = 80;          // batas jumlah foto di galeri
const MAX_FILES_PER_UPLOAD = 20;
const MAX_UPLOAD_BYTES = 15 * 1024 * 1024;
const MAX_PIXELS = 60000000;    // cegah gambar raksasa menghabiskan memori
const FULL_EDGE = 2000;         // sisi terpanjang foto besar (px)
const THUMB_EDGE = 640;         // sisi terpanjang thumbnail (px)
const SESSION_IDLE = 7200;      // keluar otomatis setelah 2 jam tak aktif
const MAX_FAILS = 5;            // salah sandi sebelum dikunci
const LOCK_SECONDS = 900;       // lama penguncian (15 menit)

$docroot = dirname(__DIR__);
$galleryDir = $docroot . '/alumni-foto';
$manifestFile = $galleryDir . '/manifest.json';
$dataDir = __DIR__ . '/data';
$configFile = __DIR__ . '/config.php';
$setupFlag = __DIR__ . '/BUAT-SANDI.txt';
$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
$self = $_SERVER['SCRIPT_NAME'] ?? 'index.php';

header('X-Robots-Tag: noindex, nofollow, noarchive');
header('Cache-Control: no-store');
header('X-Frame-Options: DENY');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'");

session_name('mecadm');
session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => $https, 'httponly' => true, 'samesite' => 'Strict']);
session_start();
if (isset($_SESSION['last']) && time() - $_SESSION['last'] > SESSION_IDLE) { $_SESSION = []; session_regenerate_id(true); }
$_SESSION['last'] = time();
if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function flash(string $type, string $msg): void { $_SESSION['flash'][] = [$type, $msg]; }
function redirect(): never { global $self; header('Location: ' . $self, true, 303); exit; }
function csrf_ok(): bool { return isset($_POST['csrf'], $_SESSION['csrf']) && hash_equals((string)$_SESSION['csrf'], (string)$_POST['csrf']); }
function ensure_dir(string $d, int $mode = 0755): void { if (!is_dir($d) && !@mkdir($d, $mode, true) && !is_dir($d)) throw new RuntimeException('Tidak bisa membuat folder.'); }
function csrf_field(): string { return '<input type="hidden" name="csrf" value="' . h((string)$_SESSION['csrf']) . '">'; }

function render(string $title, string $body, bool $loggedIn = false): never {
    global $self;
    $flash = '';
    foreach ($_SESSION['flash'] ?? [] as [$t, $m]) $flash .= '<p class="msg ' . h($t) . '">' . h($m) . '</p>';
    unset($_SESSION['flash']);
    $bar = '<header><b>MEC Academy · Kelola foto alumni</b><span>'
         . ($loggedIn ? '<a href="/alumni/" target="_blank" rel="noopener">Lihat halaman alumni</a> · <form method="post" action="' . h($self) . '" style="display:inline">' . csrf_field() . '<input type="hidden" name="action" value="logout"><button type="submit">Keluar</button></form>' : '')
         . '</span></header>';
    echo '<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive">'
       . '<title>' . h($title) . '</title><style>'
       . ':root{--ink:#061f23;--green:#265154;--gold:#cdbe86;--paper:#f4f1e8;--bad:#b3261e;--ok:#1f7a3f}*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--paper);color:var(--ink)}'
       . 'header{background:var(--ink);color:#fff;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}header a,header button{color:var(--gold);background:none;border:0;font:inherit;cursor:pointer;text-decoration:underline;padding:0}'
       . 'main{max-width:960px;margin:0 auto;padding:20px}.card{background:#fff;border:1px solid #d9d4c3;padding:18px;margin:0 0 18px;border-radius:6px}h1{font-size:22px;margin:0 0 6px}h2{font-size:18px;margin:0 0 10px}'
       . '.msg{padding:10px 14px;border-radius:6px;margin:0 0 12px}.msg.ok{background:#e2f3e8;color:var(--ok)}.msg.err{background:#fbe5e3;color:var(--bad)}.muted{color:#5b6b6c;font-size:14px}'
       . 'input[type=text],input[type=password],input[type=file]{width:100%;padding:10px;border:1px solid #8a9a9a;border-radius:6px;font:inherit;background:#fff}'
       . '.btn{display:inline-block;padding:10px 18px;border:0;border-radius:6px;background:var(--green);color:#fff;font:inherit;font-weight:600;cursor:pointer}.btn.sec{background:#e8e3d2;color:var(--ink)}.btn.bad{background:var(--bad)}'
       . '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}.item{border:1px solid #d9d4c3;border-radius:6px;overflow:hidden;background:#fff}.item img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#ddd}'
       . '.item .in{padding:10px;display:grid;gap:8px}.row{display:flex;gap:8px;flex-wrap:wrap}.row form{margin:0}label{font-weight:600;display:block;margin:0 0 6px}'
       . '</style></head><body>' . $bar . '<main>' . $flash . $body . '</main></body></html>';
    exit;
}

// ---------- manifest ----------
function gallery_init(): void {
    global $galleryDir;
    ensure_dir($galleryDir); ensure_dir($galleryDir . '/img'); ensure_dir($galleryDir . '/thumb');
    $ht = $galleryDir . '/.htaccess';
    if (!is_file($ht)) file_put_contents($ht, "# Folder foto: hanya gambar dan manifest; tidak ada eksekusi skrip\nOptions -Indexes -ExecCGI\n<FilesMatch \"\\.(php[0-9]?|phtml|phar|pl|py|cgi|sh|html?)\$\">\n  Require all denied\n</FilesMatch>\n<IfModule mod_headers.c>\n  <FilesMatch \"manifest\\.json\$\">\n    Header set Cache-Control \"no-cache\"\n  </FilesMatch>\n  Header set X-Content-Type-Options \"nosniff\"\n</IfModule>\n");
}
function manifest_read(): array {
    global $manifestFile;
    $d = is_file($manifestFile) ? json_decode((string)file_get_contents($manifestFile), true) : null;
    return is_array($d) && isset($d['items']) && is_array($d['items']) ? $d : ['updated' => gmdate('c'), 'items' => []];
}
/** Jalankan perubahan manifest secara eksklusif (flock) dan tulis atomik. */
function manifest_update(callable $fn): void {
    global $galleryDir, $manifestFile;
    gallery_init();
    $lock = fopen($galleryDir . '/.lock', 'c');
    if (!$lock || !flock($lock, LOCK_EX)) throw new RuntimeException('Tidak bisa mengunci data.');
    try {
        $m = manifest_read();
        $m = $fn($m);
        $m['updated'] = gmdate('c');
        $tmp = $manifestFile . '.tmp';
        file_put_contents($tmp, json_encode($m, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
        rename($tmp, $manifestFile);
    } finally { flock($lock, LOCK_UN); fclose($lock); }
}

// ---------- pengolahan gambar ----------
function load_image(string $tmp): array|string {
    $info = @getimagesize($tmp);
    if ($info === false) return 'bukan gambar yang valid';
    [$w, $h, $type] = $info;
    if (!in_array($type, [IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_WEBP], true)) return 'format harus JPG, PNG, atau WebP (foto HEIC iPhone: ubah dulu ke JPG)';
    if ($w < 300 || $h < 200) return 'terlalu kecil (minimal 300×200 px)';
    if ($w * $h > MAX_PIXELS) return 'resolusi terlalu besar (maksimal ±60 megapiksel)';
    @ini_set('memory_limit', '768M');
    $src = match ($type) {
        IMAGETYPE_JPEG => @imagecreatefromjpeg($tmp),
        IMAGETYPE_PNG => @imagecreatefrompng($tmp),
        IMAGETYPE_WEBP => function_exists('imagecreatefromwebp') ? @imagecreatefromwebp($tmp) : false,
    };
    if (!$src) return 'gagal dibaca (file rusak atau format tidak didukung server)';
    if ($type === IMAGETYPE_JPEG && function_exists('exif_read_data')) {   // putar sesuai orientasi kamera
        $ex = @exif_read_data($tmp);
        $deg = match ((int)($ex['Orientation'] ?? 1)) { 3 => 180, 6 => -90, 8 => 90, default => 0 };
        if ($deg !== 0) { $rot = imagerotate($src, $deg, 0); if ($rot) { imagedestroy($src); $src = $rot; } }
    }
    return [$src, imagesx($src), imagesy($src)];
}
function save_scaled(GdImage $src, int $sw, int $sh, int $edge, string $path, int $quality): array {
    $scale = min(1.0, $edge / max($sw, $sh));
    $nw = max(1, (int)round($sw * $scale)); $nh = max(1, (int)round($sh * $scale));
    $dst = imagecreatetruecolor($nw, $nh);
    imagefill($dst, 0, 0, imagecolorallocate($dst, 255, 255, 255));   // PNG transparan → latar putih
    imagecopyresampled($dst, $src, 0, 0, 0, 0, $nw, $nh, $sw, $sh);
    imageinterlace($dst, true);
    $ok = imagejpeg($dst, $path, $quality);   // dienkode ulang: metadata EXIF dan muatan tersembunyi hilang
    imagedestroy($dst);
    if (!$ok) throw new RuntimeException('Gagal menyimpan gambar.');
    return [$nw, $nh];
}
function remove_files(array $it): void {
    global $galleryDir;
    foreach (['file', 'thumb'] as $k) {
        $f = (string)($it[$k] ?? '');
        if (preg_match('#^(img|thumb)/[a-f0-9]{16}\.jpg$#', $f)) @unlink($galleryDir . '/' . $f);
    }
}

// ---------- pembatasan percobaan masuk ----------
function attempts_file(): string { global $dataDir; ensure_dir($dataDir, 0750); $ht = $dataDir . '/.htaccess'; if (!is_file($ht)) file_put_contents($ht, "Require all denied\n"); return $dataDir . '/attempts.json'; }
function attempts_get(): array { $f = attempts_file(); $d = is_file($f) ? json_decode((string)file_get_contents($f), true) : []; return is_array($d) ? $d : []; }
function attempts_put(array $d): void { $now = time(); foreach ($d as $k => $v) if (($v['until'] ?? 0) < $now && ($v['t'] ?? 0) < $now - 3600) unset($d[$k]); file_put_contents(attempts_file(), json_encode($d), LOCK_EX); }
function client_key(): string { return hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '?')); }

$config = is_file($configFile) ? (include $configFile) : null;
$action = $_SERVER['REQUEST_METHOD'] === 'POST' ? (string)($_POST['action'] ?? '') : '';

try {
    // ===== penyiapan awal: hanya bila config.php belum ada DAN admin membuat berkas BUAT-SANDI.txt lewat File Manager =====
    if (!is_array($config) || empty($config['hash'])) {
        if (!is_file($setupFlag)) {
            http_response_code(503);
            render('Belum disiapkan', '<div class="card"><h1>Belum disiapkan</h1><p>Untuk membuat kata sandi pertama kali, buat berkas kosong bernama <code>BUAT-SANDI.txt</code> di folder ini lewat File Manager cPanel, lalu muat ulang halaman. Panduan ada di <code>docs/ALUMNI-ADMIN.md</code>.</p></div>');
        }
        if ($action === 'setup') {
            $p1 = (string)($_POST['p1'] ?? ''); $p2 = (string)($_POST['p2'] ?? '');
            if (!csrf_ok()) flash('err', 'Sesi tidak valid, coba lagi.');
            elseif (mb_strlen($p1) < 12) flash('err', 'Kata sandi minimal 12 karakter.');
            elseif (!hash_equals($p1, $p2)) flash('err', 'Kedua isian kata sandi tidak sama.');
            else {
                file_put_contents($configFile, "<?php\nreturn " . var_export(['hash' => password_hash($p1, PASSWORD_DEFAULT)], true) . ";\n", LOCK_EX);
                @chmod($configFile, 0600); @unlink($setupFlag);
                flash('ok', 'Kata sandi tersimpan. Berkas BUAT-SANDI.txt sudah dihapus. Silakan masuk.');
            }
            redirect();
        }
        render('Buat kata sandi', '<div class="card"><h1>Buat kata sandi admin</h1><p class="muted">Dipakai untuk masuk ke halaman ini. Minimal 12 karakter; simpan di pengelola sandi.</p><form method="post" action="' . h($self) . '">' . csrf_field() . '<input type="hidden" name="action" value="setup"><p><label>Kata sandi</label><input type="password" name="p1" required minlength="12" autocomplete="new-password"></p><p><label>Ulangi kata sandi</label><input type="password" name="p2" required minlength="12" autocomplete="new-password"></p><button class="btn" type="submit">Simpan</button></form></div>');
    }

    // ===== masuk =====
    if (empty($_SESSION['auth'])) {
        if ($action === 'login') {
            $key = client_key(); $att = attempts_get(); $now = time();
            if (($att[$key]['until'] ?? 0) > $now) { flash('err', 'Terlalu banyak percobaan. Coba lagi beberapa menit lagi.'); redirect(); }
            if (csrf_ok() && password_verify((string)($_POST['password'] ?? ''), (string)$config['hash'])) {
                unset($att[$key]); attempts_put($att);
                session_regenerate_id(true); $_SESSION['auth'] = true; $_SESSION['csrf'] = bin2hex(random_bytes(32));
            } else {
                $n = (int)($att[$key]['n'] ?? 0) + 1;
                $att[$key] = ['n' => $n, 't' => $now, 'until' => $n >= MAX_FAILS ? $now + LOCK_SECONDS : 0];
                if ($n >= MAX_FAILS) $att[$key]['n'] = 0;
                attempts_put($att); usleep(400000);
                flash('err', 'Kata sandi salah.');
            }
            redirect();
        }
        render('Masuk', '<div class="card"><h1>Masuk</h1><form method="post" action="' . h($self) . '">' . csrf_field() . '<input type="hidden" name="action" value="login"><p><label>Kata sandi</label><input type="password" name="password" required autocomplete="current-password" autofocus></p><button class="btn" type="submit">Masuk</button></form></div>');
    }

    // ===== sudah masuk: aksi =====
    if ($action !== '') {
        if (!csrf_ok()) { flash('err', 'Sesi tidak valid, muat ulang halaman.'); redirect(); }
        if ($action === 'logout') { $_SESSION = []; session_regenerate_id(true); redirect(); }

        if ($action === 'upload') {
            gallery_init();
            $files = $_FILES['photos'] ?? null;
            if (!$files || !is_array($files['name'] ?? null)) { flash('err', 'Pilih foto dulu.'); redirect(); }
            $names = $files['name']; $count = count($names);
            if ($count > MAX_FILES_PER_UPLOAD) { flash('err', 'Maksimal ' . MAX_FILES_PER_UPLOAD . ' foto sekali unggah.'); redirect(); }
            $added = []; $errs = [];
            for ($i = 0; $i < $count; $i++) {
                $label = mb_substr(basename((string)$names[$i]), 0, 60);
                $err = (int)$files['error'][$i];
                if ($err === UPLOAD_ERR_NO_FILE) continue;
                if ($err === UPLOAD_ERR_INI_SIZE || $err === UPLOAD_ERR_FORM_SIZE) { $errs[] = "$label: melebihi batas ukuran server (" . ini_get('upload_max_filesize') . ')'; continue; }
                if ($err !== UPLOAD_ERR_OK || !is_uploaded_file((string)$files['tmp_name'][$i])) { $errs[] = "$label: unggahan gagal"; continue; }
                if ((int)$files['size'][$i] > MAX_UPLOAD_BYTES) { $errs[] = "$label: lebih dari 15 MB"; continue; }
                $img = load_image((string)$files['tmp_name'][$i]);
                if (is_string($img)) { $errs[] = "$label: $img"; continue; }
                [$src, $sw, $sh] = $img;
                $id = bin2hex(random_bytes(8));
                try {
                    [$w, $hh] = save_scaled($src, $sw, $sh, FULL_EDGE, $galleryDir . "/img/$id.jpg", 82);
                    save_scaled($src, $sw, $sh, THUMB_EDGE, $galleryDir . "/thumb/$id.jpg", 78);
                } catch (Throwable $e) { $errs[] = "$label: " . $e->getMessage(); imagedestroy($src); continue; }
                imagedestroy($src);
                $cap = trim(preg_replace('/\.[^.]+$/', '', $label) ?? '');
                $added[] = ['id' => $id, 'file' => "img/$id.jpg", 'thumb' => "thumb/$id.jpg", 'w' => $w, 'h' => $hh, 'caption' => '', 'added' => gmdate('c')];
            }
            if ($added) {
                $overflow = [];
                manifest_update(function (array $m) use ($added, &$overflow) {
                    foreach ($added as $a) { if (count($m['items']) >= MAX_PHOTOS) { $overflow[] = $a; continue; } $m['items'][] = $a; }
                    return $m;
                });
                foreach ($overflow as $o) { remove_files($o); $errs[] = 'Galeri penuh (maksimal ' . MAX_PHOTOS . ' foto); hapus beberapa foto dulu.'; }
                $ok = count($added) - count($overflow);
                if ($ok > 0) flash('ok', "$ok foto ditambahkan. Isi keterangan di bawah bila perlu.");
            }
            foreach ($errs as $e) flash('err', $e);
            if (!$added && !$errs) flash('err', 'Tidak ada foto yang dipilih.');
            redirect();
        }

        $id = (string)($_POST['id'] ?? '');
        if (!preg_match('/^[a-f0-9]{16}$/', $id)) { flash('err', 'Foto tidak dikenal.'); redirect(); }
        if ($action === 'caption') {
            $cap = trim(mb_substr(preg_replace('/\s+/u', ' ', (string)($_POST['caption'] ?? '')) ?? '', 0, 140));
            manifest_update(function (array $m) use ($id, $cap) { foreach ($m['items'] as &$it) if ($it['id'] === $id) $it['caption'] = $cap; unset($it); return $m; });
            flash('ok', 'Keterangan disimpan.'); redirect();
        }
        if ($action === 'move') {
            $dir = ($_POST['dir'] ?? '') === 'up' ? -1 : 1;
            manifest_update(function (array $m) use ($id, $dir) {
                $items = array_values($m['items']);
                foreach ($items as $i => $it) if ($it['id'] === $id) { $j = $i + $dir; if ($j >= 0 && $j < count($items)) { [$items[$i], $items[$j]] = [$items[$j], $items[$i]]; } break; }
                $m['items'] = $items; return $m;
            });
            redirect();
        }
        if ($action === 'delete') {
            $gone = null;
            manifest_update(function (array $m) use ($id, &$gone) {
                $keep = [];
                foreach ($m['items'] as $it) { if ($it['id'] === $id) $gone = $it; else $keep[] = $it; }
                $m['items'] = $keep; return $m;
            });
            if ($gone) { remove_files($gone); flash('ok', 'Foto dihapus.'); } else flash('err', 'Foto tidak ditemukan.');
            redirect();
        }
        flash('err', 'Perintah tidak dikenal.'); redirect();
    }

    // ===== halaman utama =====
    $m = manifest_read(); $items = array_values($m['items']); $n = count($items);
    $b = '<div class="card"><h1>Foto halaman Alumni</h1><p class="muted">Foto yang diunggah di sini otomatis tampil di halaman Alumni situs (perlu muat ulang halaman Alumni). Ada ' . $n . ' dari maksimal ' . MAX_PHOTOS . ' foto. Jika galeri kosong, halaman Alumni menampilkan foto bawaan.</p></div>';
    $b .= '<div class="card"><h2>Tambah foto</h2><form method="post" action="' . h($self) . '" enctype="multipart/form-data">' . csrf_field() . '<input type="hidden" name="action" value="upload">'
        . '<p><input type="file" name="photos[]" accept="image/jpeg,image/png,image/webp" multiple required></p>'
        . '<p class="muted">Format JPG, PNG, atau WebP; maksimal ' . MAX_FILES_PER_UPLOAD . ' foto sekali unggah, masing-masing ≤ 15 MB (batas server: ' . h((string)ini_get('upload_max_filesize')) . ' per berkas, ' . h((string)ini_get('post_max_size')) . ' per unggahan). Foto otomatis diperkecil dan dirapikan. Pastikan alumni yang tampil sudah memberi izin.</p>'
        . '<button class="btn" type="submit">Unggah</button></form></div>';
    $b .= '<div class="card"><h2>Foto saat ini</h2>';
    if (!$n) $b .= '<p class="muted">Belum ada foto yang diunggah.</p>';
    else {
        $b .= '<p class="muted">Urutan di sini = urutan di halaman Alumni (paling atas tampil pertama).</p><div class="grid">';
        foreach ($items as $i => $it) {
            $id = (string)$it['id'];
            $b .= '<div class="item"><img src="/alumni-foto/' . h((string)$it['thumb']) . '" alt="" loading="lazy"><div class="in">'
                . '<form method="post" action="' . h($self) . '">' . csrf_field() . '<input type="hidden" name="action" value="caption"><input type="hidden" name="id" value="' . h($id) . '"><label>Keterangan</label><input type="text" name="caption" maxlength="140" value="' . h((string)($it['caption'] ?? '')) . '" placeholder="mis. Alumni BMC 52 di lokasi OJT"><p style="margin:8px 0 0"><button class="btn sec" type="submit">Simpan keterangan</button></p></form>'
                . '<div class="row">'
                . ($i > 0 ? '<form method="post" action="' . h($self) . '">' . csrf_field() . '<input type="hidden" name="action" value="move"><input type="hidden" name="id" value="' . h($id) . '"><input type="hidden" name="dir" value="up"><button class="btn sec" type="submit" title="Naikkan">↑ Naik</button></form>' : '')
                . ($i < $n - 1 ? '<form method="post" action="' . h($self) . '">' . csrf_field() . '<input type="hidden" name="action" value="move"><input type="hidden" name="id" value="' . h($id) . '"><input type="hidden" name="dir" value="down"><button class="btn sec" type="submit" title="Turunkan">↓ Turun</button></form>' : '')
                . '<form method="post" action="' . h($self) . '" onsubmit="return confirm(\'Hapus foto ini dari halaman Alumni?\')">' . csrf_field() . '<input type="hidden" name="action" value="delete"><input type="hidden" name="id" value="' . h($id) . '"><button class="btn bad" type="submit">Hapus</button></form>'
                . '</div></div></div>';
        }
        $b .= '</div>';
    }
    $b .= '</div>';
    render('Kelola foto alumni', $b, true);
} catch (Throwable $e) {
    error_log('kelola-foto: ' . $e->getMessage());
    http_response_code(500);
    render('Terjadi kesalahan', '<div class="card"><h1>Terjadi kesalahan</h1><p>Perubahan belum tersimpan. Coba lagi; bila berulang, hubungi pengembang.</p></div>', !empty($_SESSION['auth']));
}
