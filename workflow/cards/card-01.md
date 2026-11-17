# [證據卡 01] Unit 01：背景模糊、鮮豔度補償與玻璃微觀雜訊

- **限定來源（嚴禁混入其他單元）**：
  - `notes/blur-and-saturation.md`
  - `raw/01-w3c-css-backdrop-filter-spec.md`
  - `raw/03-svg-turbulence-and-displacement-refraction.md`（§1 微觀雜訊）
- **對應網頁出處**：`../lessons/blur-and-saturation/index.html`

---

## 1. 新手一句話比喻
> 單純模糊玻璃就像隔著起霧又積灰塵的窗戶看風景——必須開大 `saturate(190%)` 把洗灰的色彩救回來，再鋪上 3% 的超細砂紙微粒消弭螢幕漸層條紋，才會變成像 Apple 水晶玻璃那樣清亮透澈。

## 2. 經來源查證之核心數據
- 單純套用高斯模糊 `blur(20px)` 會把互補色與相鄰像素加權混色，導致背後透出色彩的有效彩度（Saturation）**大幅衰減約 32%～45%**，使面板發灰混濁。
- 黃金配方：`backdrop-filter: blur(20px) saturate(190%);`（須同步宣告 `-webkit-backdrop-filter` 相容 Safari）。
- 表面微透光基底：使用 `135deg` 斜向漸層，從左上 `rgba(255, 255, 255, 0.25)` 漸弱至右下 `rgba(255, 255, 255, 0.05)`。
- SVG 微觀雜訊：使用 `<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch" />` 內嵌 Data URI，不透明度鎖定 **`2%～4%`**（本專案標準 **`0.032`**），消弭 8-bit 顯示器常見的漸層色階斷裂（Banding）。

## 3. 新手必避誤區
- 若底層是純白或純黑背景，套用再強的 `blur(20px) saturate(190%)` 也看不出折射質感——必須搭配高對比色彩或極光漸層背景。
- SVG 雜訊若開太高（例如 `> 8%`），會讓介面出現老舊電視雪花點。
