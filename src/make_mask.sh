#!/usr/bin/env bash
# 从 logo.png（旧 logo，白底黑剪影）重新生成 mask.b64（首页字符画点阵，220×220 一格一位）。
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp --suffix=.pbm); trap 'rm -f "$tmp"' EXIT
magick logo.png -colorspace gray -threshold 50% "$tmp"
python3 - "$tmp" <<'PY'
import base64, sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('L')
x0, y0, x1, y1 = Image.eval(im, lambda v: 255 - v).getbbox()
s = max(x1 - x0, y1 - y0); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
box = (int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))
m = im.crop(box).resize((220, 220), Image.LANCZOS); px = m.load()
bits = bytearray(); acc = n = 0
for y in range(220):
    for x in range(220):
        acc = (acc << 1) | (1 if px[x, y] < 128 else 0); n += 1
        if n == 8: bits.append(acc); acc = n = 0
open('mask.b64', 'w').write(base64.b64encode(bytes(bits)).decode())
PY
echo "mask.b64 updated"
