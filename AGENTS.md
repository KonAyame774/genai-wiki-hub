# AGENTS.md — Aero Glass 與介面光學設計知識庫（專案開發憲法）

> 本文件（`AGENTS.md`）是 **「Aero Glass 與介面光學設計知識庫（Aero Glass & Optical UI Wiki）」** 給 AI 協作代理與人類作者閱讀的「專案憲法」。
> 為了同時相容不同 AI 工具（Antigravity、Claude Code / Cowork、Cursor、Codex），根目錄中的 `CLAUDE.md` 與本檔案內容完全同步；修改任何規範時請務必同步更新兩者，並在 `log.md` 留下記錄。
> **任何開發或擴充任務開始前，請先依序閱讀：`AGENTS.md` → `NOTES.md` → `log.md`。**

---

## 一、專案目的與核心理念

本專案是一個專為前端設計師與工程師打造的 **「Aero Glass × Apple Liquid Glass 光學介面實作與理論知識庫」**，並以純靜態網頁部署於 GitHub Pages。

與一次性的 Vibe Coding（「只把單一頁面做出來」）不同，本專案透過明確的 **物理光學 CSS 規範** 與 **可持續擴充架構**，確保無論未來新增第 4 個還是第 10 個單元，整座知識庫的光學質感與教學骨架都保持高度一致：

1. **內容先行（Content-First）**：所有知識單元都必須先在 `notes/<slug>.md` 完成結構化的 Markdown 原稿，才生成對應的 `lessons/<slug>/index.html`。AI 不可跳過原稿直接生出 HTML。
2. **Self-Contained 單檔獨立架構**：每一個單元頁 `lessons/<slug>/index.html` 都必須是單一自給自足的 HTML 檔案——所有光學 CSS、SVG 雜訊與原生 JavaScript 實驗室皆內嵌於該檔案中（外部僅允許載入 Google Fonts），不依賴建置工具或後端 API。
3. **臺灣繁體中文語境**：行文使用臺灣繁體中文慣用術語與全形標點符號（，。、：「」！？（）），專有名詞或 CSS 屬性則使用等寬字體標記。

---

## 二、網頁整體視覺風格與五大關鍵 CSS 光學規範

全站統一採用 **「Vista Aero × Apple Liquid Glass 光學毛玻璃設計系統」**：以充滿深海極光與水彩光暈的流體背景襯托半透明 `.glass-panel` 容器，重現物理玻璃的厚度、折射與微觀磨砂觸感。

### 1. 色彩與底層流體背景（Vibrant Mesh Backdrop）

毛玻璃需要色彩豐富的底層畫面才能展現折射深度，嚴禁使用死板純白或單調全黑背景。

```css
:root {
  --bg-deep: #0b192c;
  --aurora-cyan: #0ea5e9;
  --aurora-teal: #14b8a6;
  --aurora-indigo: #4f46e5;
  --aurora-aqua: #38bdf8;
  --ink-dark: #1c1c1e;
  --ink-body: #1e293b;
  --ink-muted: #475569;
  --glass-bg-top: rgba(255, 255, 255, 0.28);
  --glass-bg-bottom: rgba(255, 255, 255, 0.08);
  --glass-border: rgba(255, 255, 255, 0.22);
  --glass-border-top: rgba(255, 255, 255, 0.72);
  --glass-border-left: rgba(255, 255, 255, 0.52);
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;
  --accent-rose: #f43f5e;
}
```

### 2. 五大關鍵 CSS 光學技巧（核心規格，必須實作於全站容器）

1. **背景模糊與鮮豔度補償（Blur + Saturate Compensation）**
   - 單純使用 `blur()` 會讓透出來的底層背景發灰濁；必須同時使用 `backdrop-filter: blur(20px) saturate(190%)`（與 `-webkit-backdrop-filter`），強迫提升底層色彩飽和度，重現通透清亮感。
2. **物理厚度與倒角光線（Optical Bevel & Inset Thickness）**
   - 頂部與左側邊框設定高透明度白光（`border-top-color: rgba(255, 255, 255, 0.7)`、`border-left-color: rgba(255, 255, 255, 0.5)`），右側與底部維持極淡邊框（`rgba(255, 255, 255, 0.2)`）。
   - 疊加外層擴散陰影與 1px 內側上下高光／暗角：`box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), inset 0 1px 0 0 rgba(255, 255, 255, 0.8), inset 0 -1px 0 0 rgba(0, 0, 0, 0.1);`
3. **表面折射與高光切面（Vista Specular 50% Cut）**
   - 使用 `.glass-panel::before` 偽元素（`height: 50%`、`pointer-events: none`）搭配線性漸層 `linear-gradient(180deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.05) 100%)`，在 50% 處產生非連續性階躍，切出 Vista Aero 經典的上半部鏡面反射光斑分界線。
