# -*- coding: utf-8 -*-
"""Build nightlife-budget.html in 5 languages from a shared template."""
import io, json, os, re, sys

ROOT = r"C:\Users\kango\bangkok-nightlife-guide"
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://bangkoknightguide.com"

# Reuse the exact stylesheet of the existing guide page so the design matches.
src = io.open(os.path.join(ROOT, "japanese-kyabakura.html"), encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

# ...but the body font stack has to follow the page language, not Japanese everywhere.
JA_STACK = ('font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", '
            '"Yu Gothic", "Meiryo", sans-serif')
STACK = {
    "en":      'font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif',
    "ja":      JA_STACK,
    "ko":      'font-family: -apple-system, "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", sans-serif',
    "zh-Hans": 'font-family: -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif',
    "zh-Hant": 'font-family: -apple-system, "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif',
}
assert JA_STACK in CSS, "source stylesheet no longer carries the expected Japanese stack"

DIRS   = {"en": "en", "ja": "ja", "ko": "ko", "zh-Hans": "zh", "zh-Hant": "zh-Hant"}
LOCALE = {"en": "en_US", "ja": "ja_JP", "ko": "ko_KR", "zh-Hans": "zh_CN", "zh-Hant": "zh_TW"}
LANGBAR = [("en", "EN"), ("ja", "JA"), ("ko", "KO"), ("zh-Hans", "ZH"), ("zh-Hant", "\u7e41")]
# page key -> output filename; content lives in content/<key>/<lang>.json
PAGES = {"budget": "nightlife-budget.html", "scams": "nightlife-scams.html"}
KEY = os.environ.get("PAGE_KEY", "budget")
PAGE = PAGES[KEY]
PUBLISHED = "2026-09-02"
MODIFIED  = "2026-09-02"

def url(lang):
    return "%s/%s/%s" % (SITE, DIRS[lang], PAGE)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def hreflangs(cur):
    out = []
    for lang in ["en", "ja", "ko", "zh-Hans", "zh-Hant"]:
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (lang, url(lang)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">' % url("en"))
    return "\n".join(out)

def langbar(cur):
    rows = []
    for lang, label in LANGBAR:
        cls = ' class="active"' if lang == cur else ""
        rows.append('    <a href="/%s/%s"%s>%s</a>' % (DIRS[lang], PAGE, cls, label))
    return "\n".join(rows)

def price_grid(items, total):
    out = ['      <div class="price-grid">']
    for label, value in items:
        out.append('        <div class="price-card">')
        out.append('          <div class="price-card-label">%s</div>' % label)
        out.append('          <div class="price-card-value">%s</div>' % value)
        out.append("        </div>")
    out.append('        <div class="price-card price-card-total" style="grid-column: 1 / -1;">')
    out.append('          <div class="price-card-label">%s</div>' % total[0])
    out.append('          <div class="price-card-value">%s</div>' % total[1])
    out.append("        </div>")
    out.append("      </div>")
    return "\n".join(out)

def compare_table(head, rows):
    out = ['      <div class="compare-wrap">', '      <table class="compare">', "        <thead><tr>"]
    for h in head:
        out.append("          <th>%s</th>" % h)
    out.append("        </tr></thead>")
    out.append("        <tbody>")
    for r in rows:
        out.append("          <tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>")
    out.append("        </tbody>")
    out.append("      </table>")
    out.append("      </div>")
    return "\n".join(out)

def faq_html(faqs):
    out = []
    for q, a in faqs:
        out.append('      <div class="faq-item">')
        out.append('        <button class="faq-question" aria-expanded="false" '
                   'onclick="var o=this.parentElement.classList.toggle(&#39;open&#39;);'
                   'this.setAttribute(&#39;aria-expanded&#39;,o)">')
        out.append("          %s" % q)
        out.append("        </button>")
        out.append('        <div class="faq-answer">')
        out.append("          %s" % a)
        out.append("        </div>")
        out.append("      </div>")
        out.append("")
    return "\n".join(out)

def build(lang):
    c = json.load(io.open(os.path.join(HERE, "content", KEY, lang + ".json"), encoding="utf-8"))
    u = url(lang)
    og = "%s/assets/og/og-%s-%s.png" % (SITE, KEY, lang)
    # the English home lives at the site root; /en/ is only a duplicate
    home = "/" if lang == "en" else "/%s/" % DIRS[lang]

    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                       for q, a in c["faq"]]}
    article_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": c["title"], "description": c["description"], "url": u,
        "inLanguage": lang, "datePublished": PUBLISHED, "dateModified": MODIFIED,
        "publisher": {"@type": "Organization", "name": "Bangkok Night Guide", "url": SITE,
                      "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.svg",
                               "width": 600, "height": 150}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": u},
        "about": [{"@type": "Place", "name": "Sukhumvit Soi 23",
                   "address": {"@type": "PostalAddress", "addressLocality": "Bangkok",
                               "addressCountry": "TH"}}]}
    crumb_ld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c["crumb_home"], "item": SITE + home},
            {"@type": "ListItem", "position": 2, "name": c["crumb_self"]}]}

    def ld(obj):
        return ('<script type="application/ld+json">\n%s\n</script>'
                % json.dumps(obj, ensure_ascii=False, indent=2))

    toc = "\n".join('        <li><a href="#%s">%s</a></li>' % (i, t) for i, t in c["toc"])
    models = "\n".join(
        '      <div class="price-card" style="text-align:left;margin-bottom:14px;">\n'
        '        <div class="price-card-label">%s</div>\n'
        '        <div class="price-card-value" style="margin-bottom:8px;">%s</div>\n'
        '        <p style="margin:0;font-size:15px;">%s</p>\n'
        "      </div>" % (m[0], m[1], m[2]) for m in c["models"])
    hidden = "\n".join("        <li><strong>%s</strong>%s%s</li>"
                       % (h[0], c["sep"], h[1]) for h in c["hidden"])
    tips = "\n".join("        <li><strong>%s</strong>%s%s</li>"
                     % (t[0], c["sep"], t[1]) for t in c["tips"])

    html = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">

