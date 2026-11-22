<p align="center">
  <a href="README.md">English</a> | 简体中文
</p>

# Miyu 官网

> <sub>本文档由 Anthropic 的 Claude Fable 5.2 生成。</sub>

这个仓库是 Miyu 官网的源码，官网地址是 <https://miyu-agent.github.io/>。

官网是一个静态的单页网站，直接打开 `index.html` 即可预览。

## 目录结构

下表说明仓库里各个文件和目录的作用：

| 路径 | 说明 |
|---|---|
| `index.html` | 已经组装完成的页面，由 `src/build.py` 生成，不要直接手动修改 |
| `assets/` | 界面截图（`.webp`）、终端集成功能的录屏（`shell.mp4`、`shell-poster.jpg`），以及各种尺寸的标志图片（`assets/logo/`） |
| `src/template.html` | 页面的源码 |
| `src/build.py` | 把字符画的点阵填入模板，生成 `index.html` |
| `src/mask.b64`、`src/make_mask.sh` | 首页字符画使用的 220×220 点阵，以及从 `src/logo.png` 重新生成点阵的脚本（需要 ImageMagick 和 Pillow） |
| `src/logo-v2-source.png`、`src/key_logo.py` | 标志的原图，以及去掉背景的脚本（需要 NumPy 和 Pillow） |

## 构建

修改 `src/template.html` 以后，运行下面的命令重新生成 `index.html`：

```sh
python3 src/build.py
```
