# 【TAICA 生成式 AI】第十週作業繳交報告：用 LLM Wiki 做一份教學 HTML 簡報

> **標題建議格式**（貼至線上表單標題欄時，請將方括號替換為您的學校簡稱、學號、系級簡稱與姓名）：  
> **`[學校簡稱] [學號] [系級簡稱] [姓名] Aero Glass 與介面光學設計 LLM Wiki 教學 HTML 簡報`**

---

## 一、LLM Wiki 主題與簡短介紹

本次作業以 **「Aero Glass 與介面光學設計知識庫（Aero Glass & Optical UI Wiki）」** 為主題，延續第 9 週 `AGENTS.md` 開發憲法，依第 10 週課程「**先討論、後生成**」原則先與 AI 進行 8 題需求訪談並定案於 `raw/00-interview-and-requirements.md`，接著實際建立完整的三層（四層細分）LLM Wiki 知識庫：

1. **原始文獻層（`raw/`，共 6 篇權威規格文獻＋1 份訪談定案）**：
   - `raw/01-w3c-css-backdrop-filter-spec.md`（W3C `backdrop-filter` 與彩度衰減 32%～45% 補償機制）
   - `raw/02-vista-dwm-aero-optical-spec.md`（Vista DWM 不對稱倒角、50% 鏡面切面與 `.vista-text` 光暈）
   - `raw/03-svg-turbulence-and-displacement-refraction.md`（`feTurbulence` 3.2% 微觀磨砂與 `feDisplacementMap` 折射置換）
   - `raw/04-apple-liquid-glass-and-dynamic-specular.md`（Apple Liquid Glass `--mx`/`--my` 動態游標光源追蹤）
   - `raw/05-chromium-gpu-compositing-and-fps-budget.md`（Chromium 合成管線、`16.67ms` 幀預算與外實內輕守則）
   - `raw/06-wcag-contrast-and-reduced-transparency.md`（WCAG 2.2 `4.5:1` 對比紅線與 `prefers-reduced-transparency` / `@supports` 降級）
2. **結構化知識與互動網頁層（`wiki/index.md` ＋ `notes/*.md` ＋ `lessons/*/index.html`，共 6 個單元）**：
   - 依 Content-First 規範完成 **Unit 01 ～ Unit 06**（涵蓋模糊彩度、Vista 倒角切面、GPU 壓測、SVG 置換色散、動態追光、無障礙退場）共 6 篇 Markdown 原稿與 6 個單檔即時互動光學實驗室。

---

## 二、LLM Wiki 與教學 HTML 簡報成果連結

- **🌐 LLM Wiki 首頁與全站預覽**：https://konayame774.github.io/genai-wiki-hub/
- **📚 LLM Wiki 知識總圖譜與 Ingest 對照索引**：https://github.com/KonAyame774/genai-wiki-hub/blob/main/wiki/index.md
- **🎓 教學 HTML 簡報（線上互動瀏覽）**：https://konayame774.github.io/genai-wiki-hub/slides/
  - 共 **12 頁**，專為不熟悉 CSS 光學與瀏覽器渲染的新手設計，透過生活化比喻（霧玻璃擦亮、45 度桌邊反光、小手電筒追光、畫師重繪風景比喻）、內嵌即時互動追光示範卡與視覺化流程圖教學。
  - **100% 出處可追溯**：每一頁底部皆設有來源資訊列（如 `Unit 01`～`Unit 06`），可直接點擊跳轉至對應互動實驗室與 `raw/` 原始文獻，並達成 6 個 Wiki 單元 100% 覆蓋。
- **📦 GitHub 完整原始碼儲存庫**：https://github.com/KonAyame774/genai-wiki-hub

---

## 三、Loop / Graph 工作流設計說明

為了避免用「一句話 Prompt」直接產出簡報時常見的三大失控問題（編造不存在的數據、遺漏特定單元、字數爆量撐破版面），本專案在 `.agents/workflows/topic-slides.md` 實作了 **「Graph（決定大流程與權限邊界）＋ 節點內 Loop（局部快速驗收修正）」** 原型，所有中間狀態皆以檔案落地於 `workflow/` 目錄：

### 1. 流程圖

```text
[節點 1：檢索 Wiki] ──► [關卡 A：覆蓋率檢查 (6/6)] ──(少於 3 篇)──► 🛑 停止並補 Ingest
         │ (通過：workflow/sources.md)
         ▼
[節點 2：平行抽取 6 張證據卡 workflow/cards/card-01..06.md]  ← 權限隔離：單卡只讀單一 Unit
         │
         ▼
[節點 3：生成 12 頁新手教學大綱] ──► [關卡 B：人類審核大綱結構 (workflow/outline.md)]
         │ (確認通過)
         ▼
[節點 4：撰寫逐頁稿 workflow/drafts/slides-draft.md] ◄──┐
         │                                               │ (忠實度/字數預檢未過，最多 2 輪 Loop)
         ▼                                               │
[關卡 C：逐頁稿字數與出處預檢] ──────────────────────────┘
         │ (通過)
         ▼
[節點 5：渲染單檔簡報 slides/index.html] ◄───────────────┐
         │                                               │ (局部退回對應頁修正，最多 3 輪 Loop)
         ▼                                               │
[關卡 D：python workflow/check_slides.py 自動化檢查] ────┘
         │ (Exit Code 0 全過)
         ▼
[節點 6：輸出 workflow/report.md 與 git push 部署]
```

### 2. 重複執行（Loop）、檢查關卡與設計理由

