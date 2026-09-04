# -*- coding: utf-8 -*-
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = {
 "en":      '"Helvetica Neue",Helvetica,Arial,sans-serif',
 "ja":      '"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif',
 "ko":      '"Malgun Gothic","Noto Sans KR","Apple SD Gothic Neo",sans-serif',
 "zh-Hans": '"Microsoft YaHei","Noto Sans SC",sans-serif',
 "zh-Hant": '"Microsoft JhengHei","Noto Sans TC",sans-serif',
}

V = [
 ("budget-en","en",["Bangkok Nightlife","Budget Guide 2026"],"What a night in Asok costs, line by line","1,500-9,000 THB PER PERSON"),
 ("budget-ja","ja",["バンコク夜遊び","予算ガイド 2026"],"1晩いくらかかるか、費目別に全部出します","1人あたり 1,500〜9,000฿"),
 ("budget-ko","ko",["방콕 밤문화","예산 가이드 2026"],"하룻밤에 얼마 드는지 항목별로 공개","1인 기준 1,500~9,000밧"),
 ("budget-zh-Hans","zh-Hans",["曼谷夜生活","预算指南 2026"],"一晚要花多少钱，逐项算给你看","人均 1,500~9,000泰铢"),
 ("budget-zh-Hant","zh-Hant",["曼谷夜生活","預算指南 2026"],"一晚要花多少錢，逐項算給你看","每人 1,500~9,000泰銖"),
]

TPL = """<html lang="{lang}"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#14142a;color:#fff;font-family:{font};position:relative}}
.glow-a{{position:absolute;width:760px;height:760px;right:-230px;top:-300px;border-radius:50%;
  background:radial-gradient(circle,rgba(232,93,38,0.55) 0%,rgba(232,93,38,0.14) 42%,rgba(232,93,38,0) 68%);}}
.glow-b{{position:absolute;width:620px;height:620px;left:-220px;bottom:-300px;border-radius:50%;
  background:radial-gradient(circle,rgba(201,150,58,0.40) 0%,rgba(201,150,58,0.10) 45%,rgba(201,150,58,0) 70%);}}
.grid{{position:absolute;inset:0;
  background-image:linear-gradient(rgba(255,255,255,0.030) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,0.030) 1px,transparent 1px);
  background-size:60px 60px;}}
.frame{{position:absolute;inset:26px;border:1px solid rgba(201,150,58,0.34);border-radius:8px}}
.wrap{{position:relative;height:100%;padding:76px 88px;display:flex;flex-direction:column;justify-content:center}}
.kicker{{position:absolute;top:64px;left:88px;font-size:19px;letter-spacing:.30em;
  color:#c9963a;font-weight:700;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}}
.bars{{position:absolute;top:60px;right:88px;display:flex;gap:7px;align-items:flex-end;height:34px}}
.bars i{{display:block;width:7px;border-radius:3px;background:#e85d26}}
.title{{font-size:{tsize}px;line-height:1.20;font-weight:800;letter-spacing:-0.005em;
  text-shadow:0 3px 26px rgba(0,0,0,0.45)}}
.title span{{display:block}}
.rule{{width:104px;height:5px;border-radius:3px;background:#e85d26;margin:34px 0 26px}}
.sub{{font-size:{ssize}px;line-height:1.55;color:#d9d9ea;font-weight:500;max-width:930px}}
.foot{{position:absolute;bottom:64px;left:88px;right:88px;display:flex;justify-content:space-between;align-items:center}}
.tag{{font-size:21px;letter-spacing:.06em;color:#f0b183;font-weight:700}}
.dom{{font-size:20px;letter-spacing:.05em;color:#fff;font-weight:700;
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif}}
.dom b{{color:#c9963a}}
</style></head><body>
<div class="glow-a"></div><div class="glow-b"></div><div class="grid"></div><div class="frame"></div>
<div class="wrap">
  <div class="kicker">ASOK NIGHTLIFE</div>
  <div class="bars"><i style="height:14px"></i><i style="height:26px"></i><i style="height:34px;background:#c9963a"></i><i style="height:20px"></i></div>
  <div class="title">{titlehtml}</div>
  <div class="rule"></div>
  <div class="sub">{sub}</div>
  <div class="foot"><div class="tag">{tagline}</div><div class="dom">bangkoknight<b>guide</b>.com</div></div>
</div></body></html>"""

for key, lang, lines, sub, tagline in V:
    longest = max(len(l) for l in lines)
    cjk = lang != "en"
    tsize = 78 if (cjk and longest <= 11) else 70 if cjk else (78 if longest <= 18 else 70)
    ssize = 30 if cjk else 31
    html = TPL.format(lang=lang, font=FONTS[lang], tsize=tsize, ssize=ssize,
                      titlehtml="".join("<span>%s</span>" % l for l in lines),
                      sub=sub, tagline=tagline)
    io.open(os.path.join(HERE, "og-%s.html" % key), "w", encoding="utf-8").write(html)
print("wrote", len(V), "budget OG templates")
