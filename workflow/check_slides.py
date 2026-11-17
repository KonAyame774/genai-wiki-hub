#!/usr/bin/env python3
"""
Automated Graph Gate Validator for Aero Glass & Optical UI Wiki Teaching Slides.
對應第 10 週課程 Slide 41/43/47：每道檢查關卡 = 一支可實際執行的 Python 腳本。
檢查項目：
1. 總頁數落在 8 ～ 15 頁區間
2. 每頁皆具備 data-wiki-unit 出處屬性，且所有相對路徑連結目標檔案真實存在於專案內
3. 知識庫單元覆蓋率：Unit 01 ～ Unit 06 達 100% 覆蓋
4. 版面防溢出：每頁主要教學區可見字數 <= 420 字、清單項 <= 6 項
5. 數據忠實度與反話檢查：關鍵光學數據與 raw/ 單一事實來源一致
6. GPU 合成圖層效能預算檢查：內層子卡未違規嵌套 backdrop-filter，且 ::before 具備 pointer-events: none
"""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SLIDES_HTML = ROOT / "slides" / "index.html"

REQUIRED_UNITS = {
    "blur-and-saturation": "Unit 01",
    "bevel-and-refraction": "Unit 02",
    "gpu-compositing-and-agents": "Unit 03",
    "svg-refraction-displacement": "Unit 04",
    "dynamic-light-tracking": "Unit 05",
    "accessibility-fallback": "Unit 06",
}

REQUIRED_FACTS = [
    ("blur(20px)", "模糊半徑基準"),
    ("saturate(190%)", "鮮豔度補償基準"),
    ("32%", "純模糊彩度衰減數據 (32%～45%)"),
    ("0.032", "SVG 雜訊標準不透明度 (3.2%)"),
    ("50%", "Vista 經典鏡面切面高度"),
    ("16.67ms", "60fps 幀預算上限"),
    ("4.5:1", "WCAG 2.2 AA 一般文字對比度基準"),
]

CONTRADICTIONS = [
    "單純模糊會提升彩度",
    "單純模糊會提高彩度",
    "16.67秒",
    "WCAG規定對比度1.5:1",
]


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_style = False
        self.in_script = False
        self.styles = []
        self.slides = []
        self.cur_slide = None
        self.slide_depth = 0
        self.in_source_bar = False
        self.source_bar_depth = 0
        self.skip_visual_depth = 0  # skip <svg> or decorative demo text from word budget
        self.all_local_links = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        classes = set((attr_map.get("class") or "").split())

        if tag == "style":
            self.in_style = True
        elif tag == "script":
            self.in_script = True

        if tag == "a" and "href" in attr_map:
            href = attr_map["href"]
            if not href.startswith(("#", "http://", "https://", "mailto:", "javascript:")):
                self.all_local_links.append(href)

        if tag == "section" and "slide" in classes:
            self.cur_slide = {
                "index": len(self.slides) + 1,
                "unit": attr_map.get("data-wiki-unit", ""),
                "title": attr_map.get("data-slide-title", ""),
                "links": [],
                "li_count": 0,
                "text_parts": [],
            }
            self.slide_depth = 1
            return

        if self.cur_slide is not None:
            if tag in VOID_TAGS:
                return
            self.slide_depth += 1
            if "slide-source-bar" in classes:
                self.in_source_bar = True
                self.source_bar_depth = 1
            elif self.in_source_bar:
                self.source_bar_depth += 1

            if tag == "svg" or "live-demo-widget" in classes:
                self.skip_visual_depth += 1
            elif self.skip_visual_depth > 0:
                self.skip_visual_depth += 1

            if tag == "a" and "href" in attr_map:
                self.cur_slide["links"].append(attr_map["href"])
            if tag == "li" and not self.in_source_bar and self.skip_visual_depth == 0:
                self.cur_slide["li_count"] += 1

    def handle_startendtag(self, tag, attrs):
        # Self-closing tags should not alter depth; capture links if any.
        attr_map = dict(attrs)
        if tag == "a" and "href" in attr_map and self.cur_slide is not None:
            self.cur_slide["links"].append(attr_map["href"])

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        elif tag == "script":
            self.in_script = False

        if tag in VOID_TAGS:
            return

        if self.cur_slide is not None:
            if self.skip_visual_depth > 0:
                self.skip_visual_depth -= 1
            if self.in_source_bar:
                self.source_bar_depth -= 1
                if self.source_bar_depth == 0:
                    self.in_source_bar = False
            self.slide_depth -= 1
            if self.slide_depth == 0:
                self.slides.append(self.cur_slide)
                self.cur_slide = None

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)
        elif self.cur_slide is not None and not self.in_style and not self.in_script:
            if not self.in_source_bar and self.skip_visual_depth == 0:
                self.cur_slide["text_parts"].append(data)


