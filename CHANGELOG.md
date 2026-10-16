# Changelog

## v0.2.0 — 2026-10-17
### Changed
- Removed 確認問題 / 類題 and grading from the whole flow. Weaknesses are now tracked from the student's own questions and self-reports.
- Video structure is now 0–3 s hook / 3–27 s three steps / 27–30 s summary.
- Renamed ショート監督bot → Explainer Video bot (`bots/explainer-video.md`, placeholder `<EXPLAINER_VIDEO_BOT_ID>`).
- Notion template: 「弱点単元と次の出し直し日」→「弱点単元」.
- Updated bots/, docs/architecture.md (flowchart), docs/notion-student-template.md, README.md, README.ja.md.
### Added
- `renderer/`: template-based video renderer prototype (JSON spec → mp4, no LLM) with sample specs and outputs.
  (the 確認問題 scene is not included)

## v0.1.0
- Initial 5-bot StudyStudio team.