4. **Vista 風格的文字光暈（`.vista-text` Halo）**
   - 標題與半透明背景上的關鍵深色文字（`color: #1c1c1e`）加上雙層白光防護：`text-shadow: 0 0 8px rgba(255, 255, 255, 0.9), 0 0 16px rgba(255, 255, 255, 0.5);`，避免背景彩光干擾辨識度。
5. **玻璃微觀雜訊（SVG Noise Data URI）**
   - 利用內嵌 SVG `feTurbulence` Noise Data URI 作為微觀背景層，將不透明度壓低至 `2%～4%`（`opacity: 0.03`），消弭大面積漸層的色階斷裂（Banding），注入細緻的磨砂實體觸感。

### 3. 標準 `.glass-panel` 基準程式碼（所有主要面板與卡片皆須遵循）

```css
.glass-panel {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
  backdrop-filter: blur(20px) saturate(190%);
  -webkit-backdrop-filter: blur(20px) saturate(190%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-top-color: rgba(255, 255, 255, 0.7);
  border-left-color: rgba(255, 255, 255, 0.5);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 0 rgba(0, 0, 0, 0.1);
}

.glass-panel::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.05) 100%
  );
  pointer-events: none;
}

.vista-text {
  color: #1c1c1e;
  font-weight: 600;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.9),
    0 0 16px rgba(255, 255, 255, 0.5);
}
```

### 4. GPU 合成效能預算守則（Performance Guardrail）

`backdrop-filter` 會強迫瀏覽器開闢獨立的 GPU 合成圖層，並在底層內容變更時進行即時重繪：
- **禁止無限嵌套**：外層已啟用 `backdrop-filter` 的 `.glass-panel` 內部次級子卡片，應改用高通透半透明實底（例如 `rgba(255, 255, 255, 0.58)` 搭配細白邊框），避免同區域疊加多層即時模糊造成低階行動裝置 FPS 下滑。
- **避免滾動視差大面積動畫疊加模糊**：背景極光裝飾維持靜態或極低成本位移，不與大面積 `blur()` 動畫同時重繪。