- **哪些步驟會重複執行？**
  1. **逐頁稿審查 Loop（節點 4 ↔ 關卡 C）**：逐頁對照證據卡核對數據與字數預算，最多 2 輪。
  2. **渲染與程式驗證 Loop（節點 5 ↔ 關卡 D）**：每次修改 `slides/index.html` 皆重跑 `python workflow/check_slides.py`，硬上限最多 **3 輪** 剎車；一旦某幾頁超出字數限制，**只退回修改出錯的那幾頁，其餘已完成頁面完全不動**。
- **哪些地方需要檢查或重新生成？**
  - **關卡 A（源頭數量檢查）**：確認 `raw/` 與 `notes/` 至少涵蓋 `3 ～ 6` 個有效單元才開工。
  - **關卡 B（人工大綱審核）**：確認投影片符合「痛點 → 光學基底 → 表面折射 → 動態追蹤 → 效能與無障礙 → 流程揭密」的新手學習坡度。
  - **關卡 D（可執行 Python 腳本 `workflow/check_slides.py`）**：強制用程式檢查 6 件事——總頁數 `8 ～ 15` 頁、每頁相對路徑出處連結真實存在、Unit 01～06 覆蓋率 `100%`、每頁可見純文字 `<= 420` 字且條列 `<= 6` 項、核心數據未寫反、以及內層卡片無違規嵌套 `backdrop-filter`。
- **為什麼這樣設計？**
  - 遵守課堂「**說『檢查一下』不算驗證，腳本說了算**」的工程準則，並利用 **節點權限隔離**（抽取證據卡時不可混看別的單元；排版渲染時不可順手修改技術數值）與 **檔案化中間產物**，讓錯在哪一關就能精準退回那一關，同時方便用 `git diff` 追蹤每一層變更。

---

## 四、一次實際執行的結果與檢查紀錄（真實 3 輪記錄）

我們在實際執行 `python workflow/check_slides.py` 時，確實經歷了一次「檢查工具自我修復 → 真實攔截版面溢出 → 局部精簡全數通過」的完整迴圈（詳見 `workflow/report.md`）：

1. **第 1 輪實測（Exit Code `1`）**：初次執行腳本時僅偵測到 `10` 頁。檢查發現 `HTMLParser` 未排除 Slide 03 與 Slide 11 中的 `<br>` 空標籤（Void Tag），造成標籤深度計數偏移。立即優先修正 `check_slides.py` 的 `VOID_TAGS` 處理，修復驗證關卡本身。
2. **第 2 輪實測（Exit Code `1`）**：正確解析全 `12` 頁後，腳本抓出 **4 頁投影片文字超過 `420` 字溢出上限**：
   - `Slide 04`：`423` 字（過多補充說明與程式碼註解）
   - `Slide 05`：`488` 字（三層 `box-shadow` 與敘述文字過長）
   - `Slide 07`：`486` 字（置換與色散說明超過舞台寬度容許量）
   - `Slide 12`：`431` 字（5 句總結口訣過長）
   - **局部退回処置**：維持已通過的其餘 8 頁與所有關鍵數據不變，只針對這 4 頁精簡贅字與註解。
3. **第 3 輪實測（Exit Code `0`）**：
   - 12 頁可見字數全數降至 `152 ～ 401` 字（`<= 420` 字安全線以下），條列皆 `0 ～ 5` 項（`<= 6` 項）。
   - Wiki 單元覆蓋率 **`6 / 6 (100%)`**。
   - 7 項核心基準數據（`blur(20px)`、`saturate(190%)`、`32%`、`0.032`、`50%`、`16.67ms`、`4.5:1`）全數命中且零矛盾。
   - 全站 `index.html`、`lessons/*/index.html` 與 `slides/index.html` **零斷鏈、零根路徑錯誤**，取得 **`ALL GATES PASSED (Exit Code 0)`**！

---

## 五、反思：錯誤來源分析與 Workflow 調整

1. **哪一個節點最常出錯？**
   - 第一容易出錯的是 **節點 4 / 5（逐頁稿與 HTML 渲染階段）**：當同時要在單一投影片放入「新手比喻＋核心原則＋CSS/SVG 程式碼範例」時，極容易因為加入多餘註解或冗長說明而讓字數默默突破 `420` 字上限，造成小螢幕垂直溢出。
   - 另一個常被忽略的盲點是 **檢查節點（關卡 D）本身實作錯誤**：第 1 輪若沒驗證解析器正確處理 `<br>` 空標籤，就會連錯頁數都不自知。
2. **發現問題後，把檢查往前移到了哪一個步驟？**
   - 將「單頁字數上限（`<= 420` 字）與程式碼精簡規範」從最後 HTML 渲染完才由 `check_slides.py` 抓錯，**往前移到節點 3（`outline.md` 大綱規劃）與節點 4（`drafts/slides-draft.md` 逐頁稿）**，在寫 HTML 標籤與 CSS 排版前就先行控管文字密度與 `<pre>` 行數；並於流程最前端（關卡 A）強制先核對 `raw/00` 訪談條件與 6 篇來源覆蓋率。
3. **有沒有因此修改 workflow / graph？為什麼？**
   - **有，實際修改了兩處**：
     1. **升級 `.agents/workflows/topic-slides.md` 退回規格**：明確規定「僅對超出字數門檻之單頁局部精簡（Local Rollback）」，避免 AI 一看到錯誤就把整份 `slides/index.html` 重新生成而破壞原本通過檢查的頁面或覆寫掉既有數據。
     2. **擴大 `workflow/check_slides.py` 驗證邊界**：除了修正 `VOID_TAGS` 解析外，也將全站 `index.html` 與 6 個 `lessons/*/index.html` 的相對路徑斷鏈掃描一併寫入檢查腳本，讓單一指令就能守住整座 LLM Wiki 與簡報的一致性。
