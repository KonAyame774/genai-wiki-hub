# [Unit 06] WCAG 對比度驗證與無障礙降級策略

---

## Meta 資訊（Frontmatter 規格）

- **單元編號**：Unit 06
- **單元標題**：WCAG 對比度驗證與無障礙降級策略
- **副標題**：兼顧極致通透與全民可讀性——實測 WCAG 2.2 相對亮度對比，並用 `prefers-reduced-transparency` 與 `@supports` 打造安全退場防線
- **Slug**：`accessibility-fallback`
- **分類**：`效能與規範`
- **預計閱讀時間**：`11 分鐘`
- **關鍵字標籤**：`WCAG 4.5:1`, `prefers-reduced-transparency`, `@supports`
- **成品路徑**：`lessons/accessibility-fallback/index.html`
- **Ingest 原始文獻來源**：[`raw/06-wcag-contrast-and-reduced-transparency.md`](../raw/06-wcag-contrast-and-reduced-transparency.md)
- **前後單元導覽**：
  - 上一單元：`../dynamic-light-tracking/index.html`（Unit 05 動態光源追蹤與滑鼠高光跟隨）
  - 下一單元：`../../slides/index.html`（前往第 10 週教學 HTML 簡報）
- **狀態**：`✅ 已定稿`

---

## 一、一句話核心觀念（TL;DR）

> 真正成熟的 UI 光學系統不能只在頂配螢幕上好看：透過計算與守護 **WCAG 2.2 `4.5:1`（AA 級）文字對比度**，並實作 `@media (prefers-reduced-transparency: reduce)` 與 `@supports not (backdrop-filter: blur(1px))` 雙重無障礙退場防線，才能確保弱視族群、開啟系統「減少透明度」的使用者與舊環境都能清楚無礙地閱讀內容。

---

## 二、核心觀念拆解

### 卡片 1：半透明介面的 WCAG 2.2 對比度紅線
- **痛點描述**：當毛玻璃底色透明度過高（例如白霧僅 `rgba(255,255,255,0.12)`）卻疊在深藍或高反差極光背景上，黑字 `#1c1c1e` 在深背景區段的實際對比度往往只剩 `2.1:1`，遠低於無障礙法定門檻。
- **WCAG 2.2 核心數字**：
  - **一般內文（`< 18pt`）AA 級底線**：**`4.5 : 1`**
  - **大標題（`>= 18pt` 或粗體 `>= 14pt`）AA 級**：**`3.0 : 1`**
  - **加強型 AAA 級高齡／醫療標準**：**`7.0 : 1`**
- **解法**：遵循 `AGENTS.md` 「外實內輕」原則，將閱讀文字區域的內層卡片墊高至 `rgba(255, 255, 255, 0.58 ～ 0.75)`，並為關鍵標題輔以 `.vista-text` 白色光暈防禦。

### 卡片 2：回應系統「減少透明度」設定（`prefers-reduced-transparency`）
- **CSS Media Queries Level 5 標準寫法**：
  ```css
  @media (prefers-reduced-transparency: reduce) {
    .glass-panel {
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      background: rgba(248, 250, 252, 0.94);
      border-color: rgba(15, 23, 42, 0.22);
    }
    .glass-panel::before {
      opacity: 0.18;
    }
  }
  ```
- **為什麼這樣設值**：對視覺疲勞或暈眩敏感的使用者會在 macOS / iOS / Windows 系統開啟「減少透明度」。當媒體查詢生效時，主動撤銷模糊並切換為高對比微霧白底（`0.94`），立即提供 `> 10:1` 的極清晰對比。

### 卡片 3：舊瀏覽器或低功耗環境的 `@supports` 漸進增強
- **雙重保險原則（Progressive Enhancement）**：不能只靠預設 `rgba(255,255,255,0.22)` 賭每台裝置都能跑出 `backdrop-filter: blur(20px)`。
- **正確防禦寫法**：
  ```css
  @supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
    .glass-panel {
      background: rgba(248, 250, 252, 0.90);
    }
  }
  ```
  萬一瀏覽器不支援背景濾鏡或使用者關閉硬體加速，面板不會淪為一塊「後面文字雜線全部透進來的髒玻璃」，而是優雅退場成高可讀性的實心磨砂卡。

