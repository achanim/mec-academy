#!/usr/bin/env bash
# Deploy dist/ ke Rumahweb lewat FTPS dari mesin lokal. Lihat docs/CICD.md.
# Kredensial dibaca dari .env.deploy (diabaikan git) atau variabel lingkungan:
#   FTP_HOST, FTP_USER, FTP_PASS   (opsional: FTP_DIR, SITE_URL, SKIP_CHECKS=1, DRY_RUN=1)
set -euo pipefail
cd "$(dirname "$0")/.."

# Dibaca sebagai teks KEY=VALUE (bukan di-source), jadi sandi boleh berisi ; $ # dst.
if [ -f .env.deploy ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|'#'*) continue ;; esac
    key="${line%%=*}"; val="${line#*=}"
    key="${key#export }"
    val="${val%$'\r'}"
    key="${key//[[:space:]]/}"
    val="${val#"${val%%[![:space:]]*}"}"; val="${val%"${val##*[![:space:]]}"}"
    case "$val" in \"*\") val="${val#\"}"; val="${val%\"}" ;; \'*\') val="${val#\'}"; val="${val%\'}" ;; esac
    [ -n "${!key:-}" ] || export "$key=$val"   # variabel lingkungan yang sudah diset diutamakan
  done < .env.deploy
fi

: "${FTP_HOST:?FTP_HOST belum diisi (.env.deploy)}"
: "${FTP_USER:?FTP_USER belum diisi (.env.deploy)}"
: "${FTP_PASS:?FTP_PASS belum diisi (.env.deploy)}"
FTP_DIR="${FTP_DIR:-./}"   # akun FTP dibatasi ke public_html, jadi akar akun = public_html
SITE_URL="${SITE_URL:-https://malangeducationcenter.com}"

command -v lftp >/dev/null || { echo "lftp belum terpasang: brew install lftp" >&2; exit 1; }

if [ "${SKIP_CHECKS:-0}" != 1 ]; then
  echo "==> check + test"
  npm run check
  npm test
fi

echo "==> build"
npm run build
test -f dist/index.html && test -f dist/.htaccess || { echo "dist/ tidak lengkap (index.html/.htaccess)" >&2; exit 1; }

echo "==> unggah dist/ ke ${FTP_HOST}:${FTP_DIR}"
flags="--reverse --only-newer --parallel=2 --no-perms"
[ "${DRY_RUN:-0}" = 1 ] && flags="$flags --dry-run"
# Tanpa --delete: berkas yang dihapus dari build tidak ikut terhapus di server.
# Sandi tidak boleh muncul di log: samarkan URL kredensial pada keluaran.
lftp -u "$FTP_USER","$FTP_PASS" "$FTP_HOST" 2>&1 <<EOF | sed -E 's#(ftps?://)[^@]*@#\1***@#g'
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ftp:passive-mode true
set net:timeout 30
set net:max-retries 3
set net:connection-limit 2
set net:reconnect-interval-base 5
lcd dist
cd "$FTP_DIR"
mirror $flags . .
bye
EOF

[ "${DRY_RUN:-0}" = 1 ] && { echo "DRY_RUN: tidak ada yang diunggah."; exit 0; }

echo "==> uji asap"
code=000
for i in 1 2 3 4 5; do
  code=$(curl -s -o /tmp/mec-home.html -w '%{http_code}' "$SITE_URL/" || true)
  if [ "$code" = 200 ] && grep -q "MEC Academy" /tmp/mec-home.html; then break; fi
  echo "percobaan $i: HTTP $code, ulangi..."; sleep 5
done
[ "$code" = 200 ] || { echo "GAGAL: beranda HTTP $code" >&2; exit 1; }
for p in /faq/ /organisasi/; do
  r=$(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL$p")
  echo "$p -> $r"
done
echo "Selesai."
