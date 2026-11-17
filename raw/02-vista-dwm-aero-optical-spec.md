# [Raw 02] Windows Vista DWM Aero Glass 光學規範：實體倒角、50% 鏡面切面與文字防護光暈

- **文獻類型**：桌面視窗合成器（Desktop Window Manager, DWM）光學設計文獻整理
- **核心標準參考**：Windows Vista Aero UI Optical Design Principles & Modern CSS 轉譯規範
- **對應 Wiki 單元**：Unit 02（`notes/bevel-and-refraction.md`）

---

## 一、什麼是 Windows Vista Aero 的光學語彙？

2006 年隨 Windows Vista 登場的 **Aero Glass** 介面設計，是人類作業系統歷史上首次大規模透過 GPU DirectX 合成器，在視窗邊框模擬「真實壓克力／厚實玻璃片」的折射與環境光反射。其之所以在視覺上遠比近代扁平化半透明面板更有立體感，仰賴以下三大光學構造：

---

## 二、三大經典光學構造與 CSS 參數對應

### 1. 不對稱物理厚度倒角（Top-Left Light Bevel + 1px Inset Thickness）
真實世界的光線通常從**左上方 45 度角**照射：
- **外層邊框亮暗分離**：不能四邊使用相同透明度（例如單寫 `border: 1px solid rgba(255,255,255,0.3)` 會顯得像塑膠薄膜）。
  - 頂部高光邊框：`border-top-color: rgba(255, 255, 255, 0.7)`
  - 左側高光邊框：`border-left-color: rgba(255, 255, 255, 0.5)`
  - 右側與底部暗邊：`border: 1px solid rgba(255, 255, 255, 0.2)`
- **1px 內側厚度高光（`inset` 陰影）**：玻璃切割後會有側面導角厚度，必須透過多層 `box-shadow` 疊加：
  - 外擴散陰影：`0 20px 40px rgba(0, 0, 0, 0.2)`（將玻璃面板推離背景產生浮空景深）
  - 頂部 1px 內高光：`inset 0 1px 0 0 rgba(255, 255, 255, 0.8)`（模擬玻璃切角反射天光）
  - 底部 1px 內暗角：`inset 0 -1px 0 0 rgba(0, 0, 0, 0.1)`（強化底部壓實陰影邊界）

### 2. 上半部 50% 非連續鏡面切面（Vista Specular 50% Cut）
Vista Aero 按鈕、標題列與玻璃面板最標誌性的特徵，是在元件上方佔比剛好 **`50%`** 的區域繪製一層平滑高光，並在中心 `50%` 水平線產生**急遽非連續階躍（Sharp Specular Horizon）**，模擬拋光玻璃反射遠方室內燈光與地平線：
- CSS 以 `::before` 偽元素實作：
  - `height: 50%`（強制覆蓋上半部）
  - `background: linear-gradient(180deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.05) 100%)`
  - **關鍵交互守則**：務必設定 `pointer-events: none;`，否則透明偽元素會攔截滑鼠點擊、文字選取與按鈕 Hover 事件。

### 3. `.vista-text` 雙層白光文字防護光暈（Text Halo）
半透明毛玻璃後方常會經過高彩度極光圖片、深色陰影或高對比格線，導致深色文字（`#1c1c1e`）局部失去辨識度。Vista DWM 在標題欄與視窗文字背後加入了擴散柔和的白色外發光保護圈（Outer Glow）：

```css
.vista-text {
  color: #1c1c1e;
  font-weight: 600;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.9),
    0 0 16px rgba(255, 255, 255, 0.5);
}
```

雙層 `text-shadow` 的物理意義：
- 第一層 `0 0 8px rgba(255, 255, 255, 0.9)`：在字元筆畫緊貼邊緣建立高濃度白色隔離帶，確保筆畫銳利不糊開。
- 第二層 `0 0 16px rgba(255, 255, 255, 0.5)`：向外平滑衰減，使光暈融入玻璃霧面而非形成生硬白框。
