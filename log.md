# log.md — 專案決策與變更歷史紀錄

> 本文件採「只增不刪（Append-Only）」原則，專門記錄會影響未來架構、設計規範或單元上線的重大變更，讓任何時間點接手的 AI 或開發者都能快速掌握規則演進脈絡。

---

## [2026-11-17] v1.2 — 首批三個核心單元上線與首頁整合完成

- **變更內容**：
  - 依據 `AGENTS.md` 四步標準工作流，依序完成 Unit 01（`rag-architecture`）、Unit 02（`reflection-agent`）、Unit 03（`agentic-workflow`）之 Markdown 原稿與互動式單元網頁。
  - 完成知識庫總覽首頁 `index.html`，實作分類篩選、即時關鍵字搜尋、`.card-soon` 一鍵複製 AI 擴充指令功能，以及 `AGENTS.md` 規則對照視覺化說明區。
  - 建立三單元之間的前後頁相對路徑串聯（Unit 01 ↔ Unit 02 ↔ Unit 03）。
- **影響檔案**：
  - `notes/rag-architecture.md`、`lessons/rag-architecture/index.html`
  - `notes/reflection-agent.md`、`lessons/reflection-agent/index.html`
  - `notes/agentic-workflow.md`、`lessons/agentic-workflow/index.html`
  - `index.html`、`NOTES.md`、`README.md`

---

## [2026-11-17] v1.1 — 確立內容先行範本與五段式網頁標準

- **變更決策**：
  - 制定 `notes/_template.md` 作為所有單元的標準 Markdown 知識原稿格式，確保「內容先行（Content-First）」。
  - 鎖定單元頁五段式結構：（1）Sticky 導覽與麵包屑（2）單元標頭與 TL;DR 摘要框（3）核心觀念卡與常見誤區提醒（4）原生 JS 互動實驗室（5）3 題隨堂測驗與前後單元導覽。
- **影響檔案**：
  - `notes/_template.md`、`AGENTS.md`、`CLAUDE.md`

---

## [2026-11-17] v1.0 — 專案初始化與設計系統定案

- **變更決策**：
  - 建立 **GenAI Atelier & Study Wiki** 專案骨架，採純靜態零建置（Zero-Build）與 Self-Contained 單檔架構，並加入 `.nojekyll` 支援 GitHub Pages 部署。
  - 確立「暖調學術實驗室風（Warm Technical Atelier）」設計規範，鎖定米白背景（`#FAF7F2`）、深岩灰粗線框（`#1E293B`）、靛藍主強調色（`#4F46E5`）等固定 CSS 變數與三款 Google Fonts（`Plus Jakarta Sans`、`Noto Sans TC`、`JetBrains Mono`）。
  - 同步建立 `AGENTS.md` 與 `CLAUDE.md`，明確約定 kebab-case `<slug>` 命名與全站相對路徑規範。
- **影響檔案**：
  - `AGENTS.md`、`CLAUDE.md`、`.nojekyll`、`.gitignore`、`NOTES.md`、`log.md`
