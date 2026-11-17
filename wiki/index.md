# LLM Wiki 知識總覽與來源對照索引（Aero Glass & Optical UI Wiki）

> 本頁面為 **Aero Glass 與介面光學設計知識庫（`genai-wiki-hub`）** 的中央知識地圖，依據 Karpathy LLM Wiki 三層結構設計：**`raw/`（6 篇原始權威文獻 + 1 份先討論後生成需求訪談） → `notes/`（6 篇結構化 Markdown 原稿） → `lessons/`（6 頁互動式光學講義網頁）**，並作為第 10 週作業教學簡報 [`slides/index.html`](../slides/index.html) 的單一事實來源（Single Source of Truth）。

---

## 一、原始文獻 Ingest 狀態總表（`raw/` → `notes/` → `lessons/`）

| 單元編號 | 單元主題與分類 | 原始文獻（`raw/`） | Markdown 知識原稿（`notes/`） | 互動光學講義網頁（`lessons/`） | 簡報引用頁碼（`slides/`） |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit 01** | **背景模糊、鮮豔度補償與玻璃微觀雜訊**（`光學基底`） | [`raw/01-w3c-css-backdrop-filter-spec.md`](../raw/01-w3c-css-backdrop-filter-spec.md)<br>[`raw/03-svg-turbulence-and-displacement-refraction.md`](../raw/03-svg-turbulence-and-displacement-refraction.md) | [`notes/blur-and-saturation.md`](../notes/blur-and-saturation.md) | [`lessons/blur-and-saturation/index.html`](../lessons/blur-and-saturation/index.html) | Slide 02、03、04、12 |
| **Unit 02** | **物理厚度、倒角光線與 Vista 鏡面切面**（`表面折射`） | [`raw/02-vista-dwm-aero-optical-spec.md`](../raw/02-vista-dwm-aero-optical-spec.md) | [`notes/bevel-and-refraction.md`](../notes/bevel-and-refraction.md) | [`lessons/bevel-and-refraction/index.html`](../lessons/bevel-and-refraction/index.html) | Slide 02、05、06、12 |
| **Unit 03** | **GPU 合成圖層效能瓶頸與 AGENTS.md 規範**（`效能與規範`） | [`raw/05-chromium-gpu-compositing-and-fps-budget.md`](../raw/05-chromium-gpu-compositing-and-fps-budget.md) | [`notes/gpu-compositing-and-agents.md`](../notes/gpu-compositing-and-agents.md) | [`lessons/gpu-compositing-and-agents/index.html`](../lessons/gpu-compositing-and-agents/index.html) | Slide 02、09、11、12 |
| **Unit 04** | **SVG 置換濾鏡與邊緣色散折射**（`表面折射`） | [`raw/03-svg-turbulence-and-displacement-refraction.md`](../raw/03-svg-turbulence-and-displacement-refraction.md) | [`notes/svg-refraction-displacement.md`](../notes/svg-refraction-displacement.md) | [`lessons/svg-refraction-displacement/index.html`](../lessons/svg-refraction-displacement/index.html) | Slide 07、12 |
| **Unit 05** | **動態光源追蹤與滑鼠高光跟隨**（`光學基底`） | [`raw/04-apple-liquid-glass-and-dynamic-specular.md`](../raw/04-apple-liquid-glass-and-dynamic-specular.md) | [`notes/dynamic-light-tracking.md`](../notes/dynamic-light-tracking.md) | [`lessons/dynamic-light-tracking/index.html`](../lessons/dynamic-light-tracking/index.html) | Slide 08、12 |
| **Unit 06** | **WCAG 對比度驗證與無障礙降級策略**（`效能與規範`） | [`raw/06-wcag-contrast-and-reduced-transparency.md`](../raw/06-wcag-contrast-and-reduced-transparency.md) | [`notes/accessibility-fallback.md`](../notes/accessibility-fallback.md) | [`lessons/accessibility-fallback/index.html`](../lessons/accessibility-fallback/index.html) | Slide 10、12 |

