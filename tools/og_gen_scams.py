# -*- coding: utf-8 -*-
import io, os, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
mod = runpy.run_path(os.path.join(HERE, "og_gen.py"))
FONTS, TPL = mod["FONTS"], mod["TPL"]

V = [
 ("scams-en","en",["Bangkok Nightlife","Avoiding Trouble"],"Scams, laws and how to spot a safe venue","FOUR THINGS TO KNOW"),
 ("scams-ja","ja",["バンコク夜遊び","トラブル回避"],"ぼったくり・法律・安全な店の見分け方","引っかかるのは4つだけ"),
 ("scams-ko","ko",["방콕 밤문화","트러블 예방"],"바가지 · 법률 · 안전한 업소 고르는 법","걸리는 건 네 가지뿐"),
 ("scams-zh-Hans","zh-Hans",["曼谷夜生活","避坑指南"],"宰客 · 法律 · 怎么分辨合法店家","会踩的就四个坑"),
 ("scams-zh-Hant","zh-Hant",["曼谷夜生活","避雷指南"],"敲竹槓 · 法律 · 怎麼分辨合法店家","會踩的就四個雷"),
]

for key, lang, lines, sub, tagline in V:
    longest = max(len(l) for l in lines)
    cjk = lang != "en"
    tsize = 78 if (cjk and longest <= 11) else 70 if cjk else (78 if longest <= 18 else 70)
    ssize = 30 if cjk else 31
    html = TPL.format(lang=lang, font=FONTS[lang], tsize=tsize, ssize=ssize,
                      titlehtml="".join("<span>%s</span>" % l for l in lines),
                      sub=sub, tagline=tagline)
    io.open(os.path.join(HERE, "og-%s.html" % key), "w", encoding="utf-8").write(html)
print("wrote", len(V), "scams OG templates")
