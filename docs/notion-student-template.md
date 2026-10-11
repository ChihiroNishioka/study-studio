# Notion student page template

Parent page: 「学習支援チーム 生徒カルテ」 (`<NOTION_PARENT_PAGE_ID>`). One child page per student (e.g. 高2数学, 高2物理, 中1数学 as initial sample students).

```markdown
# <学年><教科>  (e.g. 高2物理)
## 教科と学年
## 目標
## 間違え方の種類
- 計算ミス:
- 概念の誤解:
- 読み違い:
## 弱点単元と次の出し直し日
| 単元 | 次の出し直し日 |
## 質問の履歴
### <科目>
#### <単元>
- YYYY-MM-DD 問題の1行要約 — [フォルダ](...) [問題画像](...) [動画](...)
## 最後に解いた日
```

The tutor bot reads this page when a problem arrives and writes to it once per problem after the video is saved. Check questions (確認問題) are posted and graded in chat after the video, but scores / 正答率 are not stored in Notion.
