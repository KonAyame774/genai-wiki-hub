# Aero Glass & Optical UI Wiki — Aero Glass 與介面光學設計知識庫（第 9～10 週實作成果）

- **🌐 知識庫首頁（GitHub Pages）**：https://konayame774.github.io/genai-wiki-hub/
- **🎓 第 10 週教學 HTML 簡報**：https://konayame774.github.io/genai-wiki-hub/slides/
- **📚 LLM Wiki 知識總圖譜**：[`wiki/index.md`](./wiki/index.md)
- **📝 第 10 週作業完整繳交報告**：[`WEEK10_SUBMISSION.md`](./WEEK10_SUBMISSION.md)
- **📦 GitHub Repository**：https://github.com/KonAyame774/genai-wiki-hub

這是一座結合 **「Vista Aero 鏡面反光與文字光暈」** 及 **「Apple Liquid Glass 背景彩度補償、動態追光與 SVG 折射」** 的 LLM Wiki 知識庫與教學簡報平台，完整整合 **【TAICA 生成式 AI 第 9 週（`AGENTS.md` 憲法驅動）】** 與 **【第 10 週（先討論後 Ingest 6 篇原始文獻 ＋ Graph + Loop 工作流製作教學 HTML 簡報）】** 之實作成果。

---

## ✨ 知識庫與簡報架構亮點

1. **先討論、後生成的四層知識架構（Ingest 6 篇權威文獻）**：
   - `raw/00-interview-and-requirements.md`：記錄 8 題需求訪談定案與 Lint 驗收準則。
   - `raw/01` ～ `raw/06`：收錄 W3C `backdrop-filter`、Vista DWM Aero、SVG `feTurbulence` / `feDisplacementMap`、Apple Specular Pointer Tracking、Chromium GPU 合成與 WCAG 2.2 無障礙規範共 6 篇原始文獻。
   - `notes/*.md` & `lessons/*/index.html`：涵蓋 **Unit 01 ～ Unit 06** 六個單檔互動光學實驗室，並由 [`wiki/index.md`](./wiki/index.md) 建立雙向索引。
2. **Graph + 節點內 Loop 工作流產出 12 頁教學 HTML 簡報（[`slides/index.html`](./slides/index.html)）**：
   - 嚴格執行 [`.agents/workflows/topic-slides.md`](./.agents/workflows/topic-slides.md)：檢索覆蓋關卡 → 平行 6 張證據卡（權限隔離） → 大綱審核 → 逐頁稿與渲染 → **`python workflow/check_slides.py` 腳本驗證（12/12 頁通過、6 單元 100% 覆蓋、Exit Code 0）**。

---

## 📁 目錄架構

```text
genai-wiki-hub/
├── index.html                          # 光學知識庫首頁（6 單元卡片、分類搜尋、簡報入口）
├── AGENTS.md / CLAUDE.md               # 同步之專案開發憲法與五大光學 CSS / GPU 預算
├── NOTES.md / log.md                   # 現況白板與只增不刪的架構演進紀錄
├── WEEK10_SUBMISSION.md                # 第 10 週作業繳交完整報告與反思
├── raw/                                # 【原始文獻層】00 需求訪談 ＋ 01～06 技術文獻
├── wiki/index.md                       # 【LLM Wiki 索引】全站單一事實數據與雙向對照表
├── notes/                              # 【內容先行層】Unit 01～06 Markdown 原稿與範本
├── lessons/                            # 【互動講義成品層】Unit 01～06 單檔互動實驗室
├── slides/index.html                   # 【教學簡報層】12 頁新手向互動 HTML 簡報（含出處條）
├── .agents/workflows/topic-slides.md   # Graph + Loop 工作流規格書
└── workflow/                           # Graph 中間產物、check_slides.py 與 report.md
```

---

## 🧪 本機驗證方式

```bash
python workflow/check_slides.py
```

確認所有 12 頁投影片皆無字數溢出（`<= 420` 字）、Unit 01～06 覆蓋率達 `100%`、關鍵光學數據未寫反且全站相對路徑零斷鏈。
