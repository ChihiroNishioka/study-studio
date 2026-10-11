# StudyStudio（1問30秒動画工場）

**問題を撮って送るだけで、自分専用の30秒解説動画が届く。**
生徒の問題写真から、弱点に合わせた30秒の縦型解説動画と確認問題を作る、5体のGrok Botチーム。生徒ごとの記録が次の出題に反映されます。Grok Botハッカソン出品作品。

[English README](README.md)

## Demo / デモ動画

- [assets/demo-doppler.mp4](assets/demo-doppler.mp4) — 高2物理・ドップラー効果（救急車のサイレン）。レビュー点と確認問題は下の[デモ](#デモ)に書いてあります。
- [assets/demo-2.mp4](assets/demo-2.mp4) — 高校物理・左カーブ中のバスとヘリウム風船（慣性力と見かけの重力）。

## コンセプト
自主学習のとき、塾や学校の先生の代わりに教えるbotチーム。どこでつまずいたかを覚えて、パーソナライズしていきます。

## しくみ
1. 生徒がGrok Botチャットで担任bot先生に問題の写真を送る
2. 担任bot先生がNotionの生徒ページで弱点を確認し、依頼票を作る
3. 受験問題解答botが王道の解法で解き、検算し、確認問題を作る
4. 構成作家botが30秒の台本・絵コンテにする（弱点のステップを厚めに）
5. 受験問題解説レビューbotが採点（正しさ50点＋分かりやすさ50点）。80点以上で合格、計算ミスは解答botへ、80点未満は構成作家botへ差し戻し、3回だめならbot管理者に相談
6. ショート監督botが1080×1920・30秒・テロップのみ（音声なし）の動画を作る
7. 担任bot先生が動画を保存してNotionの生徒ページ（質問の履歴、間違え方、弱点単元、最後に解いた日）に記録し、動画を届けたあと確認問題を出してチャットで採点する。採点結果・正答率はNotionに記録しない

構成図：[docs/architecture.md](docs/architecture.md)

## 5つの役割（実際の職業になぞらえて）
| bot | 実際の職業 | プロンプト |
|---|---|---|
| 担任bot先生 | 塾のチューター・学習コーチ（自分では解かない、弱点と質問の履歴を管理） | [bots/tutor.md](bots/tutor.md) |
| 受験問題解答bot | 講師（解答・方針・確認問題） | [bots/solver.md](bots/solver.md) |
| 構成作家bot | 構成作家・放送作家（30秒の台本と絵コンテ） | [bots/scriptwriter.md](bots/scriptwriter.md) |
| 受験問題解説レビューbot | ディレクター・品質管理（正しさ50＋分かりやすさ50、80点以上で合格、3回だめで管理者へ） | [bots/reviewer.md](bots/reviewer.md) |
| ショート監督bot | ショート動画のディレクター兼編集者（1080×1920・30秒・テロップのみ） | [bots/short-director.md](bots/short-director.md) |

## 循環のしくみ
担任が弱点を見つける → 動画と確認問題に反映 → 質問の履歴がNotionに戻る → 次の出題が変わる。

## デザインガイド
駅の案内サイン風。白背景・太ゴシック・ステップごとに固定色（①赤 ②青 ③緑 ④オレンジ ⑤紫）、「▶ いまここ」の強調、セーフエリア。詳細は [docs/design-guide.md](docs/design-guide.md)。

![ドップラー効果のデモ動画（#7「遠ざかると？」）](assets/screenshot.png)

## デモ
[assets/demo-doppler.mp4](assets/demo-doppler.mp4)：高2物理・ドップラー効果（救急車のサイレン）。レビュー93点で合格、数値を変えた確認問題にチャットで正解、質問はNotionに記録。

## セットアップ
1. Grok Botを5体作り、`bots/` の各プロンプトを説明欄に貼る
2. プロンプト内のプレースホルダ（`<TUTOR_BOT_ID>` など）を実際のbot IDに置き換える
3. Notionを接続し、親ページ「学習支援チーム 生徒カルテ」と生徒ごとのページを [docs/notion-student-template.md](docs/notion-student-template.md) の形式で作り、`<NOTION_PARENT_PAGE_ID>`・`<NOTION_STUDENT_PAGE_ID_n>` を置き換える
4. （任意）Google Driveを接続し、保存フォルダを作って `<DRIVE_FOLDER_ID>` を置き換える
5. 担任bot先生に問題の写真を送る

## ロードマップ
- 入口の追加（家族向けiMessage、LINE、学校・塾）
- 生徒ページを増やして教科・学年を拡大
- ナレーション音声（任意）
- Notionデータを使った先生向けダッシュボード
- SNS配信用パイプライン

## ライセンス
MIT
