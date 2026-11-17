# AGENTS.md — GenAI 實戰講義與 LLM Wiki 知識庫（專案開發規範）

> 本文件（`AGENTS.md`）是 **「GenAI 實戰講義與 LLM Wiki 知識庫（GenAI Atelier & Study Wiki）」** 給 AI 協作代理與人類作者閱讀的「專案憲法」。
> 為了同時相容不同 AI 工具（如 Antigravity、Claude Code / Cowork、Cursor、Codex），根目錄中的 `CLAUDE.md` 與本檔案內容完全同步；修改規範時請務必同步更新兩者，並在 `log.md` 留下記錄。
> **任何開發或擴充任務開始前，請先依序閱讀：`AGENTS.md` → `NOTES.md` → `log.md`。**

---

## 一、專案目的與核心理念

本專案是一個專為生成式 AI 學習者打造的 **「可持續擴充式互動講義與 LLM Wiki 知識庫」**，並作為可部署於 GitHub Pages 的純靜態網站。

與一次性的 Vibe Coding（「只把單一頁面做出來」）不同，本專案的核心目標是建立一套 **高可讀性、低耦合、可重複複製的生產規則**：

1. **內容先行（Content-First）**：所有知識單元都必須先在 `notes/<slug>.md` 完成結構化的 Markdown 知識原稿（LLM Wiki 筆記層），才生成對應的 `lessons/<slug>/index.html`（網頁成品層）。AI 不可跳過原稿直接生出 HTML。
2. **Self-Contained 單檔獨立架構**：每一個講義單元頁 `lessons/<slug>/index.html` 都必須是可獨立運作的單一 HTML 檔案——所有版面 CSS 與互動實驗室 JavaScript 一律內嵌於該檔案中（外部僅允許載入 Google Fonts），不依賴任何建置工具（Webpack/Vite）、不需後端伺服器、不需 API Key 即可直接在瀏覽器體驗。
3. **繁體中文語境與教學溫度**：全站使用臺灣繁體中文慣用術語，中文行文一律使用**全形標點符號**（，。、：「」！？（）），專有名詞或程式碼才使用半形英文與等寬字體標記。

---

## 二、網頁整體視覺風格與設計系統（Brand & Design Tokens）

全站統一採用 **「暖調學術實驗室風（Warm Technical Atelier）」**：以溫暖米白紙感為底，搭配深岩灰粗線框（2px solid）與微偏移硬陰影（Neobrutalist-lite 卡片感），兼顧筆記本的閱讀親和力與工程實驗室的精準結構。

### 1. 固定色票（CSS Variables，嚴禁擅自替換）

所有 HTML 頁面（首頁與各單元頁）的 `:root` 必須包含並使用以下 CSS 變數：

```css
:root {
  --bg-cream: #FAF7F2;          /* 全站暖米白紙質背景 */
  --bg-card: #FFFFFF;           /* 卡片與內容區塊純白底 */
  --bg-subtle: #F2ECE1;         /* 次要區塊、程式碼或提示底色 */
  --ink-primary: #1E293B;       /* 主標題與高對比文字／邊框線色 */
  --ink-secondary: #475569;     /* 內文說明、副標題與次要資訊 */
  --accent-indigo: #4F46E5;     /* 主強調色：互動按鈕、核心標籤、連結 */
  --accent-indigo-soft: #EEF2FF;/* 靛藍淺底：核心觀念亮點區 */
  --accent-amber: #F59E0B;      /* 警告、重點提示與待擴充強調色 */
  --accent-amber-soft: #FEF3C7; /* 琥珀淺底：TL;DR 或常見誤區提醒 */
  --accent-emerald: #10B981;    /* 正確答案、已完成狀態與正向指標 */
  --accent-rose: #F43F5E;       /* 錯誤選項、反面教材與風險警示 */
  --border-strong: 2px solid #1E293B;
  --shadow-card: 5px 5px 0px rgba(30, 41, 59, 0.12);
}
```

