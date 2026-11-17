# log.md — 專案決策與變更歷史紀錄

> 本文件採「只增不刪（Append-Only）」原則，專門記錄會影響未來架構、設計規範或單元上線的重大決策。

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
