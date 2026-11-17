# [節點 3 產出] 教學型 HTML 簡報大綱（12 頁結構 ＋ 人類確認關卡）

- **目標受眾**：原本不熟悉 CSS 光學效果、SVG 濾鏡與瀏覽器 GPU 合成機制的初學者
- **預期頁數**：12 頁（落在 `8 ～ 15` 頁規格區間）
- **知識來源覆蓋**：`Unit 01` ～ `Unit 06` 全數覆蓋（100%），並納入 `wiki/index.md` 與 `workflow/report.md`
- **關卡 B（人類審核教學結構）狀態**：✅ **已確認（採「痛點導入 → 光學基底 → 表面折射 → 動態互動 → 效能無障礙 → Graph/Loop 總結」由淺入深順序）**

---

| 頁碼 | 投影片標題 | 新手教學重點與比喻 | 綁定證據卡 / Wiki 單元 |
| :---: | :--- | :--- | :--- |
| **Slide 01** | 封面：什麼是 Aero Glass 與介面光學設計？ | 認識從 Windows Vista Aero 到 Apple Liquid Glass 的演進，以及本簡報如何從 LLM Wiki 生成 | `wiki/index.md`、`raw/00` |
| **Slide 02** | 新手痛點：為何你的毛玻璃「灰濁、扁平又卡頓」？ | 點破新手只寫 `backdrop-filter: blur()` 時常見的 4 大盲點，建立全局學習地圖 | `card-01`、`card-02`、`card-03`（Unit 01–03） |
| **Slide 03** | 光學基底（一）：高斯模糊混色與 `saturate(190%)` 補償 | 解釋為何純模糊讓彩度衰減 32%～45%，展示 `blur(20px) saturate(190%)` 視覺差異 | `card-01`（Unit 01 `blur-and-saturation`） |
| **Slide 04** | 光學基底（二）：3% SVG 微觀磨砂消弭色階斷裂 | 看懂 8-bit 漸層色帶問題，與 `baseFrequency="0.85"`、`opacity: 0.032`（2%～4%）的 Dithering 原理 | `card-01`（Unit 01 `blur-and-saturation`） |
| **Slide 05** | 表面折射（一）：物理厚度、光學倒角與 `inset` 高光 | 利用左上 45 度角假設光源，`border-top (0.7)`/`border-left (0.5)` 與 1px `inset` 做出玻璃實體厚度 | `card-02`（Unit 02 `bevel-and-refraction`） |
| **Slide 06** | 表面折射（二）：Vista `::before` 50% 切面與文字光暈 | 拆解上半部 `50%` 鏡面階躍、`pointer-events: none` 防坑，與 `.vista-text` 雙層白光保護 | `card-02`（Unit 02 `bevel-and-refraction`） |
| **Slide 07** | 進階表面折射：SVG `<feDisplacementMap>` 與邊緣色散 | 用凹凸透鏡比喻理解像素位移公式 $P'(x,y)$，比較高頻雜訊 vs 低頻曲面折射 (`0.015～0.045`) | `card-04`（Unit 04 `svg-refraction-displacement`） |
| **Slide 08** | 動態光學互動：游標座標 `--mx` / `--my` 即時追蹤 | 拆解手電筒追光原理、`mask-composite: exclude` 外框發光與零 Reflow，內含可直接測試的追光卡 | `card-05`（Unit 05 `dynamic-light-tracking`） |
| **Slide 09** | 效能工程：GPU 合成圖層瓶頸與 60fps「外實內輕」守則 | 用畫師比喻理解 `16.67ms` 幀預算、嵌套 4 倍雪崩與 `rgba(255,255,255,0.58)` 解決方案 | `card-03`（Unit 03 `gpu-compositing-and-agents`） |
| **Slide 10** | 無障礙退場：WCAG `4.5:1` 對比度與雙重保險 | 認識一般內文 AA `4.5:1` 底線，以及 `@media (prefers-reduced-transparency)` 與 `@supports not` 退場 | `card-06`（Unit 06 `accessibility-fallback`） |
| **Slide 11** | 本週工程揭密：從 Wiki 到簡報的 Graph + Loop 工作流 | 視覺化呈現我們如何用「證據卡隔離 → 局部退回 → `check_slides.py` 驗收」自動產出本簡報 | `workflow/report.md`、`AGENTS.md` |
| **Slide 12** | 總結：介面光學設計 5 大口訣與 6 大實驗室傳送門 | 新手實作速查總表，附 6 個互動光學實驗室一鍵直達連結 | `card-01` ～ `card-06`（Unit 01–06） |
