# GenAI Atelier & Study Wiki — GenAI 實戰講義與 LLM Wiki 知識庫

這是一個結合 **「LLM Wiki 結構化筆記」** 與 **「Self-Contained 互動式學習網頁」** 的可擴充靜態知識庫專案，同時作為 **【TAICA 生成式 AI：文字與圖像生成的原理與實務】第九週作業（建立 `AGENTS.md` / `CLAUDE.md`）** 之實作成果。

有別於一次性的 Vibe Coding（只求把單一頁面做出來），本專案的核心在於透過根目錄的 [`AGENTS.md`](./AGENTS.md)（與同步的 [`CLAUDE.md`](./CLAUDE.md)），建立一套讓 AI 協作代理能長期讀懂並持續擴充新單元的標準化生產線。

---

## ✨ 專案特色

- **內容先行（Content-First）**：所有網頁生成前，必先在 `notes/<slug>.md` 建立結構化知識原稿（LLM Wiki 層），再轉換成網頁成品，確保教學邏輯與文字精準度。
- **單檔獨立（Self-Contained）**：每份單元網頁 `lessons/<slug>/index.html` 均內嵌完整 CSS 與原生 JavaScript，無需 Node.js、建置工具或 API Key，雙擊檔案或部署於 GitHub Pages 即可完整運作。
- **固定視覺系統（Warm Technical Atelier）**：透過 `AGENTS.md` 鎖定色票變數、字體與「五段式教學骨架」，保證未來擴充第 4、第 10 個單元時視覺風格依然一致。
- **真實原生 JS 互動實驗室**：每個單元皆附帶免 API Key 的實戰模擬器（Chunk Size 檢索實驗、Reflection 三階段演化、Agent Readiness 診斷室）與即時批改測驗。

---

## 📁 目錄架構

```text
genai-wiki-hub/
├── index.html                  # 知識庫首頁（分類篩選、即時搜尋、單元卡片與擴充指南）
├── AGENTS.md                   # AI 協作規範與專案開發憲法
├── CLAUDE.md                   # 與 AGENTS.md 同步之規範檔（相容 Claude 系列工具）
├── README.md                   # 專案說明文件
├── NOTES.md                    # 現況白板（已完成清單與待擴充 Backlog）
├── log.md                      # 決策與變更歷史紀錄（只增不刪）
├── .nojekyll                   # 停用 GitHub Pages Jekyll 處理
├── .gitignore                  # 忽略系統與編輯器暫存檔
├── notes/                      # 【知識原稿層 / LLM Wiki】
│   ├── _template.md            # 新增單元標準範本
│   ├── rag-architecture.md     # Unit 01 原稿
│   ├── reflection-agent.md     # Unit 02 原稿
│   └── agentic-workflow.md     # Unit 03 原稿
└── lessons/                    # 【互動網頁成品層】
    ├── rag-architecture/index.html
    ├── reflection-agent/index.html
    └── agentic-workflow/index.html
```

---

## 🚀 如何用 AI 繼續擴充新單元？

當你需要新增下一個主題（例如 `NOTES.md` Backlog 中的 Unit 04 `prompt-engineering`）時，只需對 AI 代理（如 Antigravity、Claude Code、Cursor）下達以下指令：

> 「請先閱讀專案根目錄的 `AGENTS.md`、`NOTES.md` 與 `log.md`。我想新增 Unit 04，主題為『Prompt 工程與結構化輸出』（slug：`prompt-engineering`，分類：`AI 工作流`）。請嚴格依照 `AGENTS.md` 的 4 步標準工作流完成原稿、互動講義網頁、首頁卡片串接與狀態更新。」

AI 便會自動依序完成：
1. 依 `notes/_template.md` 撰寫 `notes/prompt-engineering.md`
2. 依固定色票與五段式骨架生成 `lessons/prompt-engineering/index.html`
3. 更新 `index.html` 首頁卡片與前一單元的「下一單元」導覽
4. 更新 `NOTES.md` 與 `log.md` 留存交接紀錄

---

## 🌐 部署至 GitHub Pages

1. 將本專案 Push 至你的 GitHub Repository（分支 `main`）。
2. 前往 GitHub Repository 的 **Settings → Pages**。
3. 在 **Build and deployment → Source** 選擇 `Deploy from a branch`，Branch 選 `main`、資料夾選 `/ (root)` 後點擊 Save。
4. 由於全站採用相對路徑且已附上 `.nojekyll`，部署完成後即可透過 `https://<你的帳號>.github.io/<repo-name>/` 正常瀏覽所有頁面與互動實驗室。
