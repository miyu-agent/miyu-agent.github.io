# Miyu 官网

<https://miyu-agent.github.io/>

静态单页，直接打开 `index.html` 即可预览。

## 目录结构

| 路径 | 说明 |
|---|---|
| `index.html` | 组装好的页面，由 `src/build.py` 生成，不要直接手改 |
| `assets/` | 界面截图（`.webp`）、终端集成录屏（`shell.mp4`、`shell-poster.jpg`）与各尺寸 Logo（`assets/logo/`） |
| `src/template.html` | 页面源码 |
| `src/build.py` | 将字符画点阵填入模板，生成 `index.html` |
| `src/mask.b64`、`src/make_mask.sh` | 首页字符画用的 220×220 点阵，以及从 `src/logo.png` 重新生成点阵的脚本（需 ImageMagick、Pillow） |
| `src/logo-v2-source.png`、`src/key_logo.py` | Logo 原图与去底脚本（需 numpy、Pillow） |

## 构建

修改 `src/template.html` 后重新生成 `index.html`：

```sh
python3 src/build.py
```
