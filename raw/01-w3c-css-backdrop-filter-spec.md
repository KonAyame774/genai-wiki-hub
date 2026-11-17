# [Raw 01] W3C Filter Effects Module Level 2：`backdrop-filter` 與高斯模糊彩度衰減補償分析

- **文獻類型**：CSS 光學濾鏡技術規格摘要與光學實驗紀錄
- **核心標準參考**：W3C Filter Effects Module Level 2（`backdrop-filter` 屬性、Backdrop Root 建立規則）
- **對應 Wiki 單元**：Unit 01（`notes/blur-and-saturation.md`）

---

## 一、規範核心：`backdrop-filter` 如何運作？

依據 **W3C Filter Effects Module Level 2** 定義，與作用在元素自身與子內容上的 `filter` 不同，`backdrop-filter` 會將「元素後方所有屬於同一 **Backdrop Root（背景根）** 的視覺內容」擷取進離屏渲染緩衝區（Offscreen Buffer），依序套用濾鏡鏈（Filter Chain）後，再與當前元素自身的半透明背景（`background`）進行 Alpha 合成（Compositing）。

關鍵光學條件：
1. **必須搭配半透明背景**：若元素設定 `background: #ffffff`（不透明度 1.0），後方模糊運算結果將完全被遮蔽；實務上需將底色控制在 `rgba(255, 255, 255, 0.08)` ～ `rgba(255, 255, 255, 0.34)` 之間。
2. **Backdrop Root 邊界效應**：套用 `backdrop-filter`、`opacity < 1`、`transform` 或 `filter` 的元素都會建立新的 Backdrop Root，影響後方像素的採樣範圍與瀏覽器合成圖層切分。
3. **跨瀏覽器前綴**：為兼容 Safari 與舊版 WebKit 核心引擎，規格書與工程實務建議同步宣告 `-webkit-backdrop-filter` 與標準 `backdrop-filter`。

---

## 二、為什麼單純 `blur()` 會讓毛玻璃看起來「發灰又混濁」？

### 物理成因：線性空間下的高斯鄰域均化（Gaussian Neighbor Averaging）
二維高斯模糊（Gaussian Blur）以核函數 $G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$ 對周圍像素進行加權平均：
- 當模糊半徑設為 `blur(20px)` 時，視窗背後原本鮮明的藍色、綠色、紫紅色光塊會在半徑內互相混合。
- 互補色與高頻色彩細節混合的結果，就是 RGB 三通道數值趨近中間灰（Neutral Gray），導致畫面**有效彩度（Chroma / Saturation）大幅衰減約 32%～45%**。
- 若上方再疊加一層帶有白霧感的半透明白底（例如 `rgba(255, 255, 255, 0.25)`），玻璃表面就會變成「髒髒的水泥灰」，失去高級玻璃的通透光感。

---

## 三、解決方案：`saturate(190%)` 鮮豔度補償參數

為了抵銷高斯模糊造成的色彩流失，Apple Human Interface Guidelines（Vibrancy / Liquid Glass 材質設計）與現代毛玻璃規範會在濾鏡鏈中串接 `saturate()`：

```css
backdrop-filter: blur(20px) saturate(190%);
-webkit-backdrop-filter: blur(20px) saturate(190%);
```

### 參數比較數據（基準背景：深海極光網格漸層）
| 濾鏡設定 | 視覺效果評價 | 備註 |
| :--- | :--- | :--- |
| `blur(20px)`（僅模糊、無補償） | 明顯灰濁、顏色黯淡 | 彩度約流失 32%～45% |
| `blur(20px) saturate(120%)` | 略為改善但仍偏霧 | 適合低飽和度文書界面 |
| `blur(20px) saturate(190%)` | **色彩通透鮮明、邊緣乾淨** | 本知識庫 `.glass-panel` 黃金標準值 |
| `blur(20px) saturate(280%)` | 過度鮮豔甚至色偏霓虹 | 高飽和底圖容易溢出 sRGB 色域 |

> **結論重點**：濾鏡鏈的執行順序為由左至右，先執行 `blur(20px)` 完成擴散後，再以 `saturate(190%)` 拉回鮮豔度，可同時兼顧文字底襯柔和度與極光透光感。
