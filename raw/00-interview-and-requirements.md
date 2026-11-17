# LLM Wiki 建立紀錄：先討論、後生成（需求訪談與規格定案）

> 本文件依據 **【TAICA 生成式 AI 第十週：把你的工作拆成 AI 能做的流程】** 實作一規範（投影片 Slide 31–33），記錄建立「Aero Glass 與介面光學設計知識庫（Aero Glass & Optical UI Wiki）」前的需求訪談問答與規格定案，確認完畢後才進行 `raw/` 擴充、`notes/` Ingest 與 `AGENTS.md` / `CLAUDE.md` 更新。

---

## 一、8 大核心問題訪談與使用者定案結果

| 編號 | 訪談問題（Slide 32 檢核項） | 定案決策 |
| :--- | :--- | :--- |
| **Q1** | **知識庫主題與專案定位？** | 沿用並擴充第 9 週已部署之 `genai-wiki-hub`（Aero Glass 與介面光學設計知識庫），將原有 3 個單元擴充為完整 6 單元，並在現有 GitHub Pages 上新增「教學 HTML 簡報」與「Graph/Loop 工作流原型」。 |
| **Q2** | **這個 Wiki 主要是給誰看的？** | 給前端工程師、UI/UX 設計師與生成式 AI 課程同學看，同時要作為「教學 HTML 簡報」的單一事實來源（Single Source of Truth），讓原本不熟悉 CSS 光學特效的新手也能看懂原理。 |
| **Q3** | **需要哪些頁面類型？** | 採四層檔案結構：`raw/*.md`（原始權威文獻，至少 5 篇，本次收錄 6 篇）→ `wiki/index.md`（知識庫總索引）→ `notes/*.md`（單元原稿，Content-First）→ `lessons/*/index.html`（五段式互動實驗室網頁）與 `slides/index.html`（12 頁教學簡報）。 |
| **Q4** | **使用什麼語言與標點規範？** | 全站採用臺灣繁體中文慣用術語與全形標點符號（，。、：「」！？（）），專有名詞與 CSS 屬性保留英文原文（如 `backdrop-filter`、`feDisplacementMap`、`WCAG 2.2`）。 |
| **Q5** | **簡報與知識庫的出處要標到多細？** | 簡報每一頁必須透過 HTML `data-wiki-unit` 屬性與頁面底部來源列，精準標註對應的 Wiki 單元編號（`Unit 01`～`Unit 06`）、Markdown 原稿路徑（`notes/<slug>.md`）、原始文獻（`raw/<doc>.md`）及可直接點開實作實驗室的相對路徑（`../lessons/<slug>/index.html`）。 |
| **Q6** | **遇到文獻數據矛盾或名詞差異時怎麼辦？** | 優先採用 W3C 官方標準規格數據為基準；各風格參數差異（例如 Vista Aero 的 50% 鏡面切面 vs Apple Liquid Glass 的 `saturate(190%)` 與動態光源追蹤）則並陳比較，禁止 AI 用自身記憶猜測數字或混寫參數。 |
| **Q7** | **資料是一次一篇還是批次 Ingest？** | 支援逐篇與批次標準 Ingest 流程：每篇 `raw/*.md` 皆需先抽取至 `notes/<slug>.md`（或更新既有原稿出處）並登記於 `wiki/index.md` 與 `NOTES.md`，確認無誤後才生成對應互動網頁 `lessons/<slug>/index.html`。 |
| **Q8** | **之後要產出什麼成品？Lint 要檢查什麼？** | 產出一份 **10～12 頁的教學型 HTML 簡報（`slides/index.html`）**，採 Graph + 節點內 Loop 工作流，並由 `workflow/check_slides.py` 程式檢查：頁數（8～15 頁）、每頁出處與連結存在性、6 單元覆蓋率 100%、字數與條列不溢出頁面、關鍵數據忠實度、以及 GPU 合成圖層預算合規性。 |

---

## 二、確認後之 Wiki 擴充藍圖（6 篇原始文獻 ↔ 6 個知識單元）

1. `raw/01-w3c-css-backdrop-filter-spec.md` → **Unit 01**：`blur-and-saturation`（背景模糊、鮮豔度補償與玻璃微觀雜訊）
2. `raw/02-vista-dwm-aero-optical-spec.md` → **Unit 02**：`bevel-and-refraction`（物理厚度、倒角光線與 Vista 鏡面切面）
3. `raw/03-svg-turbulence-and-displacement-refraction.md` → **Unit 01 / Unit 04**：`svg-refraction-displacement`（SVG 置換濾鏡與邊緣色散折射）
4. `raw/04-apple-liquid-glass-and-dynamic-specular.md` → **Unit 05**：`dynamic-light-tracking`（動態光源追蹤與滑鼠高光跟隨）
5. `raw/05-chromium-gpu-compositing-and-fps-budget.md` → **Unit 03**：`gpu-compositing-and-agents`（GPU 合成圖層效能瓶頸與 `AGENTS.md` 規範）
6. `raw/06-wcag-contrast-and-reduced-transparency.md` → **Unit 06**：`accessibility-fallback`（WCAG 對比度驗證與無障礙降級策略）
