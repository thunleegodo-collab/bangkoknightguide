# tools — ページ生成スクリプト

このディレクトリのスクリプトが、5言語ページとOG画像の**生成元**です。
`/xx/nightlife-budget.html`・`/xx/nightlife-scams.html` の10ページと、各indexのエリアマップは
手書きではなくここから生成されています。**内容を直すときはHTMLではなくこちらを直して再生成してください。**
HTMLを直接編集すると、次回の再生成で上書きされます。

実行にはPython 3と、OG画像生成のみヘッドレスEdge（またはChrome）が必要です。

## build_pages.py — 予算ガイド／トラブル回避ガイド（5言語×2種）

文面・金額・FAQはすべて `content/<ページ>/<言語>.json` にあります。
HTMLの雛形（レイアウト・構造化データ・ナビ）はスクリプト側です。
CSSは `japanese-kyabakura.html` の `<style>` を読み込んで流用し、body のフォントスタックだけ
言語別に差し替えています（韓国語・中国語ページに日本語専用フォントを当てないため）。

```bash
PAGE_KEY=budget python -X utf8 tools/build_pages.py en ja ko zh-Hans zh-Hant
PAGE_KEY=scams  python -X utf8 tools/build_pages.py en ja ko zh-Hans zh-Hant
```

言語コードと出力先の対応は `DIRS`（`zh-Hans` → `/zh/`、`zh-Hant` → `/zh-Hant/`）。
`PUBLISHED` / `MODIFIED` が構造化データの日付になるので、内容を更新したら `MODIFIED` を上げ、
`sitemap.xml` の `lastmod` も合わせてください。

金額を直すときの注意：予算ガイドの数字は「1人あたり・ドリンク込み・サービス料10%＋VAT7%込み・
夕食と移動は別」という単一の前提で揃えてあり、モデルコースの本文には計算過程が書いてあります。
どれか1つを変えると他と食い違うので、`QA_CHECKLIST.md` の料金の項を読んでから触ってください。

## area_map.py — 各indexのエリアマップ（5言語）

`#area` セクションの導入文直後にインラインSVGを挿入し、CSSを `<style>` に足します。
**挿入済みのページに再実行しても二重挿入はされません**（`area-map-wrap` の有無で判定）。
作り直したい場合は先に該当ページの図とCSSを消してから実行してください。

```bash
python -X utf8 tools/area_map.py
```

ラベルは `L` 辞書、座標はviewBox `0 62 800 424` 上の直接指定です。
徒歩分数はサイト本文の記載（ソイカウボーイ3分・ソイ23周辺5分・Club LINE23 7分）と一致させること。

レイアウト上の注意が2つあります。どちらも実測で確認した挙動です。

- 記事カラム `main.article-body` はCSS Gridのアイテムなので、自動最小サイズが min-content 幅になります。
  地図の `min-width` がそこを押し上げてページ全体を横に広げるため、
  `.content-grid > .article-body { min-width: 0 }` が必須です。これを外すと最大270px横溢れします。
- 記事カラムの幅はサイドバー表示時522px・1カラム時629pxが上限で、地図の660pxはどの画面幅でも収まりません。
  そのため横スクロールの示唆（右端フェード＋キャプション先頭のヒント）は**常時表示**にしてあります。
  メディアクエリで隠すと、PC表示で Club LINE23 のラベルが黙って切れます。

## og_gen.py / og_gen_scams.py — OG画像

1200×630のPNGを `assets/og/` に出力します。`og_gen_scams.py` は `og_gen.py` のテンプレートを読み込むので、
デザインを変えるときは `og_gen.py` 側のTPLを直してください。

```bash
python -X utf8 tools/og_gen.py          # HTMLテンプレートを書き出す
# 各テンプレートをヘッドレスブラウザで1200x630でスクリーンショット → assets/og/*.png
```

スクリーンショットの実行例（PowerShell、Edge）:

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
& $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 `
        --window-size=1200,630 --screenshot="assets\og\og-budget-ja.png" "file:///…/og-budget-ja.html"
```

フォントは各言語で指定を分けています（日本語=Noto Sans JP系、簡体字=PingFang SC系、繁体字=PingFang TC系）。
ここを共通化すると中国語字形が日本語ページに混入するので、統一しないでください。
