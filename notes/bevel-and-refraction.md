# [Unit 02] 物理厚度、倒角光線與 Vista 鏡面切面

---

## Meta 資訊

- **單元編號**：Unit 02
- **單元標題**：物理厚度、倒角光線與 Vista 鏡面切面
- **副標題**：拆解 Windows Vista Aero 的靈魂密碼——用 `border`、雙層 `inset` 陰影、50% 高光階躍與文字光暈打造真實玻璃厚度
- **Slug**：`bevel-and-refraction`
- **分類**：`表面折射`
- **預計閱讀時間**：`12 分鐘`
- **關鍵字標籤**：`Inset Bevel`, `::before Cut`, `.vista-text`
- **成品路徑**：`lessons/bevel-and-refraction/index.html`
- **前後單元導覽**：
  - 上一單元：`../blur-and-saturation/index.html`（Unit 01 背景模糊與鮮豔度補償）
  - 下一單元：`../gpu-compositing-and-agents/index.html`（Unit 03 GPU 合成圖層效能瓶頸與 AGENTS.md 規範）
- **狀態**：`✅ 已定稿`

---

## 一、一句話核心觀念（TL;DR）

> 真正有「玻璃感」而不是「透明紙」的關鍵，在於 **邊緣厚度與表面鏡面反射**。透過「上左高光、下右微暗」的四邊不同透明度邊框＋`inset 0 1px 0 0 rgba(255,255,255,0.8)` 1 像素切角、`.glass-panel::before` 上半部 50% 鏡面反光階躍，以及 `.vista-text` 白色保護光暈，就能精準復刻 Vista Aero 經典的立體晶瑩感。

---

## 二、核心觀念拆解

### 卡片 1：物理厚度與光學倒角（Optical Bevel & Inset Shadow）
- **單色邊框為何顯得廉價**：四邊都寫 `border: 1px solid rgba(255,255,255,0.3)` 只是一條扁平線；真實玻璃板在頂部假設光源下，切角上緣與左緣會強烈聚光。
- **CSS 精準光學配方**：
  ```css
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-top-color: rgba(255, 255, 255, 0.7);
  border-left-color: rgba(255, 255, 255, 0.5);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 0 rgba(0, 0, 0, 0.1);
  ```
  外陰影撐起漂浮高度，上下 `inset` 1px 陰影則像極細的玻璃剖面反光與底部厚度陰影。

### 卡片 2：表面折射與高光切面（`::before` 50% 鏡面分界線）
- **Vista Aero 最具辨識度的光學特徵**：不只是柔和漸層，而是在玻璃上半部約 **50% 高度處突然產生非連續性的亮度階躍**，模擬平滑曲面玻璃反射上方天空或燈管的高光切線。
- **實作細節**：
  ```css
  .glass-panel::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.4) 0%,
      rgba(255, 255, 255, 0.05) 100%
    );
    pointer-events: none;
  }
  ```
  記得外層容器必須加上 `overflow: hidden` 與 `position: relative`，並於偽元素設定 **`pointer-events: none`**，才不會擋住使用者點擊卡片內的按鈕或選取文字！

### 卡片 3：Vista 風格的文字光暈（`.vista-text` 防護層）
- **半透明介面的致命痛點**：當底層背景正好捲動到深色樹影或強對比文字上方時，直接放在玻璃上的深色標題（`#1c1c1e`）會突然變得難以閱讀。
- **雙層柔和白色光暈**：
  ```css
  .vista-text {
    color: #1c1c1e;
    font-weight: 600;
    text-shadow:
      0 0 8px rgba(255, 255, 255, 0.9),
      0 0 16px rgba(255, 255, 255, 0.5);
  }
  ```
  外圍那圈柔和發光的白色防護層，就像當年 Windows Vista 視窗標題欄一樣，把深色文字穩穩托出來。

### ⚠️ 常見誤區與地雷提醒（Pitfall Alert）
- **誤區：「在 `::before` 加上高光層之後，卡片裡的按鈕突然點不到了！」**
- **真相**：偽元素 `::before` 預設會生成在文件流或定位層上方並攔截滑鼠事件。若忘記加上 **`pointer-events: none;`**（以及適當控制文字層 `position: relative; z-index: 1;`），整個上半部 50% 區域的按鈕與連結都會失靈！

---

## 三、互動實驗室規格（Interactive Lab Spec）

- **實驗室名稱**：Vista Aero 光學元件組裝器（Bevel × 50% Cut × Text Halo）
- **教學目的**：讓使用者像拆解玻璃零件一樣，獨立開關 4 個光學圖層，直觀體驗每一行 CSS 對立體感與文字辨識度的貢獻。
- **控制元件（Inputs）**：
  - 獨立圖層開關（Checkbox / Toggle）：
    1. 光學倒角亮邊（`border-top-color` 0.7 / `border-left-color` 0.5）
    2. 實體厚度內陰影（`inset 0 1px 0 0` 高光 ＋ `inset 0 -1px 0 0` 暗緣）
    3. `::before` 上半部 50% 鏡面反光切面（含切換「水平 50% 切線」或「微傾斜 165deg 光斑」）
    4. `.vista-text` 雙層白色防護光暈
  - 模擬背景衝突測試鈕：切換「高對比深色區塊穿越背後」檢驗 `.vista-text` 防護效果。
- **視覺化輸出（Outputs）**：
  - 模擬 Windows Vista / Aero 視窗面板即時變化預覽 ＋ 目前啟用層數之組裝 CSS 程式碼。

---

## 四、隨堂自我檢測（3 題單選題）

### Q1：為何 `.glass-panel` 通常將 `border-top-color` 與 `border-left-color` 設為較高不透明度（0.7 / 0.5），而右邊與下邊維持極低不透明度？
- A. 因為瀏覽器只支援設定上邊與左邊的邊框顏色
- B. 模擬來自左上方的環境光照射在玻璃倒角切面上，建立真實的光影厚度與立體感
- C. 為了縮小 CSS 檔案體積
- D. 讓表格框線自動對齊網格
- **正解**：`B`
- **詳解**：真實物理世界的倒角邊緣，迎光面（通常假設左上方）會產生高亮度反射，背光面（右下方）則維持暗淡，利用不對稱邊框即可用極低成本創造厚度感。

### Q2：製作 Vista 經典「上半部 50% 鏡面反光切面」的 `::before` 偽元素時，為何一定要加上 `pointer-events: none;`？
- A. 否則瀏覽器會自動隱藏整個偽元素
- B. 避免位於上層覆蓋面板的 `::before` 攔截滑鼠點擊，導致卡片上半部的按鈕或連結無法點擊
- C. 因為 `linear-gradient` 需要此屬性才能顯示漸層
- D. 可以讓模糊半徑自動加倍
- **正解**：`B`
- **詳解**：絕對定位的 `::before` 覆蓋了容器上半部 50% 區域；加上 `pointer-events: none;` 能讓所有點擊與選字事件穿透到下方的互動元件上。

### Q3：`.vista-text` 使用 `text-shadow: 0 0 8px rgba(255,255,255,0.9), 0 0 16px rgba(255,255,255,0.5)` 的主要設計目的為何？
- A. 製造強烈的霓虹燈閃爍動畫
- B. 在深色標題字周圍建立柔和高亮白色防護層，避免半透明底層圖案干擾文字可讀性
- C. 強制改變字體的語系編碼
- D. 讓文字變成全透明隱形狀態
- **正解**：`B`
- **詳解**：當半透明視窗滑過深色照片或雜亂背景時，文字容易糊成一團；外圍柔和白色光暈能確保與深色字元之間永遠保持足夠對比度。
