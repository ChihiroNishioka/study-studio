# Architecture

```mermaid
flowchart TD
    S[生徒<br>Grok Botチャットで問題の写真を送る] --> T[担任bot先生<br>問題を受け付けて弱点を確認し、依頼票を作る]
    N[(Notion<br>生徒ごとのページ<br>高2数学・高2物理・中1数学)] <--> T
    T -->|依頼票：問題・単元・弱点| A[受験問題解答bot<br>解答・方針・確認問題を作る]
    A --> C[構成作家bot<br>30秒の台本と絵コンテ]
    C --> R{受験問題解説レビューbot<br>正しさ50点＋分かりやすさ50点}
    R -->|計算ミス| A
    R -->|80点未満| C
    R -->|3回だめ| U[bot管理者に相談]
    R -->|80点以上| D[ショート監督bot<br>1080×1920・30秒<br>駅の案内サイン風]
    D -->|動画| T
    T -->|動画と確認問題| S
    S -->|生徒の答え| T
    T -->|採点（記録しない）| S
    T -->|質問の履歴・間違え方・弱点単元・最後に解いた日を記録| N
```

Hand-offs between bots use Grok Bot agent-to-agent messages (SendToAgent). Student data lives in Notion (one page per student). Videos are rendered on the bot box with Manim + ffmpeg.
