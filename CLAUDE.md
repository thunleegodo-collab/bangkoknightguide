# Bangkok Night Guide (bangkoknightguide.com)

## プロジェクト目的
Club LINE23 Bangkok（clubline23-bangkok.com）への集客導線サイト。
バンコク・アソーク地区のナイトライフ情報を提供し、最終的にClub LINE23への外国人来店を最大化することがゴール。

## ビジネス構造
- **本サイト**: bangkoknightguide.com — SEO・SNS経由でナイトライフ情報を求める外国人を集客
- **導線先**: clubline23-bangkok.com — スクンビットSoi23の日本式キャバクラ（サンリー合同会社運営）
- Club LINE23の連絡先: LINE公式 @624xdwsf / TEL +66928302336
- 関連リポジトリ: club-line-bangkok（店舗サイト本体）

## ターゲットユーザー
- バンコク旅行を計画中 or 滞在中の外国人（日本人・韓国人・中国人・欧米人）
- グループ旅行者（男旅2〜6名）
- バンコク駐在員・出張者
- 初めてバンコクの夜遊びに行く層

## 技術構成
- 静的HTML（フレームワークなし）
- GitHub Pages でホスティング（CNAME: bangkoknightguide.com）
- リポジトリ: thunleegodo-collab/bangkoknightguide
- 4言語対応: 英語（ルート）、日本語（/ja/）、韓国語（/ko/）、中国語（/zh/）

## ページ構成
- `index.html` / `en/index.html` — アソーク夜遊びガイド（英語）
- `ja/index.html` — アソーク夜遊びガイド（日本語）
- `ko/index.html` — アソーク夜遊びガイド（韓国語）
- `zh/index.html` — アソーク夜遊びガイド（中国語）
- `japanese-kyabakura.html` — 日本人キャバクラガイド（日本語、各言語版あり）

## SEO対策
- hreflang タグで多言語対応
- 構造化データ（Article, LocalBusiness, FAQPage）実装済み
- Open Graph / Twitter Card 設定済み
- IndexNow APIキー設定済み
- sitemap.xml あり

## 編集時の注意事項
- 全ページでClub LINE23への自然な導線（リンク・レビュー・推奨）を維持すること
- 多言語ページは内容を同期させること（1言語を変更したら他も更新）
- 年号（2026等）は定期的に更新が必要
- LocalBusinessの構造化データでClub LINE23の情報を正確に保つこと
