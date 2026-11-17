# [證據卡 06] Unit 06：WCAG 對比度驗證與無障礙降級策略

- **限定來源（嚴禁混入其他單元）**：
  - `notes/accessibility-fallback.md`
  - `raw/06-wcag-contrast-and-reduced-transparency.md`
- **對應網頁出處**：`../lessons/accessibility-fallback/index.html`

---

## 1. 新手一句話比喻
> 漂亮的玻璃窗不該讓視力不佳或用舊手機的人看不清字條——先靠底色濃度把可讀性墊到及格線以上，再準備好「系統要求減透明」與「舊瀏覽器失效」兩套自動切換的霧面安全傘！

## 2. 經來源查證之核心數據
- **WCAG 2.2 文字對比公式**：$\text{Contrast Ratio} = (L_1 + 0.05) / (L_2 + 0.05)$。
  - 一般內文 **AA 級底線**：**`4.5 : 1`**
  - 大標題（`>= 18pt`）AA 級：**`3.0 : 1`**
  - 加強型 **AAA 級**：**`7.0 : 1`**
- **第一道安全傘（系統輔助功能）**：`@media (prefers-reduced-transparency: reduce)` 關閉 `backdrop-filter`，把背景拉實至 `rgba(248, 250, 252, 0.94)`，穩拿 `> 10:1` 對比度。
- **第二道安全傘（舊瀏覽器保底）**：`@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))` 將背景提升為 `rgba(248, 250, 252, 0.90)`，避免無模糊時雜亂底圖直接穿透文字。

## 3. 新手必避誤區
- 不可只依賴 `.vista-text` 的 `text-shadow` 而把文字區底色降成極淡 `0.12`；內層閱讀區需先靠 `rgba(255, 255, 255, 0.58～0.75)` 站穩 `>= 4.5:1`。
