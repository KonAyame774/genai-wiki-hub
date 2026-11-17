# NOTES.md — 專案現況白板

> 本文件為「現況白板」，記錄目前已完成單元、待擴充光學主題 Backlog 與下次接手提醒。
> 每次新增或修改單元後，請務必更新本檔案（已完成項目請移出待辦區）。

---

## 一、目前狀態摘要

- **最後更新日期**：2026-11-17
- **專案主題與版本**：v2.0 — 全面轉型為 **「Aero Glass 與介面光學設計知識庫（Aero Glass & Optical UI Wiki）」**
- **目前線上單元數**：3 個（全站均已實作 `.glass-panel` 毛玻璃與彩度補償、光學倒角、`::before` 50% 鏡面切面、`.vista-text` 文字光暈與 SVG 微觀雜訊）
- **部署網址**：https://konayame774.github.io/genai-wiki-hub/

---

## 二、已完成單元清單

| 單元編號 | Slug | 單元標題 | 分類 | 原稿狀態 | 網頁與互動實驗室 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Unit 01 | `blur-and-saturation` | 背景模糊、鮮豔度補償與玻璃微觀雜訊 | 光學基底 | ✅ 已定稿 | ✅ 毛玻璃光學調校實驗台（`blur`、`saturate`、SVG 雜訊即時調參）+ 3 題測驗 |
| Unit 02 | `bevel-and-refraction` | 物理厚度、倒角光線與 Vista 鏡面切面 | 表面折射 | ✅ 已定稿 | ✅ Vista Aero 光學元件組裝器（倒角、`inset` 陰影、50% 切面、文字光暈）+ 3 題測驗 |
| Unit 03 | `gpu-compositing-and-agents` | GPU 合成圖層效能瓶頸與 AGENTS.md 規範 | 效能與規範 | ✅ 已定稿 | ✅ GPU 圖層效能與 FPS 壓力模擬器 + AGENTS.md 合規診斷 + 3 題測驗 |

---

## 三、待擴充單元 Backlog（下次從這裡開始）

1. **Unit 04｜SVG 置換濾鏡與邊緣色散折射**（推薦優先擴充）
   - 建議 Slug：`svg-refraction-displacement`
   - 建議分類：`表面折射`
   - 預計互動實驗室：利用 `feDisplacementMap` 模擬玻璃邊緣折射彎曲與輕微色散光環。
2. **Unit 05｜動態光源追蹤與滑鼠高光跟隨（Specular Pointer Tracking）**
   - 建議 Slug：`dynamic-light-tracking`
   - 建議分類：`光學基底`
   - 預計互動實驗室：透過 CSS 自訂屬性 `--mx` / `--my` 驅動卡片倒角反光隨游標移動。
3. **Unit 06｜無障礙降級策略：`prefers-reduced-transparency` 與舊瀏覽器退場**
   - 建議 Slug：`accessibility-fallback`
   - 建議分類：`效能與規範`
   - 預計互動實驗室：即時切換高對比／減少透明度系統設定，檢視文字對比度（WCAG AA/AAA）。

---

## 四、接手協作提醒

- 新增單元前，請先讀 [AGENTS.md](./AGENTS.md) 確認五大 CSS 光學技巧與 GPU 合成效能預算（避免在主面板內層無限嵌套 `backdrop-filter`）。
- 首頁 `index.html` 末尾的 `.card-soon` 目前指向 **Unit 04（`svg-refraction-displacement`）**。