### 2. 字體規範（Google Fonts）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Noto+Sans+TC:wght@400;500;700;900&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
```

- **英文標題／數字／徽章**：`'Plus Jakarta Sans', 'Noto Sans TC', sans-serif`
- **中文內文**：`'Noto Sans TC', 'Plus Jakarta Sans', sans-serif`
- **程式碼／Slug／檔案路徑**：`'JetBrains Mono', monospace`

### 3. 背景與元件視覺語言

- **點陣格紋底**：`body` 背景色為 `var(--bg-cream)`，疊加細微點陣格紋 `radial-gradient(#D8CFC2 1.2px, transparent 1.2px)`（間距 `24px 24px`）。
- **卡片規範**：圓角 `16px`、邊框 `var(--border-strong)`、陰影 `var(--shadow-card)`；互動卡片 Hover 時位移 `translate(-2px, -2px)` 並加深陰影。
- **響應式要求**：所有頁面必須支援手機與桌面瀏覽（版心最大寬度 `1080px`、水平置中、`padding: 0 20px`），避免任何水平捲軸溢出。

---

## 三、檔案命名與資料夾放置規則

### 1. 專案目錄樹

```text
genai-wiki-hub/                 ← GitHub Repository 根目錄（GitHub Pages 部署根目錄）
├── index.html                  ← 知識庫總覽首頁（含篩選、搜尋、單元卡片與擴充指南）
├── AGENTS.md                   ← 本文件（AI 與人類共讀的核心開發憲法）
├── CLAUDE.md                   ← 與 AGENTS.md 完全同步的指引檔
├── README.md                   ← GitHub Repository 說明文件
├── NOTES.md                    ← 現況白板：目前完成進度、待擴充 Backlog、交接備忘
├── log.md                      ← 決策與變更紀錄：只增不刪的重大架構與上線紀錄
├── .nojekyll                   ← 停用 Jekyll，確保靜態網站與資料夾直接對外提供服務
├── .gitignore                  ← 忽略作業系統暫存檔與編輯器暫存檔
├── notes/                      ← 【內容先行層 / LLM Wiki 原稿】
│   ├── _template.md            ← 新增單元時必用的 Markdown 標準範本
│   ├── rag-architecture.md     ← 單元 01 原稿
│   ├── reflection-agent.md     ← 單元 02 原稿
│   └── agentic-workflow.md     ← 單元 03 原稿
└── lessons/                    ← 【網頁成品層】每個單元一個獨立資料夾
    ├── rag-architecture/
    │   └── index.html          ← 單元 01 互動講義頁
    ├── reflection-agent/
    │   └── index.html          ← 單元 02 互動講義頁
    └── agentic-workflow/
        └── index.html          ← 單元 03 互動講義頁
```

### 2. 命名慣例（Slug Consistency）

- 所有 `<slug>` **一律使用英文小寫與連字號（kebab-case）**，例如 `rag-architecture`、`prompt-engineering`，禁止空白、大寫字母或中文字元（確保 GitHub Pages URL 友善）。
- **三處對齊原則**：每新增一個學習單元，以下三個位置的 `<slug>` 必須完全一致：
  1. 原稿路徑：`notes/<slug>.md`
  2. 網頁路徑：`lessons/<slug>/index.html`
  3. 首頁卡片連結：根目錄 `index.html` 中指向 `lessons/<slug>/index.html`

### 3. 路徑引用鐵則（GitHub Pages 相對路徑）

因為專案可能部署在 `https://<username>.github.io/<repo-name>/` 子路徑下，**全站嚴禁使用以 `/` 開頭的根絕對路徑（例如 `/lessons/...`）**，一律使用相對路徑：
- 首頁連結至單元頁：`lessons/<slug>/index.html`
- 單元頁返回首頁：`../../index.html`
- 單元頁連結至前／後單元：`../<other-slug>/index.html`

---

## 四、頁面結構與標準元件規格

### 1. 首頁（`index.html`）結構

1. **頂部品牌列（Topbar）**：專案標誌 `GenAI Atelier`、副標「LLM Wiki × 互動講義庫」、快速連往 `AGENTS.md` / GitHub 說明區的錨點。
2. **Hero 區與知識庫統計**：主標題、專案宗旨介紹，以及動態或結構化的統計徽章（已完成單元數、互動實驗室數、規則版本）。
3. **分類篩選與即時搜尋列**：
   - 分類按鈕：依 `data-category` 篩選（例如「全部」、「檢索增強」、「Agent 架構」、「AI 工作流」）。
   - 即時搜尋框：可依單元標題、摘要或標籤即時過濾卡片。
4. **單元卡片網格（`.lesson-grid`）**：
   - 每張已完成卡片顯示：單元編號膠囊（`UNIT 01`）、分類標籤、標題、一句話摘要、關鍵字 Tags、預估閱讀時間、前往閱讀按鈕。
   - 網格末尾保留 1 張 **虛線待擴充預留卡（`.card-soon`）**，顯示下一個建議新增的單元（來自 `NOTES.md` 的 Backlog），並附帶「一鍵複製 AI 擴充指令」按鈕。
5. **`AGENTS.md` 規則對照與協作流程區**：視覺化展示本網站如何透過 `AGENTS.md` + `notes/_template.md` + `NOTES.md` 實現永續擴充。

### 2. 單元講義頁（`lessons/<slug>/index.html`）固定五段式結構

每一個單元網頁都必須嚴格遵守以下五段式骨架，確保學習體驗一致：

1. **第一段：頂部導覽與麵包屑列（Sticky Topbar）**
   - 左側：`← 返回知識庫首頁`（`../../index.html`）與麵包屑 `首頁 / <分類> / Unit XX`。
   - 右側：快速跳轉錨點（`核心觀念`、`互動實驗室`、`隨堂檢測`）。
2. **第二段：單元標頭與「一句話核心觀念（TL;DR）」**
   - 單元編號膠囊、分類徽章、閱讀時間、主標題與副標題。
   - 使用 `--accent-amber-soft` 底色與粗邊框呈現的 **TL;DR 摘要框**，讓學生 10 秒內掌握本單元核心價值。
3. **第三段：核心觀念拆解（Concept Cards ＋ 常見誤區提醒）**
   - 至少包含 **3 張結構化觀念卡片**（例如架構流程、步驟拆解、優缺點比較表或程式碼對照）。
   - 至少包含 **1 個「常見誤區／地雷提醒（Pitfall Alert）」** 區塊，點出初學者最常犯錯的地方。
4. **第四段：原生 JS 互動實驗室（Interactive Lab）**
   - **本專案最大特色**：每個單元必須設計一個貼合該主題的 **免 API Key 原生 JavaScript 互動模擬器**（例如滑桿調整參數、步驟切換器、情境診斷勾選表等），並以視覺化面板即時呈現輸出變化。
   - 狀態一律保存於 JS 記憶體變數中，不依賴 `localStorage` 或外部 API。
5. **第五段：隨堂自我檢測（Quiz）與頁尾導覽（Prev / Next）**
   - 包含 **3 題單選題**，使用者點擊選項後立即批改（顯示正確 `--accent-emerald` 或錯誤 `--accent-rose` 樣式）並展開「解析說明」。
   - 頁面底部提供「上一單元」與「下一單元」導覽按鈕（沒有則顯示返回首頁）。

---

## 五、新增內容時要遵守的格式與 4 步標準工作流

當使用者要求「新增一個單元」或「擴充新頁面」時，AI 必須嚴格依照以下 4 個步驟執行，不可遺漏：

- **Step 1：撰寫知識原稿（內容先行）**
  - 複製 `notes/_template.md` 的格式，建立 `notes/<new-slug>.md`。
  - 填寫完整 Meta 資訊（單元編號、標題、Slug、分類、閱讀時間、標籤）與五段式正文、互動實驗室規格及 3 題測驗題庫。
- **Step 2：生成獨立網頁成品**
  - 嚴格遵循 `AGENTS.md` 第二節色票字體與第四節五段式結構，生成 `lessons/<new-slug>/index.html`。
  - 所有 CSS 與互動 JS 皆內嵌於該 `index.html` 中，確定互動實驗室與隨堂測驗皆可正常運作。
- **Step 3：更新首頁與單元間導覽連結**
  - 在根目錄 `index.html` 的 `.lesson-grid` 中（於 `.card-soon` 之前）加入新單元的卡片，確認 `data-category` 與篩選按鈕一致（若是新分類則同步新增篩選按鈕與統計數字）。
  - 更新前一單元的「下一單元」連結，確保學習路徑串聯完整；並更新 `.card-soon` 指向下一個待辦單元。
- **Step 4：更新管理紀錄（白板與歷史）**
  - 更新 `NOTES.md`：將新單元移入「已完成單元清單」，從待辦 Backlog 移除，並更新最新進度摘要。
  - 更新 `log.md`：在檔案最上方或紀錄區尾端追加一筆日期、變更內容與影響檔案之紀錄（不可刪除舊紀錄）。

### 給 AI 的一鍵擴充 Prompt 範本

> 「請先閱讀專案根目錄的 `AGENTS.md`、`NOTES.md` 與 `log.md`。我想新增 Unit 04，主題為『Prompt 工程與結構化輸出』（slug：`prompt-engineering`，分類：`AI 工作流`）。請嚴格依照 `AGENTS.md` 的 4 步標準工作流：先依 `notes/_template.md` 建立 `notes/prompt-engineering.md`，再生成五段式互動講義 `lessons/prompt-engineering/index.html`（含專屬原生 JS 互動實驗室與 3 題測驗），接著更新 `index.html` 首頁卡片與上一單元的導覽連結，最後更新 `NOTES.md` 與 `log.md`。」

---

## 六、AI 修改或新增內容時必須遵守的 8 條鐵則

1. **先讀憲法與白板**：開始任何任務前，必先讀取 `AGENTS.md`、`NOTES.md` 與 `log.md`。
2. **內容先行不可跳過**：必須先有 `notes/<slug>.md` 原稿，才允許生成或大幅修改 `lessons/<slug>/index.html`；日後修改文字也應同步維護原稿與網頁一致。
3. **鎖定設計系統**：不得擅自更改 `:root` 中的 CSS 色票變數與 Google Fonts 字體設定；卡片框線與陰影風格須全站統一。
4. **強制相對路徑**：所有 HTML 內部超連結只能使用相對路徑（`lessons/...`、`../../index.html`、`../...`），禁止硬寫網域或 `/` 開頭根路徑。
5. **單檔 Self-Contained**：每個單元網頁只依賴 Google Fonts，其餘 CSS、SVG 圖示與互動 JS 必須全部寫在同一個 `index.html` 內，確保離線或雙擊檔案也能開啟。
6. **互動必須真實可用**：第四段的互動實驗室與第五段的隨堂測驗禁止使用假按鈕或靜態圖片替代，必須有真實可點擊的原生 JS 狀態變化與即時回饋。
7. **全形中文標點與無錯別字**：臺灣繁體中文內文一律使用全形標點符號，並維持清晰親切且具工程準確性的教學口吻。
8. **收尾必更新白板與紀錄**：每次新增或修改完成後，必須更新 `NOTES.md`（現況與下次接手點）與 `log.md`（變更歷史），並同步檢查 `AGENTS.md` 與 `CLAUDE.md` 是否一致。
