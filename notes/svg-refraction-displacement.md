# [Unit 04] SVG 置換濾鏡與邊緣色散折射

---

## Meta 資訊（Frontmatter 規格）

- **單元編號**：Unit 04
- **單元標題**：SVG 置換濾鏡與邊緣色散折射
- **副標題**：突破 `blur()` 的平面極限——運用 `<feDisplacementMap>` 像素偏移與微幅 RGB 邊緣色散，刻畫真實液態玻璃的彎曲折光感
- **Slug**：`svg-refraction-displacement`
- **分類**：`表面折射`
- **預計閱讀時間**：`12 分鐘`
- **關鍵字標籤**：`feDisplacementMap`, `Chromatic Dispersion`, `SVG Filter`
- **成品路徑**：`lessons/svg-refraction-displacement/index.html`
- **Ingest 原始文獻來源**：[`raw/03-svg-turbulence-and-displacement-refraction.md`](../raw/03-svg-turbulence-and-displacement-refraction.md)
- **前後單元導覽**：
  - 上一單元：`../gpu-compositing-and-agents/index.html`（Unit 03 GPU 合成圖層效能瓶頸與 AGENTS.md 規範）
  - 下一單元：`../dynamic-light-tracking/index.html`（Unit 05 動態光源追蹤與滑鼠高光跟隨）
- **狀態**：`✅ 已定稿`

---

## 一、一句話核心觀念（TL;DR）

> CSS `backdrop-filter: blur()` 只能對原地像素做柔和擴散，無法真正改變光線前進方向；透過 SVG **`<feDisplacementMap>`** 讀取位移貼圖的 R/G 色版強度並將背景像素推離原本座標（$P'(x,y)$），再於玻璃邊緣疊加微幅「青藍／暖紅」雙側 **邊緣色散光環**，就能在網頁重現凸透鏡與水滴般的液態折射效果。

---

## 二、核心觀念拆解

### 卡片 1：為什麼 `blur()` 不算真正的「光學折射」？
- **痛點描述**：純粹模糊的面板背後如果是斜線網格或字母，這些圖案只會變得朦朧，線條不會在玻璃邊緣彎曲轉折，看起來仍像一層霧膜而非有曲率的實體透鏡。
- **核心解法與 SVG 屬性**：改用 SVG `<feDisplacementMap>` 根據 R/G 通道的灰階亮度差進行二維像素置換：
  $$P'(x, y) \leftarrow P\left(x + \text{scale} \cdot (XC(x, y) - 0.5),\; y + \text{scale} \cdot (YC(x, y) - 0.5)\right)$$
- **參數對照**：當置換貼圖像素值等於中性灰（`0.5`，即 RGB `128`）時位移量為 `0`；高於或低於 `0.5` 時，會依 `scale` 強度將後方圖案向左右與上下推移。

### 卡片 2：標準 `<feTurbulence>` ＋ `<feDisplacementMap>` 濾鏡結構
- **SVG 濾鏡串接寫法**：
  ```xml
  <filter id="liquidGlassRefract" x="-15%" y="-15%" width="130%" height="130%">
    <feTurbulence type="fractalNoise" baseFrequency="0.024" numOctaves="2" result="noiseMap" />
    <feDisplacementMap in="SourceGraphic" in2="noiseMap"
      scale="24" xChannelSelector="R" yChannelSelector="G" />
  </filter>
  ```
- **為什麼這樣設值**：與用於消弭色帶的 `baseFrequency="0.85"` 微觀雜訊不同，做「表面波紋與玻璃曲率折射」時頻率必須壓低至 **`0.015 ～ 0.045`** 才能形成大片水波曲面；UI 微折射 `scale` 建議落在 **`8 ～ 28`**（高曲率展示可至 `40 ～ 60`）。

### 卡片 3：邊緣色散光環（Chromatic Dispersion）與跨瀏覽器實戰策略
- **牛頓三稜鏡效應的 UI 轉譯**：不同波長的可見光折射率不同，因此在厚玻璃切面邊緣常出現極微弱的「青藍（`rgba(56, 189, 248, 0.48)`）與暖紅（`rgba(244, 63, 94, 0.30)`）」光緣偏移。
- **工程實戰解法**：直接在玻璃內邊框使用雙色微幅 `inset` 陰影（`1px ～ 3px`）重現色散光緣，搭配內聯 SVG 舞台呈現 `<feDisplacementMap>` 即時扭曲——既能在 Chrome / Firefox / Safari 保持 100% 一致顯示，又不會像全螢幕套用 SVG `backdrop-filter: url()` 般拖垮幀率。