---

## 二、核心光學數據單一事實基準（Canonical Metrics）

為了避免後續 AI 代理在生成教學簡報或擴充新講義時猜測數值，本知識庫鎖定以下經 `raw/` 驗證之核心數據：

1. **模糊與彩度衰減補償**（出自 `raw/01` → Unit 01）：
   - 單純 `blur(20px)` 會因互補色混色導致有效彩度衰減約 **32%～45%**。
   - 標準解方為 `backdrop-filter: blur(20px) saturate(190%)`（搭 `-webkit-backdrop-filter`），並結合 `135deg` 斜向微透光漸層（`0.25 → 0.05`）。
2. **Vista Aero 倒角、50% 切面與文字光暈**（出自 `raw/02` → Unit 02）：
   - 迎光邊框 `border-top-color: rgba(255,255,255,0.7)`、`border-left-color: rgba(255,255,255,0.5)`，搭配 `inset 0 1px 0 0 rgba(255,255,255,0.8)` 與 `inset 0 -1px 0 0 rgba(0,0,0,0.1)`。
   - `.glass-panel::before` 設定 `height: 50%` 與 `pointer-events: none;`，切出非連續鏡面反光。
   - `.vista-text` 使用雙層白光防護：`0 0 8px rgba(255,255,255,0.9), 0 0 16px rgba(255,255,255,0.5)`。
3. **微觀磨砂雜訊與 SVG 曲率折射**（出自 `raw/03` → Unit 01 / Unit 04）：
   - 微觀磨砂消弭 8-bit 色帶採用高頻 `baseFrequency="0.85"`、`opacity: 0.032`（`2%～4%`）。
   - 水波與透鏡曲率折射使用 `<feDisplacementMap>` 搭配低頻 `baseFrequency: 0.015～0.045` 與 UI 建議強度 `scale: 8～28`。
4. **動態光源追蹤**（出自 `raw/04` → Unit 05）：
   - 透過 `pointermove` 與 `requestAnimationFrame` 更新 `--mx` / `--my`（預設 `50%` / `20%`），配合 `mask-composite: exclude` 打造無 Layout Reflow（腳本耗時 `< 0.5ms`）的 1.5px 邊框追光。
5. **GPU 合成圖層與 60fps 幀預算**（出自 `raw/05` → Unit 03）：
   - 60Hz 幀預算上限為 **`16.67ms`**（超過 `24ms` 視為掉幀 Jank）。
   - 嚴禁在 `.glass-panel` 內部次級元件嵌套 `backdrop-filter`（避免造成 4 倍以上 RenderPass 爆發），改採「外實內輕」半透明實底 `rgba(255,255,255,0.58)`。
6. **WCAG 2.2 無障礙對比與雙重降級**（出自 `raw/06` → Unit 06）：
   - 一般內文對比度底線 **`4.5:1`**（AA 級），大標題 **`3.0:1`**，加強版 AAA 級 **`7.0:1`**。
   - 必須實作 `@media (prefers-reduced-transparency: reduce)`（提升底色至 `0.94`）與 `@supports not (backdrop-filter: blur(1px))`（退場至 `0.90`）。

---

## 三、相關工作流與憲法文件

- **需求訪談與先討論紀錄**：[`raw/00-interview-and-requirements.md`](../raw/00-interview-and-requirements.md)
- **專案開發憲法**：[`AGENTS.md`](../AGENTS.md) / [`CLAUDE.md`](../CLAUDE.md)
- **現況白板與變更紀錄**：[`NOTES.md`](../NOTES.md) / [`log.md`](../log.md)
- **Graph + Loop 自動生成簡報工作流**：[`.agents/workflows/topic-slides.md`](../.agents/workflows/topic-slides.md) 與 [`workflow/report.md`](../workflow/report.md)
