# [Raw 04] Apple Liquid Glass 與 Specular Pointer Tracking：動態光源追蹤與游標交互反光

- **文獻類型**：現代作業系統液態玻璃設計與前端互動光學技術整理
- **核心標準參考**：Apple WWDC Liquid Glass Materials（動態高光追蹤概念）與 CSS Custom Properties 實作指南
- **對應 Wiki 單元**：Unit 05（`notes/dynamic-light-tracking.md`）

---

## 一、從「靜態光影」走向「環境光互動（Dynamic Specular）」

Vista Aero 假設環境光源固定來自正上方或左上方 45 度角；而 Apple 在 Liquid Glass 材質系統中強調 **「玻璃會對使用者的操作與角度變化做出即時物理回應」**——在桌面網頁介面中，最直覺的物理媒介便是**滑鼠游標／觸控指針座標**。

---

## 二、實現 Specular Pointer Tracking 的三段式技術架構

### 1. JavaScript 事件取樣（低開銷局部座標換算）
監聽容器或視窗的 `pointermove` 事件，利用 `el.getBoundingClientRect()` 將全螢幕座標 `(clientX, clientY)` 換算為卡片內部的相對座標 `(x, y)`，寫入 CSS 自訂屬性 `--mx` 與 `--my`：

```js
card.addEventListener('pointermove', (e) => {
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  card.style.setProperty('--mx', `${x.toFixed(1)}px`);
  card.style.setProperty('--my', `${y.toFixed(1)}px`);
});
```

### 2. CSS 徑向高光層（Surface Specular Spotlight）
在 `.glass-panel` 內部加入獨立的追光漸層（或不阻擋事件的浮層）：
```css
background-image: radial-gradient(
  260px circle at var(--mx, 50%) var(--my, 20%),
  rgba(255, 255, 255, 0.42) 0%,
  rgba(56, 189, 248, 0.14) 38%,
  transparent 72%
);
```
當游標滑過卡片表面時，一片橢圓／圓形柔和高光會緊貼指針移動，與原本 `::before` 的 50% 靜態切面形成雙重反光層次。

### 3. 倒角邊框動態感應（Border-Mask Bevel Glow）
透過 CSS `mask` 或偽元素邊框遮罩（`-webkit-mask-composite: xor; mask-composite: exclude;`），只保留玻璃面板外圍 `1.5px` 邊框顯示徑向白光，讓真實物理玻璃邊緣「只在燈光靠近的那一側被點亮」，而不只是面板中間多一團亮斑。

---

## 三、效能守則：為什麼 `--mx` / `--my` 不能觸發 Layout Reflow 或 Nested Blur？

1. **禁止在 `pointermove` 讀取後立刻連續寫入幾何屬性（`width` / `top` / `left`）**：改寫 `top`/`left` 會引發瀏覽器主執行緒強制重新排版（Forced Synchronous Layout Thrashing）。
2. **安全做法**：
   - 更新 `--mx`、`--my` 驅動透明高光背景圖層（僅觸發 Paint/Composite）。
   - 若搭配 3D 微傾角物理視覺回饋，應使用 `transform: perspective(900px) rotateX(...) rotateY(...)`（純 GPU 合成器變換，零 Reflow）。
   - 保持 `pointer-events: none` 於所有追光高光層上，以免游標座標跳動閃爍。
   - 若頁面上有多張卡片同時追光，應結合 `requestAnimationFrame` 節流（每幀最多更新一次座標），將單幀 CPU 腳本耗時壓在 `0.5ms` 以下。
