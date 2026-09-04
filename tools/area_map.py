# -*- coding: utf-8 -*-
"""Insert a schematic Asok area map into the #area section of the six index pages.

Walking times are the ones the site already publishes (Soi Cowboy 3 min,
Soi 23 bar area 5 min, Club LINE23 7 min from BTS Asok). The drawing is
explicitly a schematic, not to scale.
"""
import io, os, re

os.chdir(r"C:\Users\kango\bangkok-nightlife-guide")

CSS = """
/* ── AREA MAP ── */
.area-map-wrap {
  margin: 28px 0 8px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
}
/* the article column is a grid item, whose automatic minimum size is its
   min-content width; without this the map's min-width would widen the page */
.content-grid > .article-body { min-width: 0; }
.area-map-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; max-width: 100%; }
.area-map { display: block; width: 100%; min-width: 660px; height: auto; }
.area-map text { font-family: inherit; }
.area-map-caption {
  padding: 12px 18px 14px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--muted);
  line-height: 1.7;
}
.area-map-scroll:focus-visible { outline: 2px solid var(--orange); outline-offset: -2px; }
.area-map-hint { font-weight: 700; color: var(--orange); }
.area-map-wrap { position: relative; }
.area-map-wrap::after {
  content: ""; position: absolute; top: 0; right: 0; width: 44px; bottom: 56px;
  background: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.92));
  pointer-events: none;
}
"""

