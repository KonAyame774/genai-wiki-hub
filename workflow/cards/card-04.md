# [證據卡 04] Unit 04：SVG 置換濾鏡與邊緣色散折射

- **限定來源（嚴禁混入其他單元）**：
  - `notes/svg-refraction-displacement.md`
  - `raw/03-svg-turbulence-and-displacement-refraction.md`
- **對應網頁出處**：`../lessons/svg-refraction-displacement/index.html`

---

## 1. 新手一句話比喻
> CSS 模糊只是讓水底的字變得霧霧的；SVG 的 `<feDisplacementMap>` 才像是把一片放大鏡或凹凸水波玻璃放在上方，真的把水底線條「推彎、折過去」，還能在玻璃切邊折射出淡淡的彩虹邊光！

## 2. 經來源查證之核心數據
- **像素置換數學公式**：$P'(x, y) \leftarrow P(x + \text{scale} \cdot (R(x,y) - 0.5),\; y + \text{scale} \cdot (G(x,y) - 0.5))$。灰階值 `0.5`（128）代表原地不動。
- **波紋頻率對照**：與高頻微粒雜訊 `0.85` 相反，曲面水波折射必須將 `<feTurbulence>` 的 `baseFrequency` 設為低頻 **`0.015 ～ 0.045`**。
- **置換強度 `scale`**：UI 卡片微折射建議設定在 **`8 ～ 28`**（實驗示範高曲率可至 `40 ～ 60`）。
- **稜鏡邊緣色散（Chromatic Dispersion）**：以雙色 `inset` 內陰影（左側青藍 `rgba(56, 189, 248, 0.48)`、右側暖紅 `rgba(244, 63, 94, 0.30)`）在 `1px ～ 3px` 內重現色散光緣，兼顧文字清晰度與跨瀏覽器 100% 相容。

## 3. 新手必避誤區
- 不要將強置換（如 `scale > 50`）直接覆蓋在大段小字內文上，以免字體筆畫嚴重扭曲無法辨識。
