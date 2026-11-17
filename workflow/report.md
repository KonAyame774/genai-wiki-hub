# [節點 6 產出] Graph + Loop 實際執行與檢查紀錄報告

- **執行日期**：2026-11-17
- **工作流規格**：[`.agents/workflows/topic-slides.md`](../.agents/workflows/topic-slides.md)
- **目標成品**：[`slides/index.html`](../slides/index.html)（12 頁教學型 HTML 簡報）
- **自動化檢查腳本**：[`workflow/check_slides.py`](./check_slides.py)

---

## 一、三輪真實執行與局部退回軌跡（Execution Trace）

### 第 1 輪：初版 `check_slides.py` 檢查（Exit Code `1`）
- **檢查動作**：完成 12 頁 `slides/index.html` 初版渲染與 `raw/`/`notes/`/`lessons/` 建置後，首次執行 `python workflow/check_slides.py`。
- **實測發現**：腳本輸出僅偵測到 `10 頁`，且誤將相鄰投影片合併計算。追蹤原因為 `HTMLParser` 未將 HTML 空標籤（Void Tags，如 Slide 03 與 Slide 11 中的 `<br>`）排除於容器深度計數外，導致標籤深度失準。
- **處置行動（先修驗證工具關卡）**：於 `workflow/check_slides.py` 補上 `VOID_TAGS` 判斷與 `handle_startendtag` 處理，確保關卡 D 能精確切分 12 頁投影片。

### 第 2 輪：全頁精確檢核 — 捕捉版面字數溢出（Exit Code `1`）
- **檢查動作**：重新執行 `python workflow/check_slides.py`。
- **實測通過項目**：
  - 偵測頁數：`12 頁`（符合 `8 ～ 15` 頁規格）
  - Wiki 覆蓋率：`6 / 6 個單元 (100%)`（Unit 01 ～ Unit 06 全部連結存在）
  - 核心數據忠實度：`blur(20px)`、`saturate(190%)`、`32%`、`0.032`、`50%`、`16.67ms`、`4.5:1` 全數命中且無反話
  - GPU 預算與全站斷鏈檢查：全數通過
- **真實攔截到 4 項問題**：
  1. `Slide 04` 可見字數 `423` 字（超過 `420` 字上限）
  2. `Slide 05` 可見字數 `488` 字（超過 `420` 字上限）
  3. `Slide 07` 可見字數 `486` 字（超過 `420` 字上限）
  4. `Slide 12` 可見字數 `431` 字（超過 `420` 字上限）
- **局部退回行動（Local Rollback）**：依 `.agents/workflows/topic-slides.md` 退回規則，**不重新抽取任何證據卡，也不更動已過關的其餘 8 頁**，僅對 `S04`、`S05`、`S07`、`S12` 精簡贅字與程式碼過長註解，同時保留全部原始光學數據。

### 第 3 輪：全關卡通過（Exit Code `0`）
- **檢查動作**：針對第 4、5、7、12 頁局部微調後重跑 `python workflow/check_slides.py`。
- **終端機實測輸出摘要**：

```text
目標檔案：slides\index.html
偵測頁數：12 頁 (規範要求：8 ～ 15 頁)

頁碼     可見字數       條列數      出處連結     Wiki 來源單元
--------------------------------------------------------------------
S01    253        0        3        Wiki Index & Raw Requirements
S02    200        4        3        Unit 01 / Unit 02 / Unit 03
S03    243        3        2        Unit 01 (blur-and-saturation)
S04    296        3        2        Unit 01 (blur-and-saturation)
S05    372        3        2        Unit 02 (bevel-and-refraction)
S06    293        4        2        Unit 02 (bevel-and-refraction)
S07    377        3        2        Unit 04 (svg-refraction-displacement)
S08    222        3        2        Unit 05 (dynamic-light-tracking)
S09    335        4        2        Unit 03 (gpu-compositing-and-agents)
S10    401        2        2        Unit 06 (accessibility-fallback)
S11    158        2        3        Workflow Graph + Loop
S12    367        5        8        All Units Summary (Unit 01–06)
--------------------------------------------------------------------
[1] 知識庫覆蓋率檢查：6 / 6 個單元 (100%) -> ✅ PASS
[2] 來源忠實度與核心數據比對：7 / 7 基準數據命中、0 矛盾 -> ✅ PASS
[3] AGENTS.md 光學與 GPU 預算合規檢查：pointer-events: none、無嵌套模糊 -> ✅ PASS
[4] 全站相對路徑與斷鏈掃描：index.html、lessons/*、slides/index.html -> ✅ PASS
🎉 ALL GATES PASSED — 12 頁教學簡報與全站知識庫檢查全數通過！(Exit Code 0)
```

---

## 二、狀態產出清單總核對

- [x] `raw/00-interview-and-requirements.md`（先討論後生成 8 題訪談紀錄）
- [x] `raw/01` ～ `raw/06`（6 篇原始權威文獻）
- [x] `wiki/index.md`（雙向索引與單一事實基準表）
- [x] `notes/*.md`（Unit 01 ～ Unit 06 完整知識原稿）
- [x] `lessons/*/index.html`（Unit 01 ～ Unit 06 獨立單檔互動實驗室）
- [x] `workflow/sources.md`、`workflow/cards/card-01..06.md`、`workflow/outline.md`、`workflow/drafts/slides-draft.md`
- [x] `slides/index.html`（12 頁互動式教學簡報）
- [x] `workflow/check_slides.py`（已執行驗證 Exit Code 0）
