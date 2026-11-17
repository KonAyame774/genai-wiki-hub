# [Raw 06] W3C WCAG 2.2 對比度基準與無障礙減少透明度退場規範

- **文獻類型**：網頁無障礙（Accessibility, a11y）與漸進增強 CSS 規範整理
- **核心標準參考**：W3C WCAG 2.2 Success Criterion 1.4.3 / 1.4.6、CSS Media Queries Level 5（`prefers-reduced-transparency`）、`@supports` 特性查詢
- **對應 Wiki 單元**：Unit 06（`notes/accessibility-fallback.md`）

---

## 一、毛玻璃介面最大的隱藏風險：可讀性崩潰

毛玻璃靠背後的流動色彩創造美感，但也正因為底圖顏色時刻變化，當高亮度白字疊在淺藍極光上，或深黑文字碰上深靛藍圓球時，文字與背景的相對亮度比（Contrast Ratio）會瞬間跌破法定無障礙標準，對老花、弱視、色覺異常或戶外強光下的使用者造成嚴重閱讀障礙。

---

## 二、W3C WCAG 2.2 文字對比度數學標準

相對亮度 $L$ 依據 sRGB 線性化轉換計算（範圍 `0.0` 純黑 ～ `1.0` 純白），對比度公式為：

$$\text{Contrast Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05} \quad (L_1 \ge L_2)$$

| 等級與情境 | 最低對比度要求 | 介面設計意義 |
| :--- | :--- | :--- |
| **WCAG AA（一般內文 `< 18pt`）** | **`4.5 : 1`** | 網頁基本合規底線（歐美無障礙法規門檻） |
| **WCAG AA（大標題 `>= 18pt` 或粗體 `>= 14pt`）** | **`3.0 : 1`** | Hero 大標、卡片主標題最低門檻 |
| **WCAG AAA（加強型無障礙規範）** | **`7.0 : 1`** | 醫療、金融與高齡友善閱讀環境目標 |

> **註**：`.vista-text` 的 `text-shadow` 白色光暈能在視覺上幫深色字 `#1c1c1e` 爭取局部底色，但嚴格來說不能取代底層遮罩本身應達到的基礎對比度——建議內層文字區底色不透明度提升至 `rgba(255, 255, 255, 0.58)` ～ `0.72` 以穩定守住 `4.5:1`。

---

## 三、雙重降級防護罩：`prefers-reduced-transparency` 與 `@supports`

### 1. 尊重作業系統「減少透明度」無障礙設定
macOS / iOS「減少透明度」、Windows 11「關閉透明效果」會觸發 CSS Media Queries Level 5 查詢：

```css
@media (prefers-reduced-transparency: reduce) {
  .glass-panel {
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    background: rgba(248, 250, 252, 0.94);
    border-color: rgba(15, 23, 42, 0.22);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.14);
  }
  .glass-panel::before {
    opacity: 0.18;
  }
}
```
開啟時直接撤除高透明度透視並轉為 `0.94` 高不透明度潔白霧面卡片，確保文字對比度穩定高於 `10:1`。

### 2. 舊版瀏覽器或停用硬體加速環境的 `@supports` 退場
不支援 `backdrop-filter` 的瀏覽器若只拿到 `rgba(255,255,255,0.18)` 的極薄白底而背後又沒被模糊掉，背景強烈字樣與雜訊會直接穿透過文字。因此務必寫出雙重保底：

```css
/* 不支援 backdrop-filter 時，提供較實的磨砂背景確保可讀性 */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass-panel {
    background: rgba(248, 250, 252, 0.90);
  }
}
```
只有在確認支援濾鏡與未要求減少透明度時，才釋放通透光學效果，這才是負責任的現代前端光學工程。