### ⚠️ 常見誤區與效能地雷（Pitfall Alert）
- **誤區名稱**：將全域 `backdrop-filter: url(#displacement)` 套用在滾動長頁面或所有小卡片，且把 `scale` 開到 `100` 以上。
- **為什麼容易出錯**：跨元素 SVG 濾鏡作為 `backdrop-filter` 在部分行動瀏覽器與 Safari 尚未統一支援，且超大 `scale` 會導致文字筆畫斷裂完全不可讀。
- **正確做法**：主體文字容器維持 `AGENTS.md` 標準 `blur(20px) saturate(190%)`＋外緣雙色色散 `inset` 光框；真正的 `<feDisplacementMap>` 應限定於裝飾性透鏡圖層或專屬 SVG 實驗舞台（`scale` 控制在 `8 ～ 28` 之間）。

---

## 三、互動實驗室規格（Interactive Lab Spec）

- **實驗室名稱**：SVG 置換濾鏡與邊緣色散折射實驗台
- **教學目的**：讓開發者即時調整 `feDisplacementMap` 的 `scale`、`feTurbulence` 的 `baseFrequency` 與邊緣色散偏移量，親眼看見後方網格與色彩如何被玻璃曲率彎曲推開。
- **控制元件（Inputs）**：
  - 置換強度 `scale` 滑桿：`0 ～ 60`（預設 `24`）
  - 曲面波紋頻率 `baseFrequency` 滑桿：`0.010 ～ 0.075`（預設 `0.025`）
  - 邊緣色散強度（Chromatic Edge）滑桿：`0px ～ 6px`（預設 `2.5px`）
  - 快速模式切換：`推薦 UI 微折射 (scale: 20)` / `強水波曲率 (scale: 48)` / `歸零對照 (scale: 0)`
- **視覺化輸出（Outputs）**：
  - 內嵌真實 `<svg>` `<feDisplacementMap>` 光學折射預覽舞台 ＋ 即時產生的 SVG / CSS 複製碼。

---

## 四、隨堂自我檢測（3 題單選題）

### Q1：為何想在網頁中呈現「玻璃將後方線條彎曲推開」的效果，不能只靠 CSS `blur()`，而需要 SVG `<feDisplacementMap>`？
- A. 因為 `blur()` 只能做原地像素加權平均模糊，無法根據置換貼圖改變後方像素的 X/Y 幾何座標
- B. 因為 `blur()` 無法支援 PNG 圖片背景
- C. 因為 `<feDisplacementMap>` 會自動關閉 GPU 加速
- D. 因為 CSS 不支援百分比單位
- **正解**：`A`
- **詳解**：高斯模糊是對鄰域像素進行亮度色彩平均，線條中心仍在原處；`<feDisplacementMap>` 則依 R/G 通道亮度偏移座標 $P'(x,y)$，真正模擬光線折射偏折。

### Q2：若分別要製作「消弭色帶微粒」與「大片水波曲面折射」，`baseFrequency` 應該如何區分？
- A. 兩者都必須設定成 `0`
- B. 消弭色帶用高頻 `0.85` 配合 `2%～4%` 低透明度；大片曲面折射用低頻 `0.015～0.045`
- C. 曲面折射要用 `5.0`，微觀雜訊要用 `0.001`
- D. `baseFrequency` 不會影響濾鏡波形大小
- **正解**：`B`
- **詳解**：`baseFrequency` 越高顆粒越細碎，適合 `0.85` 模擬磨砂霧面顆粒；頻率越低波長越寬，才會長出滑順的玻璃曲率與水波紋。

### Q3：實作真實玻璃的「邊緣色散光環（Chromatic Dispersion）」時，在顧及文字可讀性與效能下，最推薦的實作策略為何？
- A. 對整頁所有文字都套用大幅度 SVG RGB 位移濾鏡直到文字變成彩色疊影
- B. 在玻璃邊緣疊加微幅（1px～3px）的青藍與暖紅雙色 `inset` 內陰影光緣，主文字區保持清晰銳利
- C. 把所有 HTML 按鈕截圖後進 Photoshop 塗上漸層
- D. 關閉 `-webkit-backdrop-filter`
- **正解**：`B`
- **詳解**：邊緣色散發生於高曲率切角外緣；利用輕量級雙色 `inset` 陰影即可零額外 GPU 濾鏡成本重現稜鏡邊光，同時確保內部文字 100% 清晰可讀。
