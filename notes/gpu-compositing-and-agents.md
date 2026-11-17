# [Unit 03] GPU 合成圖層效能瓶頸與 AGENTS.md 規範

---

## Meta 資訊

- **單元編號**：Unit 03
- **單元標題**：GPU 合成圖層效能瓶頸與 AGENTS.md 規範
- **副標題**：漂亮不能以卡頓為代價——剖析 `backdrop-filter` 的 GPU 重繪成本，並把光學預算與設計規則寫進 `AGENTS.md`
- **Slug**：`gpu-compositing-and-agents`
- **分類**：`效能與規範`
- **預計閱讀時間**：`12 分鐘`
- **關鍵字標籤**：`GPU Compositing`, `FPS Budget`, `AGENTS.md`
- **成品路徑**：`lessons/gpu-compositing-and-agents/index.html`
- **Ingest 原始文獻來源**：[`raw/05-chromium-gpu-compositing-and-fps-budget.md`](../raw/05-chromium-gpu-compositing-and-fps-budget.md)
- **前後單元導覽**：
  - 上一單元：`../bevel-and-refraction/index.html`（Unit 02 物理厚度、倒角光線與 Vista 鏡面切面）
  - 下一單元：`../svg-refraction-displacement/index.html`（Unit 04 SVG 置換濾鏡與邊緣色散折射）
- **狀態**：`✅ 已定稿`

---

## 一、一句話核心觀念（TL;DR）

> **`backdrop-filter` 是瀏覽器效能代價最高的 CSS 屬性之一**——它會強迫瀏覽器開闢獨立的 GPU 合成圖層，並在底層內容捲動或改變時不斷重繪（Repaint）。想讓 AI 長期幫你擴充毛玻璃網站而不失控掉幀，就必須把 **圖層數量上限、嵌套禁忌與標準 `.glass-panel` 寫法** 寫進 `AGENTS.md`。

---

## 二、核心觀念拆解

### 卡片 1：為什麼 `backdrop-filter` 會拖慢行動裝置幀率？
- **GPU 合成圖層的即時擷取循環**：每一層帶有 `backdrop-filter: blur(20px)` 的元素，瀏覽器都必須先繪製後方畫面 → 複製進 GPU 紋理緩衝區 → 執行多輪二維高斯卷積與彩度運算 → 再合成前景。
- **效能雪崩的兩大元兇**：
  1. **多層疊加嵌套（Nested Blur）**：在已經套用 `backdrop-filter` 的大型卡片內部，又替每個小按鈕、小標籤加上 `backdrop-filter`，造成渲染管線指數級重複計算。
  2. **大面積視差滾動重繪**：頁面捲動時底層圖層每幀都在移動，迫使所有大面積磨砂容器在 16.6ms（60fps）內全部重新模糊計算一次。

### 卡片 2：如何設計兼顧美感與 60fps 的「替代降級架構」？
- **外實內輕（Outer Glass, Inner Translucent Solid）**：
  - 只在最外層主卡片／Sticky 導覽列使用 `backdrop-filter: blur(20px) saturate(190%)`。
  - 卡片內部的子區塊（例如膠囊標籤、程式區塊、輸入框）改用 **半透明實底 `rgba(255, 255, 255, 0.58)` ＋ 細白邊框**，既保留通透層次，又只需零額外模糊成本！
- **控制模糊半徑與面積**：在手機版或低階裝置可適度將非必要裝飾圖層關閉模糊。

### 卡片 3：為什麼光學設計系統特別需要 `AGENTS.md`？
- **Vibe Coding 的毛玻璃災難**：如果你沒在專案規範鎖定 `.glass-panel` 配方，今天請 AI 生首頁它用 `blur(20px) saturate(190%)`、明天請它加第 4 頁它卻改用 `blur(4px)` 或把 `backdrop-filter` 嵌套三層，最後整個網站既不統一又在手機上滑不動。
- **用 `AGENTS.md` 把隱性經驗變成顯性合約**：
  - 鎖定標準 `.glass-panel` 程式碼與 `::before` 50% 切面寫法。
  - 明確寫下「禁止嵌套多層 `backdrop-filter`」的效能預算鐵則。
  - 搭配 `notes/_template.md` 與 `NOTES.md`，讓 AI 每次擴充新頁面都維持同樣的視覺與效能水準。

### ⚠️ 常見誤區與地雷提醒（Pitfall Alert）
- **誤區：「我的高階桌機跑 120Hz 超順，所以全頁塞滿 20 個重疊動畫毛玻璃沒關係！」**
- **真相**：中低階手機與筆電內建顯示卡的紋理填充率（Fill Rate）有限。只要同時在螢幕可視區內渲染超過 5～6 層重疊模糊且背景持續播放動畫，幀率會瞬間跌破 25fps，甚至導致瀏覽器主動放棄模糊效果或閃爍。

