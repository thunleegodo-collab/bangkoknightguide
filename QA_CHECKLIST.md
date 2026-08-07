# QA_CHECKLIST — bangkok-nightlife-guide（bangkoknightguide.com 導線サイト）

qa-inspector / audit-reviewer がデプロイ・公開前に照合するプロジェクト固有正典。
共通規約は ~/.claude/CLAUDE.md 側でチェックされる前提。

## デプロイ前
- 5言語版（EN ルート＋/en/、/ja/、/ko/、/zh/ 簡体字、/zh-Hant/ 繁体字）の間で店舗情報・料金・リンク・ニュース内容が同期しているか（片言語だけの更新残りは🟡）
- 中国語は簡体字（/zh/）と繁体字（/zh-Hant/）が同期しているか（繁体字は s2twp 変換＋台湾語彙補正：包间→包廂、素坤逸/蘇坤蔚、评测→評測 等）
- clubline23-bangkok.com（本サイト）への導線リンクが生きているか（導線サイト→本サイトの方向は推奨。逆は本サイト側で禁止）
- 各言語の `lang` 属性が正しいか（en / ja / ko / zh-Hans / zh-Hant）
- hreflang が6種（en / ja / ko / zh-Hans / zh-Hant / x-default）相互参照になっているか
- 構造化データ（Article / LocalBusiness / FAQPage）の dateModified・店舗情報が更新内容と一致しているか
- コンテンツ更新時に sitemap.xml の lastmod も更新したか

## コンテンツ
- 店舗紹介の表現が誇大・断定になっていないか（事実ベース、体験は体験と明示）
- 経営者個人の本名・運営者情報の露出がないか
- 掲載店情報（営業時間・料金）の取得時点が古すぎないか（更新日明示を推奨）
- ニュース欄の「Last updated」日付が実際の更新日と一致しているか。規制・法令の記述は日付＋出典リンク付きで、推測を事実として書かないこと
- 年号（2026等）が古いまま残っていないか
