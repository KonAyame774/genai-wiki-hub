# log.md — 專案決策與變更歷史紀錄

> 本文件採「只增不刪（Append-Only）」原則，專門記錄會影響未來架構、設計規範或單元上線的重大決策。

---

## [2026-11-17] v3.0 — 完成第 10 週「6 篇 Ingest LLM Wiki ＋ Graph/Loop 教學 HTML 簡報」全面升級

- **變更決策**：
  - 依第 10 週課程「先討論、後生成」規範完成 8 題需求訪談定案並寫入 `raw/00-interview-and-requirements.md`。
  - 建立原始文獻層 `raw/01` ～ `raw/06` 共 6 篇權威規格文獻，完成對 Unit 01～03 的來源回補，並將 Backlog 中的 Unit 04（`svg-refraction-displacement`）、Unit 05（`dynamic-light-tracking`）、Unit 06（`accessibility-fallback`）全數生成 `notes/*.md` 原稿與五段式互動講義 `lessons/*/index.html`，建立 `wiki/index.md` 總索引。
  - 依課程 Slide 43–47 建立檔案化 Graph + Loop 工作流（`.agents/workflows/topic-slides.md`、`workflow/sources.md`、`workflow/cards/card-01..06.md`、`workflow/outline.md`、`workflow/drafts/slides-draft.md`），產出 12 頁新手向教學 HTML 簡報 `slides/index.html`（每頁附 Wiki 出處與互動實驗室連結）。
  - 開發可執行檢查腳本 `workflow/check_slides.py`；執行過程中第 1 輪偵測到解析器未跳過 HTML 空標籤（`<br>`）、第 2 輪真實攔截 S04/S05/S07/S12 字數溢出（> 420 字），僅局部精簡該 4 頁後於第 3 輪達成 `Exit Code 0` 全過並留存於 `workflow/report.md` 與 `WEEK10_SUBMISSION.md`。
- **影響檔案**：
  - 新增 `raw/*`（7 檔）、`wiki/index.md`、`notes/svg-refraction-displacement.md`、`notes/dynamic-light-tracking.md`、`notes/accessibility-fallback.md`
  - 新增 `lessons/svg-refraction-displacement/index.html`、`lessons/dynamic-light-tracking/index.html`、`lessons/accessibility-fallback/index.html`
  - 新增 `slides/index.html`、`.agents/workflows/topic-slides.md`、`workflow/*`、`WEEK10_SUBMISSION.md`
  - 更新 `index.html`、`AGENTS.md`、`CLAUDE.md`、`README.md`、`NOTES.md`、`notes/blur-and-saturation.md`、`notes/bevel-and-refraction.md`、`notes/gpu-compositing-and-agents.md`、`lessons/gpu-compositing-and-agents/index.html`

---

## [2026-11-17] v2.1 — 升級 Unit 03 互動實驗室為真實 GPU 渲染與即時 FPS 壓測

- **變更內容**：
  - 將 `lessons/gpu-compositing-and-agents/index.html` 的第四段實驗室從公式估算升級為真實瀏覽器渲染壓測：依滑桿與嵌套開關在舞台動態掛載 `1 ～ 80` 個真實 `backdrop-filter` DOM 節點，搭配 `requestAnimationFrame` 移動底層光球強迫 GPU 每幀重繪。
  - 新增 `performance.now()` 即時 FPS、Frame Time（`ms`）、Jank 計數與 Canvas 60 幀波形圖（含 `16.7ms` 基準線）。
  - 同步更新 `notes/gpu-compositing-and-agents.md` 規格。
- **影響檔案**：
  - `notes/gpu-compositing-and-agents.md`、`lessons/gpu-compositing-and-agents/index.html`、`log.md`

---

## [2026-11-17] v2.0 — 全面轉型為「Aero Glass 與介面光學設計知識庫」

- **變更決策**：
  - 依使用者要求，將知識庫主題與全站視覺風格全面改版為 **「Vista Aero × Apple Liquid Glass 光學介面設計知識庫」**。
  - 鎖定五大核心 CSS 技巧於 `AGENTS.md` / `CLAUDE.md`：`backdrop-filter: blur(20px) saturate(190%)` 鮮豔度補償、左上亮／右下暗光學倒角與 `inset` 1px 內陰影、`.glass-panel::before` 上半部 50% 鏡面反光切面、`.vista-text` 白色防護光暈、以及 2%～4% 不透明度的 SVG `feTurbulence` 微觀雜訊。
  - 訂定 **GPU 合成圖層效能預算守則**：為防止行動裝置幀率下滑，規定次級嵌套子元件改採半透明實底而非重疊多層 `backdrop-filter`。
  - 移除舊 GenAI 示範單元（`rag-architecture`、`reflection-agent`、`agentic-workflow`），依「內容先行」流程全面重建為三個光學單元：`blur-and-saturation`、`bevel-and-refraction`、`gpu-compositing-and-agents`。
- **影響檔案**：
  - `AGENTS.md`、`CLAUDE.md`、`NOTES.md`、`README.md`、`index.html`、`notes/_template.md`
  - 新增 `notes/blur-and-saturation.md`、`lessons/blur-and-saturation/index.html`
  - 新增 `notes/bevel-and-refraction.md`、`lessons/bevel-and-refraction/index.html`
  - 新增 `notes/gpu-compositing-and-agents.md`、`lessons/gpu-compositing-and-agents/index.html`

---

## [2026-11-17] v1.2 — 首批三個示範單元上線與 GitHub Pages 初次發布

- **變更內容**：完成初版專案骨架與 GitHub Pages 部署（`https://konayame774.github.io/genai-wiki-hub/`）。
- **影響檔案**：初版 `index.html`、`README.md`、初代三個示範單元。

---

## [2026-11-17] v1.0 — 專案初始化與基礎工作流確立

- **變更決策**：建立 Content-First（`notes/*.md` → `lessons/*/index.html`）、Self-Contained 單檔架構、kebab-case `<slug>` 三處對齊與全站相對路徑規範。
