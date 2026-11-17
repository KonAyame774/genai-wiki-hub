# [證據卡 02] Unit 02：物理厚度、倒角光線與 Vista 鏡面切面

- **限定來源（嚴禁混入其他單元）**：
  - `notes/bevel-and-refraction.md`
  - `raw/02-vista-dwm-aero-optical-spec.md`
- **對應網頁出處**：`../lessons/bevel-and-refraction/index.html`

---

## 1. 新手一句話比喻
> 四邊顏色一樣的透明方框看起來像廉價塑膠片；Windows Vista Aero 的秘訣是「想像光從左上方 45 度打下來」：讓上／左邊框發亮、`inset` 切出 1 像素玻璃厚邊，再用上半部 50% 高光反射天花板日光燈！

## 2. 經來源查證之核心數據
- **不對稱倒角邊框**：四邊底邊 `rgba(255, 255, 255, 0.2)`，但頂邊拉高至 **`border-top-color: rgba(255, 255, 255, 0.7)`**，左邊調亮至 **`border-left-color: rgba(255, 255, 255, 0.5)`**。
- **1 像素物理厚度陰影**：`box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), inset 0 1px 0 0 rgba(255, 255, 255, 0.8), inset 0 -1px 0 0 rgba(0, 0, 0, 0.1);`。
- **Vista 經典 50% 鏡面切面**：`.glass-panel::before` 設 `height: 50%;` 並搭配 `linear-gradient(180deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.05) 100%)`，在高度剛好 **`50%`** 處切出非連續鏡面反射階躍。
- **`.vista-text` 文字防護光暈**：深色文字（`#1c1c1e`）搭配雙層白色外發光：`text-shadow: 0 0 8px rgba(255, 255, 255, 0.9), 0 0 16px rgba(255, 255, 255, 0.5);`。

## 3. 新手必避誤區
- 絕對不可忘記在 `.glass-panel::before` 加上 **`pointer-events: none;`**（以及容器內子元素設定 `z-index: 1`），否則透明高光偽元素會擋住滑鼠，讓卡片上半部的按鈕全部點不到！
