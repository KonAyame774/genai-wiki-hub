# [證據卡 05] Unit 05：動態光源追蹤與滑鼠高光跟隨

- **限定來源（嚴禁混入其他單元）**：
  - `notes/dynamic-light-tracking.md`
  - `raw/04-apple-liquid-glass-and-dynamic-specular.md`
- **對應網頁出處**：`../lessons/dynamic-light-tracking/index.html`

---

## 1. 新手一句話比喻
> 如果把游標想像成你手上拿的小手電筒，當你把滑鼠滑過 Apple Liquid Glass 卡片時，卡片玻璃表面與 1.5px 的邊框倒角都會跟著手電筒移動的方向泛起微光！

## 2. 經來源查證之核心數據
- **核心驅動機制**：透過 JS 監聽 `pointermove` 與 `getBoundingClientRect()` 算出卡片局部座標，寫入 CSS 自訂屬性 **`--mx`** 與 **`--my`**。
- **預設回退（Fallback）**：撰寫 `radial-gradient(260px circle at var(--mx, 50%) var(--my, 20%), ...)` 保留 `50%` / `20%` 預設值，確保手機無懸停游標時依然好看。
- **外框邊角感光遮罩**：利用 `padding: 1.5px` 配合 `-webkit-mask-composite: xor` / `mask-composite: exclude` 挖空 `content-box`，只讓邊框隨滑鼠點亮而不洗白內文。
- **零 Reflow 效能**：只更新 `--mx`/`--my` 與 GPU 合成的 `transform: perspective(900px) rotateX() rotateY()`，配合 `requestAnimationFrame` 節流將單幀腳本耗時壓低至 **`< 0.5ms`**。

## 3. 新手必避誤區
- 不可替每個動態高光覆蓋層疊加 `backdrop-filter`，也不可改寫 `top`/`left` 幾何位置導致 Layout Thrashing；覆蓋層務必設定 `pointer-events: none;`。