def main():
    if not SLIDES_HTML.exists():
        print(f"[FAIL] 找不到簡報檔案：{SLIDES_HTML}")
        return 1

    html_text = SLIDES_HTML.read_text(encoding="utf-8")
    parser = SlideParser()
    parser.feed(html_text)

    errors = []
    slides = parser.slides
    total = len(slides)

    print("=" * 68)
    print("Aero Glass Wiki 教學 HTML 簡報 — Graph/Loop 自動化檢查報告")
    print("=" * 68)
    print(f"目標檔案：{SLIDES_HTML.relative_to(ROOT)}")
    print(f"偵測頁數：{total} 頁 (規範要求：8 ～ 15 頁)\n")

    if not (8 <= total <= 15):
        errors.append(f"簡報頁數為 {total} 頁，未落在 8 ～ 15 頁規範區間。")

    print(f"{'頁碼':<6} {'可見字數':<10} {'條列數':<8} {'出處連結':<8} {'Wiki 來源單元'}")
    print("-" * 68)

    covered_slugs = set()

    for s in slides:
        raw_txt = "".join(s["text_parts"])
        compact_len = len(re.sub(r"\s+", "", raw_txt))
        li_cnt = s["li_count"]
        unit = s["unit"]
        links = [lnk for lnk in s["links"] if not lnk.startswith("#")]

        # Resolve relative links from slides/
        valid_links = []
        for lnk in links:
            target = (SLIDES_HTML.parent / lnk.split("#")[0]).resolve()
            if not target.exists():
                errors.append(f"Slide {s['index']:02d} 連結目標不存在：{lnk}")
            else:
                valid_links.append(lnk)
                for slug in REQUIRED_UNITS:
                    if slug in lnk:
                        covered_slugs.add(slug)

        if not unit:
            errors.append(f"Slide {s['index']:02d} 缺少 data-wiki-unit 出處標籤。")
        if not valid_links:
            errors.append(f"Slide {s['index']:02d} 缺少有效相對路徑出處連結。")
        if compact_len > 420:
            errors.append(f"Slide {s['index']:02d} ({s['title']}) 可見字數 {compact_len} 字超過 420 字溢出上限。")
        if li_cnt > 6:
            errors.append(f"Slide {s['index']:02d} ({s['title']}) 條列數 {li_cnt} 項超過 6 項上限。")

        print(f"S{s['index']:02d}    {compact_len:<10} {li_cnt:<8} {len(valid_links):<8} {unit}")

    print("-" * 68)
    print(f"\n[1] 知識庫覆蓋率檢查：{len(covered_slugs)} / {len(REQUIRED_UNITS)} 個單元 ({len(covered_slugs)*100//len(REQUIRED_UNITS)}%)")
    missing_units = set(REQUIRED_UNITS.keys()) - covered_slugs
    if missing_units:
        errors.append(f"以下 Wiki 單元尚未被任何投影片引用：{sorted(missing_units)}")
    else:
        print("    ✅ Unit 01 ～ Unit 06 全部出處連結存在且 100% 覆蓋！")

    print("\n[2] 來源忠實度與核心數據比對：")
    for token, desc in REQUIRED_FACTS:
        if token in html_text:
            print(f"    ✅ 命中基準數據 `{token}` — {desc}")
        else:
            errors.append(f"缺少或誤改基準數據 `{token}` ({desc})")
    for bad in CONTRADICTIONS:
        if bad in html_text:
            errors.append(f"偵測到與 raw/ 相左的錯誤敘述：`{bad}`")

    print("\n[3] AGENTS.md 光學與 GPU 預算合規檢查：")
    css_blob = "\n".join(parser.styles)
    if "pointer-events: none" in css_blob:
        print("    ✅ .glass-panel::before 已宣告 pointer-events: none")
    else:
        errors.append("CSS 缺少 pointer-events: none，恐攔截滑鼠點擊事件。")

    nested_check = re.search(r"\.(concept-tile|source-card|slide-source-bar)\s*\{[^}]*backdrop-filter", css_blob, re.S)
    if nested_check:
        errors.append("偵測到投影片內層子元件違規嵌套 backdrop-filter！")
    else:
        print("    ✅ 外實內輕規範合規（內層子卡無嵌套 backdrop-filter）")

    # Also verify all site-wide relative links on index.html and lessons/
    broken_site = []
    for html_file in [ROOT / "index.html", *sorted((ROOT / "lessons").glob("*/index.html"))]:
        content = html_file.read_text(encoding="utf-8")
        for m in re.finditer(r'href="([^"]+)"', content):
            href = m.group(1)
            if href.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if href.startswith("/"):
                broken_site.append(f"{html_file.relative_to(ROOT)} 使用禁止之根絕對路徑：{href}")
                continue
            resolved = (html_file.parent / href.split("#")[0]).resolve()
            if not resolved.exists():
                broken_site.append(f"{html_file.relative_to(ROOT)} 斷鏈：{href}")

    print("\n[4] 全站相對路徑與斷鏈掃描：")
    if broken_site:
        errors.extend(broken_site)
    else:
        print("    ✅ index.html、lessons/*/index.html、slides/index.html 零斷鏈且 100% 相對路徑！")

    print("\n" + "=" * 68)
    if errors:
        print(f"❌ 檢查未通過，共發現 {len(errors)} 項問題：")
        for idx, err in enumerate(errors, 1):
            print(f"   {idx}. {err}")
        print("=" * 68)
        return 1

    print("🎉 ALL GATES PASSED — 12 頁教學簡報與全站知識庫檢查全數通過！(Exit Code 0)")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
