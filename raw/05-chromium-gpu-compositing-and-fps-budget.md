# [Raw 05] Chromium GPU 合成圖層管線與 `backdrop-filter` 60fps 效能預算報告

- **文獻類型**：瀏覽器渲染引擎（Blink / Skia / Viz Compositor）效能分析整理
- **核心標準參考**：Chromium Compositing & RenderPass Optimization Principles、AGENTS.md 效能預算守則
- **對應 Wiki 單元**：Unit 03（`notes/gpu-compositing-and-agents.md`）

---

## 一、`backdrop-filter` 在 GPU 管線中的真實成本

一般純色背景（`background-color`）或平面陰影在合成階段僅需單次混合（Alpha Blending）；然而當元素啟用 `backdrop-filter: blur(20px) saturate(190%)` 時，Chromium 的繪圖排程必須執行代價高昂的多步驟 **RenderPass Cycle**：

1. **建立獨立合成圖層（RenderSurface）**：迫使合成器開闢額外 VRAM 離屏紋理緩衝區。
2. **背景擷取（Backdrop Readback）**：先繪製該元素後方所有圖層，再將交疊區域紋理拷貝至濾鏡輸入緩衝區。
3. **兩階段可分離高斯卷積（Separable 2D Blur Pass）**：對 `blur(20px)` 而言，需要進行水平與垂直雙向多輪採樣；半徑擴大為 `blur(60px)` 時需進行顯著擴張與降採樣縮放（Downsample / Upsample Chain）。
4. **彩度矩陣變換與最終合成**：依 `saturate(190%)` 乘上 4×5 色彩矩陣，最後疊回主畫面。

---

## 二、兩大致命效能地雷與量化風險

### 1. 幀預算只有 16.67ms（60fps）
在主流 60Hz 顯示器上，每一幀從 JavaScript 計算、樣式排版到 GPU 完成合成的總時間上限為 **$1000\text{ ms} / 60 \approx 16.67\text{ ms}$**（若逾時達 `> 24ms` 則被視為明顯掉幀 Jank）。一旦背景有移動光球或使用者觸控捲動，所有可視區內的 `backdrop-filter` 面板都必須每幀從頭重算一次。

### 2. 嵌套模糊（Nested Backdrop Filter）的 4 倍雪崩效應
若開發者在已經套用 `.glass-panel`（帶有 `backdrop-filter`）的大卡片內部，又替內部的 3 個狀態標籤或統計卡都加上 `backdrop-filter`：
- 單卡片的 RenderPass 數量立即從 `1` 個暴增至 `1 + 3 = 4` 倍；若頁面上有 20 張卡片，畫面將同時掛載高達 **80 個獨立模糊節點**。
- 在行動裝置或內建顯示卡上，GPU 紋理填充率（Texture Fill Rate）瞬間飽和，導致幀率跌破 25fps 甚至瀏覽器主動停用部分濾鏡。

---

## 三、工程解法：「外實內輕」架構與 `AGENTS.md` 憲法化

1. **外實內輕原則（Outer Glass, Inner Translucent Solid）**：
   - **外層**：全頁僅於 Sticky 導覽列與最外層 `.glass-panel` 啟用真實 `backdrop-filter: blur(20px) saturate(190%)`。
   - **內層**：子卡片、標籤、按鈕一律改用**高通透半透明實底**（如 `rgba(255, 255, 255, 0.58)` ～ `rgba(255, 255, 255, 0.68)`）搭配亮白 1px 邊框。外觀維持通透層次，GPU 額外模糊運算量降為 **0**。
2. **將效能預算寫進 `AGENTS.md`**：
   - 靠口頭提醒 AI「寫順一點」無效；必須在專案規範檔明確禁止嵌套 `backdrop-filter`，並用壓測腳本與真實 DOM 節點數量審查來把關。
