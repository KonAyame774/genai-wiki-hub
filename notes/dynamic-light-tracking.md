# [Unit 05] 動態光源追蹤與滑鼠高光跟隨

---

## Meta 資訊（Frontmatter 規格）

- **單元編號**：Unit 05
- **單元標題**：動態光源追蹤與滑鼠高光跟隨
- **副標題**：讓靜態毛玻璃「活過來」——透過 `--mx` / `--my` CSS 變數與 `pointermove`，打造 Liquid Glass 游標即時反光與邊緣感光
- **Slug**：`dynamic-light-tracking`
- **分類**：`光學基底`
- **預計閱讀時間**：`11 分鐘`
- **關鍵字標籤**：`--mx / --my`, `Specular Tracking`, `Liquid Glass`
- **成品路徑**：`lessons/dynamic-light-tracking/index.html`
- **Ingest 原始文獻來源**：[`raw/04-apple-liquid-glass-and-dynamic-specular.md`](../raw/04-apple-liquid-glass-and-dynamic-specular.md)
- **前後單元導覽**：
  - 上一單元：`../svg-refraction-displacement/index.html`（Unit 04 SVG 置換濾鏡與邊緣色散折射）
  - 下一單元：`../accessibility-fallback/index.html`（Unit 06 WCAG 對比度驗證與無障礙降級策略）
- **狀態**：`✅ 已定稿`

---

## 一、一句話核心觀念（TL;DR）

> Apple Liquid Glass 的核心靈魂在於「玻璃會對環境與使用者位置做出即時回應」：只用幾行 JavaScript 監聽 `pointermove` 並將相對座標寫入 CSS 自訂屬性 **`--mx` / `--my`**，搭配 `radial-gradient(circle at var(--mx) var(--my), ...)` 與外框遮罩，就能零 Layout Reflow 地讓面板表面與玻璃倒角隨游標發光。

---

## 二、核心觀念拆解

### 卡片 1：從靜態高光到動態互動光源（Specular Pointer Tracking）
- **痛點描述**：Vista Aero 假設上方恆有一盞靜止的燈，因此即使滑鼠在畫面上來回移動、點擊卡片，玻璃反光也紋風不動。
- **核心解法與 CSS 屬性**：以 `--mx`（Pointer X）與 `--my`（Pointer Y）作為光源中心，動態定位表面與邊框的徑向高光層：
  ```css
  .specular-spot {
    background: radial-gradient(
      260px circle at var(--mx, 50%) var(--my, 20%),
      rgba(255, 255, 255, 0.42) 0%,
      rgba(56, 189, 248, 0.14) 38%,
      transparent 72%
    );
  }
  ```
- **參數對照**：提供預設值 `50%` / `20%` 至關重要，能確保滑鼠尚未滑入前或行動裝置純點擊時，玻璃依然維持上方受光的經典高光美感。

### 卡片 2：邊框動態感光倒角（CSS Border-Mask Glow）
- **為什麼不能只有面板中間亮一塊？**：物理玻璃在光源靠近某側邊緣時，該側的 1.5px 切割倒角也會瞬間變得璀璨。
- **CSS Mask 精準透框技術**：
  ```css
  .edge-glow::after {
    padding: 1.5px;
    background: radial-gradient(180px circle at var(--mx) var(--my), rgba(255,255,255,0.95), transparent 70%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
  }
  ```
  利用雙層遮罩互斥（`exclude`），挖空中間區域、只留下邊緣 `1.5px` 顯示隨游標流動的銳利邊光，不會像內層背景那樣洗白文字！

### 卡片 3：零 Reflow 的效能工程守則
- **嚴禁修改幾何佈局屬性**：追光動畫絕對不可改變 `top`、`left`、`width` 或 `border-width`，以免觸發瀏覽器重新計算版面（Layout Thrashing）。
- **GPU 友善的互動寫法**：
  1. 僅更新 `--mx`、`--my` 驅動透明覆蓋層與邊框漸層。
  2. 所有高光覆蓋偽元素務必宣告 **`pointer-events: none;`**。
  3. 若要結合手勢傾角回饋，只允許使用 `transform: perspective(900px) rotateX(...) rotateY(...)`（純 GPU 合成變換）。