<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{hreflang}

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Bangkok Night Guide">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogalt}">
<meta property="og:locale" content="{locale}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{ogalt}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">

<!-- Structured Data: Article -->
{article_ld}

<!-- Structured Data: BreadcrumbList -->
{crumb_ld}

<!-- Structured Data: FAQPage -->
{faq_ld}

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-L3F0B833S2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-L3F0B833S2');
</script>
<style>{css}</style>
</head>
<body>

<!-- Language Bar -->
<div class="lang-bar">
  <div class="lang-bar-inner">
{langbar}
  </div>
</div>

<!-- Header -->
<header>
  <div class="header-inner">
    <a class="site-logo" href="{home}">Bangkok <span>Night</span> Guide</a>
    <nav class="header-nav">
      <a href="{home}">{nav_guide}</a>
      <a href="{kyabakura}">{nav_kyaba}</a>
      <a href="/{dir}/nightlife-budget.html">{nav_budget}</a>
      <a href="/{dir}/nightlife-scams.html">{nav_scams}</a>
    </nav>
  </div>
</header>

<!-- Hero -->
<div class="hero">
  <div class="hero-inner">
    <div class="hero-breadcrumb">
      <a href="{home}">{crumb_home}</a> <span>&rsaquo;</span>
      {crumb_self}
    </div>
    <div class="hero-category">{hero_category}</div>
    <h1>{h1}</h1>
    <p class="hero-sub">{hero_sub}</p>
    <div class="hero-meta">
      <div class="hero-meta-item">&#128176; <strong>{meta_1}</strong></div>
      <div class="hero-meta-item">&#128197; <strong>{meta_2}</strong></div>
      <div class="hero-meta-item">&#128205; <strong>{meta_3}</strong></div>
    </div>
  </div>
</div>

<!-- Main Content -->
<div class="page-wrap">
  <div class="article-body">

    <!-- TOC -->
    <div class="toc-box fade-in">
      <div class="toc-label">{toc_label}</div>
      <ol>
{toc}
      </ol>
    </div>

    <!-- Section: Answer -->
    <section id="answer" class="fade-in">
      <h2>{h_answer}</h2>
      <p>{p_answer}</p>
{answer_grid}
      <p>{note_answer}</p>
    </section>

    <!-- Section: Breakdown -->
    <section id="breakdown" class="fade-in">
      <h2>{h_breakdown}</h2>
      <p>{p_breakdown}</p>
{breakdown_grid}
      <p>{note_breakdown}</p>
    </section>

    <!-- Section: Models -->
    <section id="models" class="fade-in">
      <h2>{h_models}</h2>
      <p>{p_models}</p>
{models}
    </section>

    <!-- Section: Hidden costs -->
    <section id="hidden" class="fade-in">
      <h2>{h_hidden}</h2>
      <p>{p_hidden}</p>
      <ol class="numbered-list">
{hidden}
      </ol>
    </section>

    <!-- Section: Tips -->
    <section id="save" class="fade-in">
      <h2>{h_save}</h2>
      <p>{p_save}</p>
      <ol class="numbered-list">
{tips}
      </ol>
    </section>

    <!-- Section: Compare -->
    <section id="compare" class="fade-in">
      <h2>{h_compare}</h2>
      <p>{p_compare}</p>
{compare}
      <p>{note_compare}</p>
    </section>

    <!-- Section: FAQ -->
    <section id="faq" class="fade-in">
      <h2>{h_faq}</h2>