### ⚠️ 常見誤區與效能地雷（Pitfall Alert）
- **誤區名稱**：認為「只要加上 `.vista-text` 的白色 `text-shadow`，玻璃底色就算設成全透明 `alpha: 0.05` 也能通過 WCAG 無障礙認證。」
- **為什麼容易出錯**：自動化無障礙檢測工具與純計算公式僅衡量前景字色與背景混合後底色的相對亮度比；當半透明背後撞上純黑背景而白底僅 `0.05` 時，算出的對比度仍會亮起不及格紅燈。
- **正確做法**：文字主要閱讀卡務必先靠 `rgba(255, 255, 255, 0.62 ～ 0.78)` 實底遮罩本身就站穩 `>= 4.5:1`，再疊加 `.vista-text` 錦上添花。

---

## 三、互動實驗室規格（Interactive Lab Spec）

- **實驗室名稱**：WCAG 2.2 對比度檢測與無障礙降級模擬器
- **教學目的**：即時將網頁背景亮度（亮青天色 / 中間深藍 / 夜間深海極光）、卡片底色不透明度與無障礙環境模式（標準 Aero / 系統減少透明度 / 模擬無模糊）組合運算，用真實 WCAG 公式顯示當前比值及 AA / AAA 狀態燈。
- **控制元件（Inputs）**：
  - 環境模擬模式按鈕：`標準 Aero Glass` / `系統開啟 prefers-reduced-transparency` / `模擬無 backdrop-filter`
  - 文字區域背景遮罩濃度滑桿：`0.10 ～ 0.96`
  - 底層極光區段亮度切換：`淺青天色 #7dd3fc` / `極光深藍 #0369a1` / `深海夜空 #0b192c`
  - `.vista-text` 光暈保護開關
- **視覺化輸出（Outputs）**：
  - 即時渲染對照視窗 ＋ 動態計算出的 **真實對比度比值（如 `6.18 : 1`）與 AA / AAA 通關燈號** ＋ 完整 `@media` / `@supports` 防護 CSS 輸出。

---

## 四、隨堂自我檢測（3 題單選題）

### Q1：依據 W3C WCAG 2.2 規範，毛玻璃卡片內的「一般大小內文」至少需達到多少對比度才符合 AA 基本無障礙標準？
- A. `1.5 : 1`
- B. `4.5 : 1`
- C. `12.0 : 1`
- D. 只要是半透明就沒有對比度限制
- **正解**：`B`
- **詳解**：WCAG 2.2 Level AA 規定一般文字須達 `4.5:1`（大標題為 `3.0:1`），若要達最高級 Level AAA 則需 `7.0:1`。

### Q2：當使用者在 Windows 或 macOS 系統開啟「減少透明度（Reduce Transparency）」輔助功能時，CSS 應透過哪一個標準媒體查詢接手退場？
- A. `@media (prefers-reduced-transparency: reduce)`
- B. `@media (prefers-glass-opacity: zero)`
- C. `@media (min-blur: 100px)`
- D. `@import url("solid.css")`
- **正解**：`A`
- **詳解**：`@media (prefers-reduced-transparency: reduce)` 是 CSS Media Queries Level 5 專門偵測系統「減少透明度」偏好的標準查詢語法。

### Q3：為何不能只靠極低不透明度的 `rgba(255,255,255,0.12)` 搭配 `.vista-text`，就跳過 `@supports not` 退場設定？
- A. 若舊環境或不支援硬體加速的瀏覽器無法渲染 `backdrop-filter`，只剩 12% 白透視的玻璃會讓雜亂背景直接穿透並破壞可讀性
- B. 因為 `@supports` 會自動替網站加上高光切面
- C. 因為 `rgba()` 不支援小數
- D. 否則所有圖片都會變成白色
- **正解**：`A`
- **詳解**：當濾鏡失效時必須依賴 `0.90` 左右的高不透明度實底撐住對比與遮罩力。
