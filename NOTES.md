# NOTES.md — 專案現況白板

> 本文件為「現況白板」，記錄目前已完成單元、原始文獻 Ingest 進度與第 10 週教學簡報工作流狀態。
> 每次新增或修改單元後，請務必更新本檔案（已完成項目請移出待辦區）。

---

## 一、目前狀態摘要

- **最後更新日期**：2026-11-17
- **專案主題與版本**：v3.0 — **「Aero Glass × Apple Liquid Glass LLM Wiki ＋ 第 10 週 Graph/Loop 教學 HTML 簡報平台」**
- **原始文獻 Ingest 數量**：6 篇權威原始文獻（`raw/01`～`raw/06` ＋ `raw/00` 先討論後生成需求訪談紀錄）
- **目前線上單元數**：6 個完整知識單元（`notes/*.md` 原稿 ＋ `lessons/*/index.html` 五段式互動實驗室）＋ 1 份 12 頁教學型 HTML 簡報（`slides/index.html`）
- **部署網址**：https://konayame774.github.io/genai-wiki-hub/ （簡報：https://konayame774.github.io/genai-wiki-hub/slides/ ）

---

## 二、已完成單元清單（100% 對應 `raw/` 來源）

| 單元編號 | Slug | 單元標題 | 分類 | 原始文獻 | 網頁與互動實驗室 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Unit 01 | `blur-and-saturation` | 背景模糊、鮮豔度補償與玻璃微觀雜訊 | 光學基底 | `raw/01`, `raw/03` | ✅ 毛玻璃調校實驗台 + 3 題測驗 |
| Unit 02 | `bevel-and-refraction` | 物理厚度、倒角光線與 Vista 鏡面切面 | 表面折射 | `raw/02` | ✅ Vista 光學元件組裝器 + 3 題測驗 |
| Unit 03 | `gpu-compositing-and-agents` | GPU 合成圖層效能瓶頸與 AGENTS.md 規範 | 效能與規範 | `raw/05` | ✅ 真實 GPU 與即時 FPS 壓測 + 3 題測驗 |
| Unit 04 | `svg-refraction-displacement` | SVG 置換濾鏡與邊緣色散折射 | 表面折射 | `raw/03` | ✅ `feDisplacementMap` 置換與色散台 + 3 題測驗 |
| Unit 05 | `dynamic-light-tracking` | 動態光源追蹤與滑鼠高光跟隨 | 光學基底 | `raw/04` | ✅ `--mx`/`--my` 與 Border-Mask 追光台 + 3 題測驗 |
| Unit 06 | `accessibility-fallback` | WCAG 對比度驗證與無障礙降級策略 | 效能與規範 | `raw/06` | ✅ 即時相對亮度對比度計算與降級模擬器 + 3 題測驗 |

---

## 三、第 10 週 Graph + Loop 教學簡報狀態

- **教學 HTML 簡報**：`slides/index.html`（共 **12 頁**，每頁底部標註對應 Unit 與連結）
- **Workflow 原型與證據卡**：`.agents/workflows/topic-slides.md`、`workflow/sources.md`、`workflow/cards/card-01..06.md`、`workflow/outline.md`、`workflow/drafts/slides-draft.md`
- **自動檢查腳本**：`workflow/check_slides.py`（已驗證 Exit Code `0` 全過，紀錄於 `workflow/report.md`）
- **作業繳交報告**：`WEEK10_SUBMISSION.md`

---

## 四、後續擴充建議（Backlog）

- **Unit 07（規劃中）**：Wide-Gamut P3 光學色彩空間與 HDR 亮面漸層（`wide-gamut-p3-glass`）。
