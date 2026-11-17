# NOTES.md — 專案現況白板

> 本文件為「現況白板」，記錄目前已完成進度、待擴充單元清單（Backlog）與下次接手要點。
> 每次完成新單元或修改現有頁面後，請務必更新本檔案（已完成的項目請移出待辦區）。

---

## 一、目前狀態摘要

- **最後更新日期**：2026-11-17
- **專案階段**：基礎架構與首批三個核心單元已全面上線（MVP 完成）
- **目前線上單元數**：3 個（皆已完成 `notes/<slug>.md` 原稿、`lessons/<slug>/index.html` 互動網頁與首頁卡片串接）
- **部署備妥狀態**：已包含 `.nojekyll` 與全站相對路徑，可直接推上 GitHub 並開啟 GitHub Pages。

---

## 二、已完成單元清單

| 單元編號 | Slug | 單元標題 | 分類 | 原稿狀態 | 網頁與互動實驗室 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Unit 01 | `rag-architecture` | RAG 檢索增強生成原理與實務 | 檢索增強 | ✅ 已定稿 | ✅ RAG 檢索與 Chunk Size 模擬器 + 3 題測驗 |
| Unit 02 | `reflection-agent` | Reflection 反思型 Agent 架構與設計 | Agent 架構 | ✅ 已定稿 | ✅ 三階段演化模擬器（Drafter → Critic → Refiner）+ 3 題測驗 |
| Unit 03 | `agentic-workflow` | 換你當老闆！AGENTS.md 與 AI 協作工作流 | AI 工作流 | ✅ 已定稿 | ✅ Vibe Coding vs. Agentic Work 規則診斷室 + 3 題測驗 |

---

## 三、待擴充單元 Backlog（下次從這裡開始）

1. **Unit 04｜Prompt 工程與結構化輸出**（推薦優先擴充）
   - 建議 Slug：`prompt-engineering`
   - 建議分類：`AI 工作流`
   - 預計互動實驗室：Few-shot 範例與 JSON Schema 結構化輸出比對模擬器（對比有／無約束的 LLM 輸出穩定度）。
2. **Unit 05｜Multi-Agent 協作與任務分工**
   - 建議 Slug：`multi-agent-crew`
   - 建議分類：`Agent 架構`
   - 預計互動實驗室：Coordinator 與 Subagent 任務派工與訊息流視覺化追蹤器。
3. **Unit 06｜Function Calling 與 MCP 協定入門**
   - 建議 Slug：`function-calling-mcp`
   - 建議分類：`Agent 架構`
   - 預計互動實驗室：Tool Schema 參數檢驗與模擬工具呼叫迴圈沙盒。

---

## 四、接手協作提醒

- 新增單元前，請務必先讀取 [AGENTS.md](./AGENTS.md) 第五節的「4 步標準工作流」。
- 首頁 `index.html` 末尾的虛線待擴充卡片（`.card-soon`）目前指向 **Unit 04（`prompt-engineering`）**；當 Unit 04 完成時，記得將該卡片的預設指令更新為 Unit 05。
