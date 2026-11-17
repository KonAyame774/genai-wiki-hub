---
description: 從 Aero Glass LLM Wiki 執行 Graph + 節點內 Loop 工作流，產出經過覆蓋率、出處與忠實度檢查的新手教學 HTML 簡報（slides/index.html）。
---

# `/topic-slides` — LLM Wiki → 教學 HTML 簡報 Graph + Loop 工作流原型

本工作流依據 **蔡炎龍老師第 10 週課程（Slide 43–47）** 設計，將簡報生成拆解為「節點權限隔離、每關狀態落地存檔、局部退回不整份重來」的 Graph 管線，並在關鍵節點內嵌 Loop 自我修正迴圈。

---

## 一、Graph 流程總圖

```text
[節點 1：檢索 Wiki] ──► [關卡 A：覆蓋率檢查 (6/6)] ──(不足 < 3 篇)──► 🛑 停止，補 Ingest raw/
         │ (通過)
         ▼
[節點 2：平行抽取 6 張證據卡] ──► (單卡獨立：僅讀單一 Unit + raw/)
         │
         ▼
[節點 3：生成教學大綱 outline.md] ──► [關卡 B：人類審核教學結構] ──(缺頁/太難)──► 退回節點 3 或 1
         │ (確認通過)
         ▼
[節點 4：撰寫逐頁稿 drafts/slides-draft.md] ◄──────┐
         │                                         │
         ▼                                         │ (忠實度/字數預檢未過，最多 2 輪)
[關卡 C：逐頁稿忠實度與字數檢查] ───────────────────┘
         │ (通過)
         ▼
[節點 5：渲染單檔簡報 slides/index.html] ◄────────┐
         │                                         │
         ▼                                         │ (程式腳本失敗，退回修對應頁或草稿)
[關卡 D：python workflow/check_slides.py 驗證] ────┘
         │ (Exit Code 0 全數通過)
         ▼
[節點 6：輸出 workflow/report.md 與交件]
```

---

## 二、節點隔離與權限邊界表（對應 Slide 44–45）

| 節點 / 關卡 | 輸入檔案 | 輸出檔案 | 只能看什麼（Read Scope） | 不能做什麼（Guardrail） |
| :--- | :--- | :--- | :--- | :--- |
| **節點 1：檢索 Wiki** | `wiki/index.md`、`raw/*.md`、`notes/*.md` | `workflow/sources.md` | 專案內的 `raw/` 與 `notes/` | 不可憑模型自身記憶補充未 Ingest 的來源 |
| **節點 2：證據卡抽取** | 單一 `notes/<slug>.md` ＋ 對應 `raw/*.md` | `workflow/cards/card-01..06.md` | 每次僅讀對應的單一單元 | **嚴禁混入其他單元來源**（避免張冠李戴） |
| **節點 3：大綱規劃** | `workflow/sources.md`、`workflow/cards/*.md` | `workflow/outline.md` | 證據卡摘要與新手學習目標 | 需停下確認結構由淺入深後再寫逐頁稿 |
| **節點 4：逐頁稿 + Loop** | `workflow/outline.md` ＋ 對應單張 `card-XX.md` | `workflow/drafts/slides-draft.md` | 該頁指定的證據卡 | 不可引用證據卡以外未經核實的數字；單頁上限 `420` 字 |
| **節點 5：HTML 渲染** | 已通過的 `workflow/drafts/slides-draft.md` | `slides/index.html` | 已審過的逐頁稿 | **改排版時禁止順手亂改技術數據與結論** |
| **節點 6：程式驗證** | `slides/index.html`、`notes/`、`raw/` | `workflow/report.md` ＋ 終端機輸出 | 只讀 DOM 結構、連結路徑與字數 | **禁止由人類或生成者口頭喊「檢查完了」，必須腳本過關** |

---

## 三、自動退回與停止條件

1. **大圈退回（從源頭重來）**：僅當某單元缺少 `raw/` 來源或整份簡報大綱教學順序錯誤時，才退回節點 1 或節點 3。
2. **小圈局部快修**：
   - 第 $k$ 頁字數溢出或缺少出處連結 → **只修改第 $k$ 頁，其他頁數不動**。
   - 單一數據寫反或沒根據 → **退回重核對應 `card-XX.md`**。
3. **Hard Cap 剎車條件**：任一檢查迴圈最多重跑 **3 輪**；若 `sources.md` 可用來源少於 3 篇，必須立即停止執行並請求補充資料。