# label sets ---------------------------------------------------------------
L = {
"ja": dict(
  title="アソーク周辺エリアマップ",
  desc="BTSアソーク駅・MRTスクンビット駅・ターミナル21・ソイカウボーイ・ソイ23・Club LINE23 の位置関係を示した概念図。",
  sukhumvit="スクンビット通り",
  asok="アソーク通り（Soi 21）",
  soi23="ソイ23",
  cowboy="ソイカウボーイ",
  bts="BTS アソーク駅",
  mrt="MRT スクンビット駅",
  t21="ターミナル21",
  club="Club LINE23",
  nana="← ナナ方面",
  thonglor="トンロー方面 →",
  w3="徒歩3分", w5="徒歩5分", w7="徒歩7分",
  bars="バービア・スナック",
  legend_route="BTSアソーク駅からの徒歩ルート",
  hint="→ 横にスクロールできます　",
  caption="※ 位置関係を示す概念図です。縮尺は正確ではありません。徒歩分数はBTSアソーク駅からの目安で、"
          "信号待ちや通りの混雑で前後します。ソイカウボーイはソイ21とソイ23を結ぶ約150mの路地です。通りの向きも簡略化しています。",
),
"en": dict(
  title="Asok area map",
  desc="Schematic showing BTS Asok, MRT Sukhumvit, Terminal 21, Soi Cowboy, Soi 23 and Club LINE23.",
  sukhumvit="Sukhumvit Road",
  asok="Asok Montri Rd (Soi 21)",
  soi23="Soi 23",
  cowboy="Soi Cowboy",
  bts="BTS Asok",
  mrt="MRT Sukhumvit",
  t21="Terminal 21",
  club="Club LINE23",
  nana="← To Nana",
  thonglor="To Thonglor →",
  w3="3 min walk", w5="5 min walk", w7="7 min walk",
  bars="Beer bars & snack bars",
  legend_route="Walking route from BTS Asok",
  hint="Scroll sideways to see the whole map. ",
  caption="Schematic only — not drawn to scale. Walking times are from BTS Asok and vary with "
          "crossings and crowds. Soi Cowboy is a roughly 150 m lane linking Soi 21 and Soi 23. Street bearings are simplified too.",
),
"ko": dict(
  title="아속 일대 지도",
  desc="BTS 아속역·MRT 수쿰윗역·터미널21·소이 카우보이·소이 23·Club LINE23의 위치 관계를 나타낸 개념도.",
  sukhumvit="수쿰윗 로드",
  asok="아속 몬뜨리 로드(Soi 21)",
  soi23="소이 23",
  cowboy="소이 카우보이",
  bts="BTS 아속역",
  mrt="MRT 수쿰윗역",
  t21="터미널21",
  club="Club LINE23",
  nana="← 나나 방면",
  thonglor="통러 방면 →",
  w3="도보 3분", w5="도보 5분", w7="도보 7분",
  bars="비어바·스낵바",
  legend_route="BTS 아속역에서의 도보 경로",
  hint="→ 옆으로 스크롤할 수 있습니다　",
  caption="※ 위치 관계를 나타낸 개념도이며 축척은 정확하지 않습니다. 도보 시간은 BTS 아속역 기준이며 "
          "신호 대기와 혼잡에 따라 달라집니다. 소이 카우보이는 소이 21과 소이 23을 잇는 약 150m 골목입니다.도로의 방향도 단순화했습니다.",
),
"zh-Hans": dict(
  title="阿索克一带地图",
  desc="标示 BTS 阿索克站、MRT 素坤逸站、Terminal 21、牛仔街、素坤逸23巷与 Club LINE23 位置关系的示意图。",
  sukhumvit="素坤逸路",
  asok="阿索克路（Soi 21）",
  soi23="素坤逸23巷",
  cowboy="牛仔街 Soi Cowboy",
  bts="BTS 阿索克站",
  mrt="MRT 素坤逸站",
  t21="Terminal 21",
  club="Club LINE23",
  nana="← 前往娜娜",
  thonglor="前往通罗 →",
  w3="步行3分钟", w5="步行5分钟", w7="步行7分钟",
  bars="啤酒吧·小酒馆",
  legend_route="从 BTS 阿索克站出发的步行路线",
  hint="→ 可左右滑动查看　",
  caption="※ 本图为位置关系示意图，比例并不精确。步行时间以 BTS 阿索克站为起点，"
          "会因等红灯与人潮而变动。牛仔街是连接 Soi 21 与 Soi 23、长约150公尺的巷子。道路走向也做了简化。",
),
"zh-Hant": dict(
  title="阿索克一帶地圖",
  desc="標示 BTS 阿索克站、MRT 素坤逸站、Terminal 21、牛仔街、素坤逸23巷與 Club LINE23 位置關係的示意圖。",
  sukhumvit="素坤逸路",
  asok="阿索克路（Soi 21）",
  soi23="素坤逸23巷",
  cowboy="牛仔街 Soi Cowboy",
  bts="BTS 阿索克站",
  mrt="MRT 素坤逸站",
  t21="Terminal 21",
  club="Club LINE23",
  nana="← 前往娜娜",
  thonglor="前往通羅 →",
  w3="步行3分鐘", w5="步行5分鐘", w7="步行7分鐘",
  bars="啤酒吧·小酒館",
  legend_route="從 BTS 阿索克站出發的步行路線",
  hint="→ 可左右滑動檢視　",
  caption="※ 本圖為位置關係示意圖，比例並不精確。步行時間以 BTS 阿索克站為起點，"
          "會因等紅燈與人潮而變動。牛仔街是連接 Soi 21 與 Soi 23、長約150公尺的巷子。道路走向也做了簡化。",
),
}

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text_width(text, size):
    """Rough advance width: CJK/Hangul are full-width, latin roughly 0.55em."""
    ems = 0.0
    for ch in text:
        o = ord(ch)
        if 0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3            or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFF60:
            ems += 1.0
        elif ch == " ":
            ems += 0.30
        else:
            ems += 0.58
    return ems * size

def chip(x, y, text, w=None, fill="#ffffff", stroke="#d4d4e2", tcol="#3d3d5c",
         bold=False, size=15):
    """A white pill with centred text."""
    w = w if w else max(70, text_width(text, size) + 30)
    h = size + 15
    return (
      '<g><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="%s"/>'
      '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" fill="%s"%s>%s</text></g>'
      % (x - w / 2, y - h / 2, w, h, h / 2, fill, stroke,
         x, y + size * 0.36, size, tcol,
         ' font-weight="700"' if bold else "", esc(text)))