---

## 三、互動實驗室規格（Interactive Lab Spec）

- **實驗室名稱**：GPU 合成圖層真實渲染與 `AGENTS.md` 效能壓測實驗室
- **教學目的**：不再使用估算數字，而是直接在瀏覽器 DOM 中動態掛載真實的 `backdrop-filter` 容器與嵌套子層，並以 `requestAnimationFrame` 連續位移底層光球強迫 GPU 每幀重繪，透過 `performance.now()` 即時量測目前裝置的真實 FPS、單幀耗時（ms）與掉幀（Jank）波形。
- **控制元件（Inputs）**：
  - 真實渲染主層數滑桿：`1 ～ 20 層`（於 `#gpuRenderStage` 中真實生成互相交疊的 `.real-glass-layer` DOM）
  - 模糊半徑切換：`10px` / `20px` / `40px` / `60px`
  - 卡片內層子元件嵌套 `backdrop-filter` 開關（違反 `AGENTS.md` 規範：每張卡片內部 3 個子膠囊同步掛上即時模糊，總模糊節點倍增為 4 倍）
  - 底層高對比光球連續移動開關（`requestAnimationFrame` 每幀更新 `translate3d()` 迫使瀏覽器即時重算背景模糊）
  - 快速壓測預設：`🚨 失控 Vibe Coding（20 主層＋嵌套＝80 個真實模糊層＋60px）` vs. `🏆 遵守 AGENTS.md 預算（3 主層＋0 嵌套＋20px）`
- **視覺化輸出（Outputs）**：
  - 真實 GPU 渲染測試舞台（可視化重疊毛玻璃卡片與移動光球）。
  - 即時真實遙測儀表：Live Measured FPS、單幀耗時（`ms`）、Jank 掉幀次數（`> 24ms`）、DOM 實際掛載 `[data-has-backdrop="true"]` 節點數，以及 Canvas 繪製的最近 60 幀耗時波形圖（含 `16.7ms` 60FPS 預算基準線）。
  - `AGENTS.md` 合規檢查清單與優化建議。

---

## 四、隨堂自我檢測（3 題單選題）

### Q1：為何在行動裝置畫面上堆疊過多層 `backdrop-filter` 或搭配視差捲動時，畫面幀率（FPS）容易明顯下滑？
- A. 因為每個 `backdrop-filter` 容器都會強迫瀏覽器開闢獨立 GPU 合成圖層，並在背景變動時即時重算模糊卷積
- B. 因為 CSS 的 `border-radius` 只能支援最多三個圖層
- C. 因為 SVG 雜訊檔會暫停瀏覽器的 JavaScript 執行緒
- D. 因為 HTML 不能在同一個頁面放置超過兩張卡片
- **正解**：`A`
- **詳解**：背景模糊屬於相依於下方像素的即時後處理濾鏡；背景每移動一幀，所有覆蓋在其上的模糊層都要重新採樣與計算，對紋理填充率負擔極高。

### Q2：若想在已套用 `backdrop-filter` 的 `.glass-panel` 卡片內部再放一個提示框或標籤，最符合效能預算的做法為何？
- A. 在提示框上再套一次 `backdrop-filter: blur(30px)` 以增加模糊深度
- B. 改用半透明實底（如 `rgba(255, 255, 255, 0.58)`）搭配細白邊框，避免在同一區域嵌套多層即時模糊
- C. 用 `setInterval` 每 10 毫秒切換一次卡片的透明度
- D. 把文字全部轉成 4K PNG 圖片貼上去
- **正解**：`B`
- **詳解**：外層大卡片負責玻璃模糊折射，內部元件採用高通透純色半透明背景即可維持和諧的層次感，且不會重複觸發 GPU 模糊計算。

### Q3：將 `.glass-panel` 標準程式碼與 GPU 圖層限制寫入 `AGENTS.md`，對長期專案擴充的最大價值為何？
- A. 讓新開啟的 AI 對話不用從頭猜測光學參數，能長期複製一致的光學風格並主動避開效能地雷
- B. 讓 GitHub Pages 免除 HTTPS 憑證設定
- C. 自動把所有 CSS 檔案壓縮成零位元組
- D. 讓不支援 CSS 的文字終端機也能渲染毛玻璃
- **正解**：`A`
- **詳解**：這正是 Agentic Work 的精髓：把設計品味（5 大光學技巧）與工程紀律（GPU 預算）固化在 `AGENTS.md` 中，讓任何 AI 協作者都能產出高品質且風格一致的新單元。
