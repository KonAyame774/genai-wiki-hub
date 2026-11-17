# Aero Glass & Optical UI Wiki — Aero Glass 與介面光學設計知識庫

- **🌐 線上網頁預覽（GitHub Pages）**：https://konayame774.github.io/genai-wiki-hub/
- **📦 GitHub Repository**：https://github.com/KonAyame774/genai-wiki-hub

這是一座結合 **「Vista Aero 鏡面反光與文字光暈」** 及 **「Apple Liquid Glass 背景彩度補償毛玻璃」** 的介面光學設計知識庫，同時作為 **【TAICA 生成式 AI：文字與圖像生成的原理與實務】第九週作業（建立 `AGENTS.md` / `CLAUDE.md`）** 之完整實作成果。

透過根目錄的 [`AGENTS.md`](./AGENTS.md)（與同步的 [`CLAUDE.md`](./CLAUDE.md)），本專案將容易寫歪的視覺光學細節寫成「AI 看得懂、改得準」的標準規範，實現真正的 **Agentic Work 可持續擴充**。

---

## ✨ 知識庫涵蓋的五大核心 CSS 光學技巧

1. **背景模糊與鮮豔度補償**：`backdrop-filter: blur(20px) saturate(190%)`，解決單純 `blur()` 讓背景發灰的問題。
2. **物理厚度與倒角光線**：透過上／左亮邊框搭配 `box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.8)` 做出精準的 1 像素高光切角。
3. **表面折射與高光切面**：使用 `.glass-panel::before` 在高度 `50%` 處製造非連續階躍，重現 Vista Aero 經典的鏡面反射光斑分界線。
4. **Vista 風格的文字光暈**：`.vista-text` 使用雙層白色 `text-shadow` 在文字周圍建立發光防護層，確保半透明面板上的極佳可讀性。
5. **玻璃微觀雜訊與效能控管**：嵌入 `2%～4%` 不透明度的 SVG Noise Data URI 消除色階斷裂，同時訂定 GPU 合成圖層預算避免行動裝置掉幀。

---

## 📁 目錄架構

```text
genai-wiki-hub/
├── index.html                          # 光學知識庫首頁（分類篩選、搜尋、.glass-panel 範例與工作流說明）
├── AGENTS.md                           # AI 協作規範與光學設計系統憲法
├── CLAUDE.md                           # 與 AGENTS.md 完全同步之規範檔
├── README.md                           # 專案說明文件
├── NOTES.md                            # 現況白板（已完成單元與待擴充 Backlog）
├── log.md                              # 決策與變更歷史（只增不刪）
├── .nojekyll                           # 停用 Jekyll
├── .gitignore
├── notes/                              # 【內容先行層 / 光學設計原稿】
│   ├── _template.md                    # 新增單元標準 Markdown 範本
│   ├── blur-and-saturation.md          # Unit 01 原稿
│   ├── bevel-and-refraction.md         # Unit 02 原稿
│   └── gpu-compositing-and-agents.md   # Unit 03 原稿
└── lessons/                            # 【互動網頁成品層】
    ├── blur-and-saturation/index.html
    ├── bevel-and-refraction/index.html
    └── gpu-compositing-and-agents/index.html
```

---

## 🚀 如何用 AI 繼續擴充新光學單元？

只需請 AI 代理依序讀取 `AGENTS.md`、`NOTES.md` 與 `log.md`，並下達以下指令：

> 「請先閱讀專案根目錄的 `AGENTS.md`、`NOTES.md` 與 `log.md`。我想新增 Unit 04，主題為『SVG 置換濾鏡與邊緣色散折射』（slug：`svg-refraction-displacement`，分類：`表面折射`）。請嚴格依照 `AGENTS.md` 的 4 步標準工作流完成原稿、互動講義網頁、首頁卡片串接與狀態更新。」