### 5. 字體規範（Google Fonts）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Noto+Sans+TC:wght@400;500;700;900&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
```

---

## 三、檔案命名與資料夾放置規則

### 1. 專案目錄樹

```text
genai-wiki-hub/                         ← GitHub Repository 根目錄（GitHub Pages 部署根目錄）
├── index.html                          ← 光學知識庫首頁（6 單元卡片、分類搜尋、Graph/Loop 與規範區）
├── AGENTS.md                           ← 本文件（AI 與人類共讀的核心開發憲法）
├── CLAUDE.md                           ← 與 AGENTS.md 完全同步的指引檔
├── README.md                           ← 專案說明文件
├── NOTES.md                            ← 現況白板：目前進度、待擴充 Backlog、交接備忘
├── log.md                              ← 決策與變更紀錄：只增不刪的架構演進歷史
├── WEEK10_SUBMISSION.md                ← 第 10 週作業繳交完整報告與反思紀錄
├── raw/                                ← 【原始文獻層】6 篇權威技術規格＋00 需求訪談定案
├── wiki/
│   └── index.md                        ← 【知識總索引】raw → notes → lessons → slides 對照圖譜
├── notes/                              ← 【內容先行層 / 6 單元知識原稿】
│   ├── _template.md
│   ├── blur-and-saturation.md          ← Unit 01 原稿
│   ├── bevel-and-refraction.md         ← Unit 02 原稿
│   ├── gpu-compositing-and-agents.md   ← Unit 03 原稿
│   ├── svg-refraction-displacement.md  ← Unit 04 原稿
│   ├── dynamic-light-tracking.md       ← Unit 05 原稿
│   └── accessibility-fallback.md       ← Unit 06 原稿
├── lessons/                            ← 【互動講義成品層】Unit 01～06 獨立單檔實驗室
├── slides/
│   └── index.html                      ← 【第 10 週教學 HTML 簡報】12 頁互動簡報（含出處列）
├── .agents/workflows/topic-slides.md   ← Graph + Loop 自動生成簡報工作流規格
└── workflow/                           ← Graph 狀態產出物（sources / cards / outline / drafts / check_slides.py / report）
```

### 2. 命名與相對路徑鐵則

- 所有 `<slug>` **一律使用英文小寫與連字號（kebab-case）**，且 `notes/<slug>.md`、`lessons/<slug>/index.html`、`index.html` 卡片連結三處完全一致。
- **嚴禁使用 `/` 開頭的根絕對路徑**：
  - 首頁連至單元：`lessons/<slug>/index.html`
  - 單元返回首頁：`../../index.html`
  - 單元連至前後單元：`../<other-slug>/index.html`

---

## 四、頁面結構與標準元件規格

### 1. 首頁（`index.html`）結構

1. **Sticky Aero 導覽列**：`Aero Glass Wiki` 品牌標章、章節錨點。
2. **Hero 光學展示面板（`.glass-panel`）**：含 `.vista-text` 主標、專案核心主張與即時統計儀表（已上線單元、光學實驗室、測驗題數、GPU 預算合規率）。
3. **分類篩選與搜尋列**：分類按鈕（「全部」、「光學基底」、「表面折射」、「效能與規範」）與關鍵字即時搜尋。
4. **單元卡片網格（`.lesson-grid`）**：每張卡片套用 `.glass-panel` 物理倒角與鏡面反光切面，末尾保留 1 張虛線待擴充預留卡（`.card-soon`），支援一鍵複製 Unit 04 擴充指令。
5. **`AGENTS.md` 規則對照與 `.glass-panel` 標準程式碼區**：直接展示可一鍵複製的標準 CSS 範例與四步擴充流程。

### 2. 單元講義頁（`lessons/<slug>/index.html`）固定五段式結構

1. **第一段：Sticky Aero 導覽列與麵包屑**（`← 返回知識庫首頁`、`首頁 / <分類> / Unit XX`、章節跳轉連結）。
2. **第二段：單元標頭與「一句話核心觀念（TL;DR）」**（單元編號膠囊、閱讀時間、毛玻璃摘要框）。
3. **第三段：核心觀念拆解**（至少 **3 張** 結構化觀念卡片＋ **1 個常見誤區／效能地雷提醒框**）。
4. **第四段：原生 JS 互動光學實驗室（Interactive Lab）**（免 API Key 即時調整光學參數、CSS 預覽與即時程式碼輸出，狀態存於 JS 記憶體）。
5. **第五段：隨堂自我檢測（3 題單選題，點擊即時批改＋詳解）與頁尾前後單元導覽**。

---

## 五、新增內容時要遵守的 4 步標準工作流

當使用者要求「新增一個單元」時，AI 必須嚴格依照以下 4 步執行：

- **Step 1：撰寫知識原稿（內容先行）** — 複製 `notes/_template.md` 建立 `notes/<new-slug>.md`，完成 Meta、TL;DR、3 張觀念卡、誤區、互動實驗室規格與 3 題測驗。
- **Step 2：生成獨立光學網頁成品** — 嚴格套用本檔第二節 `.glass-panel`、`.vista-text`、SVG Noise 與 GPU 預算守則，依五段式骨架生成 `lessons/<new-slug>/index.html`。
- **Step 3：更新首頁與單元間導覽連結** — 在 `index.html` 的 `.lesson-grid` 中（`.card-soon` 之前）加入新單元卡片，更新前一單元的「下一單元」連結與 `.card-soon` 待辦目標。
- **Step 4：更新管理紀錄** — 更新 `NOTES.md`（將新單元移入已完成區）與 `log.md`（只增不刪地寫入上線紀錄）。

### 給 AI 的一鍵擴充 Prompt 範本

> 「請先閱讀專案根目錄的 `AGENTS.md`、`NOTES.md` 與 `log.md`。我想新增 Unit 04，主題為『SVG 置換濾鏡與邊緣色散折射』（slug：`svg-refraction-displacement`，分類：`表面折射`）。請嚴格依照 `AGENTS.md` 的 4 步標準工作流：先依 `notes/_template.md` 建立 `notes/svg-refraction-displacement.md`，再生成套用 `.glass-panel` 規範的五段式互動講義 `lessons/svg-refraction-displacement/index.html`（含原生 JS 互動實驗室與 3 題測驗），接著更新 `index.html` 首頁卡片與上一單元的導覽連結，最後更新 `NOTES.md` 與 `log.md`。」

---

## 六、AI 修改或新增內容時必須遵守的 8 條鐵則

1. **先讀憲法與白板**：動工前必先讀取 `AGENTS.md`、`NOTES.md` 與 `log.md`。
2. **內容先行不可跳過**：必須先建立 `notes/<slug>.md`，才允許生成或大幅修改 `lessons/<slug>/index.html`。
3. **嚴守五大光學 CSS 規範**：所有主面板須正確運用 `blur() + saturate()`、左上倒角亮邊與 `inset` 陰影、`::before` 50% 鏡面切面、`.vista-text` 光暈與 2%～4% SVG 雜訊。
4. **遵守 GPU 合成效能預算**：禁止在已啟用 `backdrop-filter` 的主面板內層再無限嵌套多層即時模糊。
5. **強制相對路徑**：所有連結僅能使用相對路徑（`lessons/...`、`../../index.html`、`../...`），禁止 `/` 開頭根路徑。
6. **單檔 Self-Contained**：每個單元頁僅依賴 Google Fonts，其餘 CSS、SVG 雜訊與互動 JS 必須全數內嵌於單一 `index.html`。
7. **互動必須真實可用**：第四段光學實驗室與第五段測驗必須具備真實的 DOM 與 CSS 即時變化。
8. **收尾必更新白板與歷史**：完成工作後務必更新 `NOTES.md` 與 `log.md`，並確認 `AGENTS.md` 與 `CLAUDE.md` 保持同步。
