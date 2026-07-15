<p align="center">
  <img src="laoa-lego/assets/viewer/assets/brickmorph-icon-64.png" width="64" height="64" alt="LaoA-Lego skill 图标">
</p>

# LaoA-Lego skill

**版本 0.5**

`$laoa-lego` 可以把关键词或参考图片转换成高辨识度的乐高风格三维积木模型，并生成一个可独立运行的交互网页。

0.5 版本重点解决人物模型“表面很细、结构却很弱”的问题。技能现在默认先构建少量但有明确意义的三维造型体，让头部、躯干、关节、手掌、手指、鞋和配件都保持清楚的积木分段；只有像素画、马赛克、文字和近似平面的薄线细节才使用 `explicit-bricks-v1`。

## 0.5 版本更新

- 完整三维人物、机器人、载具和生物默认优先使用 `primitives-v1`。
- 禁止用单个球体或椭球体代替手掌、拳头或脚掌。
- 人物双手必须拆分为掌心、拇指、指块或指节等独立结构。
- 概念图必须展示可实现的积木层级、关节和手部构造，不能只追求微积木表面平滑度。
- 新增人物结构检查：检查器会识别未分段的手部和圆球手。
- 最终验收增加手、脚、关节近景以及三分之四视角检查。
- README 改为中文版，并更新仓库地址。

## 每次生成的内容

- 已验收的 `reference/concept.png` 及对应提示词。
- 通过结构检查的 BrickMorph `model.json`。
- 适合完整三维结构的 `primitives-v1`，或适合平面像素细节的 `explicit-bricks-v1`。
- 支持组装、解体、环形/球形/龙卷风散件、旋转、平移、缩放、进度拖动、自动旋转和明暗主题的本地网页。
- 自带本地 Three.js 文件、不依赖 CDN 的便携 ZIP。

技能直接使用 Codex 当前模型和内置图片生成能力，不需要调用第二个付费大模型 API。

## 安装

在 Codex 中使用 `$skill-installer`：

```text
请使用 $skill-installer 从下面的仓库安装 laoa-lego：
https://github.com/zhulin025/LaoA-Lego-skill
```

也可以手动克隆并建立链接：

```bash
git clone https://github.com/zhulin025/LaoA-Lego-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/LaoA-Lego-skill/laoa-lego" \
  "${CODEX_HOME:-$HOME/.codex}/skills/laoa-lego"
```

如果需要在 Codex Cloud 或单个仓库中使用，把 `laoa-lego/` 放到或链接到 `.agents/skills/laoa-lego/`。安装后重新载入 Codex。

## 使用示例

```text
使用 $laoa-lego 生成经典黑发孙悟空积木模型。先生成建模概念图，
再用结构化造型体完成头发、服装、关节、分段拳头和鞋。
```

```text
使用 $laoa-lego 按这张参考图生成模型。保留轮廓、姿态、比例、
配色和标志结构，并确保手掌、拇指与指块分别建模。
```

```text
使用 $laoa-lego 把这张像素画做成正面马赛克积木模型，
使用 explicit-bricks-v1 精确保留像素颜色边界。
```

```text
使用 $laoa-lego 修复这个 model.json，并重新生成可交互网页和 ZIP。
```

## 两种模型格式

### `primitives-v1`（默认）

适合完整三维人物、机器人、载具、生物、建筑和物体。模型由 48–80 个带名称的盒体、锥台、圆柱、胶囊、圆环等结构组成，再转换成约 16,000 块积木。它更容易得到清楚的体块、关节、手指、装甲层级和真实三维轮廓。

### `explicit-bricks-v1`（受限模式）

只在单颗积木坐标和正面颜色排列比三维结构更重要时使用，例如像素画、马赛克、文字、标志和浅浮雕。不要因为人物有面部伤疤或服装细线，就把整个三维人物改成微积木表面模型；这些局部细节应优先用薄造型体表达。

## 校验与预览

```bash
python3 laoa-lego/scripts/brick_model.py check model.json --write-self-check
python3 laoa-lego/scripts/build_viewer.py model.json --output viewer --zip
python3 laoa-lego/scripts/serve_viewer.py viewer --port 0
```

运行环境只需要 Python 标准库。

## 开源协议

MIT