### ⚠️ 常見誤區與效能地雷（Pitfall Alert）
- **誤區名稱**：為了做「多張卡片同時追光」，替頁面上每張卡片的追光疊層又各掛一個 `backdrop-filter: blur(20px)`，且沒有節流處理。
- **為什麼容易出錯**：違反 `AGENTS.md` 單層外框模糊規範，讓滑鼠每移動 1 像素就迫使十多個嵌套模糊圖層同步重繪，立即掉幀。
- **正確做法**：追光層僅使用純 `radial-gradient` 透明疊層（零 `backdrop-filter`），並用 `requestAnimationFrame` 節流座標寫入，將單幀 CPU 腳本耗時控制在 `0.5ms` 以內。

---

## 三、互動實驗室規格（Interactive Lab Spec）

- **實驗室名稱**：Specular Pointer Tracking 動態光源追蹤實驗台
- **教學目的**：讓開發者親手在舞台上移動滑鼠（或啟用「自動軌道巡航燈」），即時調整高光半徑、反光亮度、邊框感光與 3D 微傾角，並直接複製 CSS + JS 程式碼。
- **控制元件（Inputs）**：
  - 高光半徑（Spotlight Radius）：`120px ～ 420px`（預設 `260px`）
  - 表面反光強度（Specular Alpha）：`0.10 ～ 0.72`（預設 `0.42`）
  - 獨立開關：`開啟 Border-Mask 邊角感應`、`開啟 3D 傾角透視`、`自動光源巡航（Auto Orbit）`
- **視覺化輸出（Outputs）**：
  - 可即時追蹤滑鼠的 Liquid Glass 卡片舞台 ＋ 即時座標遙測（`--mx`, `--my`, 傾角角度）＋ 完整 CSS 輸出。

---

## 四、隨堂自我檢測（3 題單選題）

### Q1：為何在撰寫 `radial-gradient(260px circle at var(--mx, 50%) var(--my, 20%), ...)` 時，強烈建議替 `--mx` 與 `--my` 加上預設值（Fallback）？
- A. 因為滑鼠尚未移入或手機觸控用戶沒有懸停（Hover）游標前，卡片仍能保有自然的高光預設位置
- B. 因為沒有預設值會導致 JavaScript 無法執行
- C. 因為這樣可以繞過瀏覽器同源政策
- D. 為了把文字全部變成粗體
- **正解**：`A`
- **詳解**：手機螢幕與頁面初載入時通常尚未觸發 `pointermove`，保留 `50%, 20%` 預設值能確保卡片隨時保持美觀的上方受光態。

### Q2：製作「只有玻璃外框 1.5px 邊緣會隨游標發光、但中間文字區不受高光遮蓋」的效果，最適合搭配哪一項 CSS 技術？
- A. `mask-composite: exclude`（搭配 `-webkit-mask-composite: xor`）挖空 `content-box`
- B. 替文字加上 `display: none`
- C. 把外框設成 `backdrop-filter: blur(80px)`
- D. 用 `position: static` 覆蓋整個網頁
- **正解**：`A`
- **詳解**：雙層漸層搭配 `exclude` / `xor` 遮罩複合模式，能精準剔除 `content-box` 內部，僅露出 `padding` 所形成的 `1.5px` 玻璃切割倒角邊框。

### Q3：實作滑鼠追光反光與微幅 3D 傾角回饋時，應如何避免造成瀏覽器卡頓（Layout Thrashing）？
- A. 改寫元素的 `top` 與 `left` 位置來模擬傾斜
- B. 只透過 `--mx` / `--my` 更新高光漸層，並使用 `transform: perspective(...) rotateX(...) rotateY(...)` 且確保高光層設有 `pointer-events: none`
- C. 每秒強制清空重建整個 DOM 樹 60 次
- D. 在每個子膠囊內層都加上 `backdrop-filter`
- **正解**：`B`
- **詳解**：`transform` 由瀏覽器合成器直接於 GPU 執行，不會觸發主執行緒的 Layout 重排，搭配純透明高光層即可維持穩定 60fps。
