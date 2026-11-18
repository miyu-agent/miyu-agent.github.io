#!/usr/bin/env python3
"""把 src/template.html 组装成可以直接打开的 index.html。

template.html 里有一个占位：__MASK__（字符画用的 220×220 点阵，来自 mask.b64，由 make_mask.sh 生成）。
"""
import pathlib

src = pathlib.Path(__file__).resolve().parent
root = src.parent
page = (src / "template.html").read_text().replace("__MASK__", (src / "mask.b64").read_text().strip())
# everything above the first <canvas> (title, icons, fonts, the stylesheet) belongs in <head>
cut = page.index("\n<canvas")
head = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}</style>\n' + page[:cut] + '\n</head>\n<body>')
(root / "index.html").write_text(head + page[cut:] + "\n</body>\n</html>\n")
print("wrote", root / "index.html")