def svg(lang):
    d = L[lang]
    ROAD, ROAD_EDGE, ROAD_TXT = "#e9e9f1", "#dcdce8", "#7a7a9a"
    INK, ORANGE = "#1a1a2e", "#e85d26"
    p = []
    p.append('<svg class="area-map" viewBox="0 62 800 424" '
             'aria-labelledby="map-t map-d" xmlns="http://www.w3.org/2000/svg">')
    p.append('<title id="map-t">%s</title><desc id="map-d">%s</desc>' % (esc(d["title"]), esc(d["desc"])))
    p.append('<defs><marker id="arw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
             'markerHeight="6" orient="auto-start-reverse">'
             '<path d="M0,1 L9,5 L0,9 z" fill="%s"/></marker></defs>' % ORANGE)
    p.append('<rect x="0" y="62" width="800" height="424" fill="#fafaf8"/>')

    # roads
    p.append('<rect x="0" y="336" width="800" height="44" fill="%s" stroke="%s"/>' % (ROAD, ROAD_EDGE))
    p.append('<rect x="136" y="30" width="36" height="430" fill="%s" stroke="%s"/>' % (ROAD, ROAD_EDGE))
    p.append('<line x1="508" y1="352" x2="556" y2="100" stroke="%s" stroke-width="36" '
             'stroke-linecap="round"/>' % ROAD)
    p.append('<line x1="508" y1="352" x2="556" y2="100" stroke="%s" stroke-width="36" '
             'stroke-linecap="round" fill="none" opacity="0.35"/>' % ROAD_EDGE)
    p.append('<line x1="172" y1="240" x2="528" y2="240" stroke="%s" stroke-width="28" '
             'stroke-linecap="round"/>' % ROAD)

    # Terminal 21 block
    p.append('<rect x="26" y="222" width="106" height="84" rx="6" fill="#eef0f8" stroke="#d4d4e2"/>')
    t21 = d["t21"].split(" ")
    if len(t21) == 2:
        p.append('<text x="79" y="258" text-anchor="middle" font-size="13" fill="%s" '
                 'font-weight="700">%s</text>' % (INK, esc(t21[0])))
        p.append('<text x="79" y="278" text-anchor="middle" font-size="13" fill="%s" '
                 'font-weight="700">%s</text>' % (INK, esc(t21[1])))
    else:
        p.append('<text x="79" y="268" text-anchor="middle" font-size="13" fill="%s" '
                 'font-weight="700">%s</text>' % (INK, esc(d["t21"])))

    # road labels
    p.append('<text x="690" y="364" text-anchor="middle" font-size="15" fill="%s">%s</text>'
             % (ROAD_TXT, esc(d["sukhumvit"])))
    p.append('<text transform="translate(154 168) rotate(-90)" text-anchor="middle" font-size="14" '
             'fill="%s">%s</text>' % (ROAD_TXT, esc(d["asok"])))
    p.append('<text transform="translate(592 214) rotate(-78)" text-anchor="middle" font-size="15" '
             'fill="%s">%s</text>' % (ROAD_TXT, esc(d["soi23"])))
    p.append('<text x="330" y="246" text-anchor="middle" font-size="16" fill="%s" '
             'font-weight="700">%s</text>' % (INK, esc(d["cowboy"])))

    # direction hints
    p.append('<text x="14" y="326" font-size="13" fill="%s">%s</text>' % (ROAD_TXT, esc(d["nana"])))
    p.append('<text x="786" y="326" text-anchor="end" font-size="13" fill="%s">%s</text>'
             % (ROAD_TXT, esc(d["thonglor"])))

    # walking route: BTS -> east along Sukhumvit -> up Soi 23
    p.append('<path d="M154,406 L154,358 L506,358 L541,178" fill="none" stroke="%s" '
             'stroke-width="4" stroke-dasharray="11 7" stroke-linecap="round" '
             'marker-end="url(#arw)"/>' % ORANGE)

    # stations and spots
    p.append('<circle cx="154" cy="358" r="7" fill="#fff" stroke="%s" stroke-width="3"/>' % INK)
    p.append(chip(154, 424, d["bts"], bold=True))
    p.append('<circle cx="154" cy="300" r="6" fill="#fff" stroke="%s" stroke-width="3"/>' % INK)
    p.append(chip(268, 300, d["mrt"], bold=True))
    p.append('<line x1="161" y1="300" x2="%.0f" y2="300" stroke="#c9c9d8" stroke-width="1.5"/>'
             % (268 - (max(70, text_width(d["mrt"], 15) + 30)) / 2))

    # Soi 23 bar area
    p.append('<circle cx="519" cy="288" r="6" fill="#fff" stroke="%s" stroke-width="3"/>' % INK)
    p.append(chip(662, 288, d["bars"], size=14))
    p.append('<line x1="527" y1="288" x2="%.0f" y2="288" stroke="#c9c9d8" stroke-width="1.5"/>'
             % (662 - (max(70, text_width(d["bars"], 14) + 30)) / 2))

    # Club LINE23
    p.append('<a href="#shoplist" aria-label="%s">' % esc(d["club"]))
    p.append('<circle cx="546" cy="152" r="9" fill="%s"/>' % ORANGE)
    p.append('<circle cx="546" cy="152" r="15" fill="none" stroke="%s" stroke-width="2" '
             'opacity="0.45"/>' % ORANGE)
    p.append(chip(650, 152, d["club"], fill="#fff4ef", stroke=ORANGE, tcol="#b8471a",
                  bold=True, size=15))
    p.append("</a>")

    # walking-time chips
    p.append(chip(238, 204, d["w3"], fill="#fff", stroke="#e2e2ec", tcol=ROAD_TXT, size=13))
    p.append(chip(424, 296, d["w5"], fill="#fff", stroke="#e2e2ec", tcol=ROAD_TXT, size=13))
    p.append(chip(640, 106, d["w7"], fill="#fff4ef", stroke="#f0c3ab", tcol="#b8471a", size=13))

    # north arrow
    p.append('<g opacity="0.55"><path d="M62,132 L70,110 L78,132 L70,126 Z" fill="%s"/>'
             '<text x="70" y="150" text-anchor="middle" font-size="12" fill="%s" '
             'font-weight="700">N</text></g>' % (ROAD_TXT, ROAD_TXT))

    # legend
    p.append('<line x1="44" y1="466" x2="76" y2="466" stroke="%s" stroke-width="4" '
             'stroke-dasharray="11 7" stroke-linecap="round"/>' % ORANGE)
    p.append('<text x="86" y="471" font-size="13" fill="%s">%s</text>'
             % (ROAD_TXT, esc(d["legend_route"])))
    p.append("</svg>")
    return "".join(p)


def figure(lang):
    d = L[lang]
    return ('      <figure class="area-map-wrap">\n'
            '        <div class="area-map-scroll" tabindex="0" role="group" aria-label="%s">%s</div>\n'
            '        <figcaption class="area-map-caption">'
            '<span class="area-map-hint">%s</span>%s</figcaption>\n'
            '      </figure>\n\n'
            % (esc(d["title"]), svg(lang), esc(d["hint"]), esc(d["caption"])))


PAGES = {"index.html": "en", "en/index.html": "en", "ja/index.html": "ja",
         "ko/index.html": "ko", "zh/index.html": "zh-Hans", "zh-Hant/index.html": "zh-Hant"}

for path, lang in PAGES.items():
    s = io.open(path, encoding="utf-8", newline="").read()
    if "area-map-wrap" in s:
        print("already has the map:", path); continue

    # insert after the intro paragraph of the #area section
    m = re.search(r'(<h2 id="area">.*?</h2>\s*<p>.*?</p>\s*\n)', s, re.S)
    assert m, path + ": #area intro not found"
    s = s[:m.end(1)] + "\n" + figure(lang) + s[m.end(1):]
    s = s.replace("</style>", CSS + "</style>", 1)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("map inserted:", path)
