"""去洋红底：纯洋红→透明；边缘按绿色通道算透明度，颜色取附近不透明像素的颜色，不留粉边。"""
import sys
from PIL import Image; import numpy as np
P = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
s = (np.minimum(P[..., 0], P[..., 2]) - P[..., 1]) / 255          # 洋红程度
bg = s > 0.9
def grow(m, n):                                                      # 二值膨胀 n 像素
    m = m.copy()
    for _ in range(n):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m
band = grow(bg, 3) & ~bg                                             # 边缘带
core = ~bg & ~band
def boxsum(x, r):
    c = np.cumsum(np.cumsum(np.pad(x, ((r + 1, r), (r + 1, r)) + ((0, 0),) * (x.ndim - 2)), 0), 1)
    return c[2*r+1:, 2*r+1:] - c[:-2*r-1, 2*r+1:] - c[2*r+1:, :-2*r-1] + c[:-2*r-1, :-2*r-1]
r = 6
F = boxsum(P * core[..., None], r) / np.maximum(boxsum(core.astype(float), r), 1e-6)[..., None]
alpha = np.ones(P.shape[:2])
alpha[bg] = 0
a_band = np.clip(P[..., 1] / np.maximum(F[..., 1], 1), 0, 1)
alpha[band] = a_band[band]
out = P.copy(); out[band] = F[band]
tint = ~bg & (out[..., 2] > out[..., 1] + 2) & (out[..., 0] > out[..., 1] + 2)   # 残留的洋红色偏：蓝压到绿
out[..., 2] = np.where(tint, out[..., 1], out[..., 2])
out[bg] = F[band].mean(0)                                            # 透明处填边缘色，缩放时不渗出洋红
rgba = np.dstack([out, alpha * 255]).round().clip(0, 255).astype(np.uint8)
im = Image.fromarray(rgba, 'RGBA')
# 裁到内容、放回正方形画布中央，四周留 4%
x0, y0, x1, y1 = im.getbbox(); w, h = x1 - x0, y1 - y0
side = int(max(w, h) * 1.08)
canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
canvas.paste(im.crop((x0, y0, x1, y1)), ((side - w) // 2, (side - h) // 2))
canvas.save(sys.argv[2])
print('bbox', (x0, y0, x1, y1), 'canvas', side, 'band px', band.sum(), 'tinted fixed', tint.sum())
