# [Raw 03] W3C SVG Filter Effects 規範：`feTurbulence` 微觀磨砂雜訊與 `feDisplacementMap` 邊緣折射置換

- **文獻類型**：W3C SVG Filters 1.0 / Filter Effects Module 技術文獻整理
- **核心標準參考**：SVG Filter Primitives（`<feTurbulence>`、`<feDisplacementMap>`）
- **對應 Wiki 單元**：Unit 01（微觀雜訊）與 Unit 04（`notes/svg-refraction-displacement.md`）

---

## 一、微觀質感層：為什麼需要 `2%～4%` 的 SVG 雜訊？

### 1. 消除 8-bit 色階斷裂（Gradient Banding）
現代網頁顯色普遍仍處於每色版 8-bit（`0～255` 階）sRGB 色彩空間。當毛玻璃上方覆蓋大面積 `rgba(255,255,255,0.25)` 至 `rgba(255,255,255,0.05)` 的平滑線性漸層，或後方執行大範圍 `blur(20px)` 時，相鄰像素的亮度差小於 1 個階度就會出現肉眼可見的「等高線條紋（Banding）」。

### 2. Perlin / Simplex 分形雜訊抖動（Dithering）
利用內嵌 SVG Data URI `<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch" />` 生成高頻細粒雜訊紋理，透過極低不透明度覆蓋於 `.glass-panel::after`：
- **標準濃度區間**：`opacity: 0.02 ～ 0.04`（本知識庫標準值為 `0.032`，即 **3.2%**）。
- **過高風險**：超過 `0.08`（8%）會使畫面出現老舊電視雪花點，文字閱讀產生顆粒疲勞；設為 `0` 則失去磨砂實體觸感並顯露色階斷層。

---

## 二、表面曲率折射：`feDisplacementMap` 光學原理

單純的 CSS `backdrop-filter: blur()` 只能對後方像素做「同位置鄰域模糊」，**無法改變像素座標位置**——也就是缺乏真實凹凸透鏡、水滴或玻璃邊緣厚邊將背景光線「推開／扭曲（Refraction）」的效果。

SVG 的 `<feDisplacementMap>` 提供了基於灰階／色版貼圖的二維像素座標偏移公式：

$$P'(x, y) \leftarrow P\left(x + \text{scale} \cdot (XC(x, y) - 0.5),\; y + \text{scale} \cdot (YC(x, y) - 0.5)\right)$$

關鍵屬性解釋：
- **`in="SourceGraphic"`**：被扭曲的原圖來源。
- **`in2="displacementMap"`**：提供偏移方向與幅度的貼圖（可由 `<feTurbulence>` 或雙色徑向/線性漸層產生）。
- **`xChannelSelector="R"` / `yChannelSelector="G"`**：分別讀取紅通道（`R`）與綠通道（`G`）作為 X 軸與 Y 軸的折射向量。通道值 `0.5`（十進位 `128`）代表零位移，`< 0.5` 向負方向偏移，`> 0.5` 向正方向偏移。
- **`scale`（置換強度）**：控制折射彎曲幅度。實務 UI 微折射建議落在 `scale="8"` ～ `scale="28"`；邊緣透鏡實驗可展示到 `40 ～ 60`。

---

## 三、邊緣色散光環（Chromatic Dispersion / Abberation）

真實玻璃三稜鏡對紅（R）、綠（G）、藍（B）不同波長的光線具有略微不同的折射率（Cauchy 色散效應），因此在毛玻璃高曲率邊緣常能見到極細微的「藍青—紫紅邊緣色散」：
- 在 UI 工程上，可結合兩種手法重現：
  1. **SVG 濾鏡通道微偏移**：透過 `<feColorMatrix>` 分離 RGB 三通道並套用相差 `1 ～ 3` 單位的 `scale` 或 `feOffset` 微偏移，再用 `blend mode="screen"` 合成。
  2. **CSS 多層內外色散邊框陰影（零多通道負擔）**：在主玻璃容器邊緣疊加 `inset 1px 0 0 rgba(56, 189, 248, 0.45)`（青藍光緣）與 `inset -1px 0 0 rgba(244, 63, 94, 0.28)`（暖紅光緣），在不破壞文字清晰度的前提下做出極具液態玻璃感的色散邊緣。
- **效能注意**：Firefox、Safari 與 Chrome 對 CSS `backdrop-filter: url(#svg-filter)` 的跨元素支持度仍在演進，將 `feDisplacementMap` 應用於專屬背景光學舞台或內聯 SVG 元素（`<svg>` 內部 `<g filter="url(#...)">`）是目前跨瀏覽器最穩定 100% 可用的做法。