{faq}
    </section>

    <!-- CTA -->
    <div class="final-cta fade-in">
      <div class="final-cta-eyebrow">Club LINE23</div>
      <h2>{cta_h}</h2>
      <p>{cta_p}</p>
      <a href="https://clubline23-bangkok.com/" target="_blank" rel="noopener noreferrer" class="btn-line" style="margin-right:8px;">{cta_site}</a>
      <a href="https://line.me/R/ti/p/@624xdwsf" target="_blank" rel="noopener noreferrer" class="btn-line">{cta_line}</a>
    </div>

  </div>
</div>

<!-- Footer -->
<footer>
  <div class="footer-inner">
    <div>
      <div class="footer-logo">Bangkok <span>Night</span> Guide</div>
    </div>
    <div class="footer-text">
      {footer}
    </div>
  </div>
</footer>

<!-- IntersectionObserver fade-in -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
  var targets = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function(entries) {{
      entries.forEach(function(e) {{
        if (e.isIntersecting) {{ e.target.classList.add('visible'); io.unobserve(e.target); }}
      }});
    }}, {{ threshold: 0.08 }});
    targets.forEach(function(t) {{ io.observe(t); }});
  }} else {{
    targets.forEach(function(t) {{ t.classList.add('visible'); }});
  }}
}});
</script>
</body>
</html>
""".format(
        lang=lang, title=esc(c["title"]), description=esc(c["description"]),
        keywords=esc(c["keywords"]), url=u, hreflang=hreflangs(lang), og=og,
        ogalt=esc(c["og_alt"]), locale=LOCALE[lang],
        article_ld=ld(article_ld), crumb_ld=ld(crumb_ld), faq_ld=ld(faq_ld),
        css=CSS.replace(JA_STACK, STACK[lang]), langbar=langbar(lang), home=home,
        dir=DIRS[lang], nav_budget=c["nav_budget"], nav_scams=c["nav_scams"],
        kyabakura=("/japanese-kyabakura.html" if lang == "ja"
                   else "/%s/japanese-kyabakura.html" % DIRS[lang]),
        nav_guide=c["nav_guide"], nav_kyaba=c["nav_kyaba"],
        crumb_home=c["crumb_home"], crumb_self=c["crumb_self"],
        hero_category=c["hero_category"], h1=c["h1"], hero_sub=c["hero_sub"],
        meta_1=c["meta"][0], meta_2=c["meta"][1], meta_3=c["meta"][2],
        toc_label=c["toc_label"], toc=toc,
        h_answer=c["h_answer"], p_answer=c["p_answer"],
        answer_grid=price_grid(c["answer_cards"], c["answer_total"]), note_answer=c["note_answer"],
        h_breakdown=c["h_breakdown"], p_breakdown=c["p_breakdown"],
        breakdown_grid=price_grid(c["breakdown_cards"], c["breakdown_total"]),
        note_breakdown=c["note_breakdown"],
        h_models=c["h_models"], p_models=c["p_models"], models=models,
        h_hidden=c["h_hidden"], p_hidden=c["p_hidden"], hidden=hidden,
        h_save=c["h_save"], p_save=c["p_save"], tips=tips,
        h_compare=c["h_compare"], p_compare=c["p_compare"],
        compare=compare_table(c["compare_head"], c["compare_rows"]),
        note_compare=c["note_compare"],
        h_faq=c["h_faq"], faq=faq_html(c["faq"]),
        cta_h=c["cta_h"], cta_p=c["cta_p"], cta_site=c["cta_site"], cta_line=c["cta_line"],
        footer=c["footer"])

    out = os.path.join(ROOT, DIRS[lang], PAGE)
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    return out, len(html)

if __name__ == "__main__":
    for lang in sys.argv[1:]:
        p, n = build(lang)
        print("built %-46s %6d bytes" % (p, n))
