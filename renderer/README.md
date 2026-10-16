# Template renderer (prototype)

Renders a 30 s, 1080×1920, captions-only explainer video from a JSON spec — no LLM calls at render time. Intended for the Explainer Video bot so it no longer writes video code per problem.

- `schema.json` — spec format (title, problem, steps with heading/caption/formula/seconds, optional figure: `wave`, `point`, `graph`)
- `render.py` — `python3 render.py specs/doppler.json out.mp4` (needs Pillow, ffmpeg, Noto Sans CJK JP Bold)
- `check.py` — `python3 check.py spec.json out.mp4`: automatic checks (size, 30 s, text overflow)
- `specs/` — two examples (高2物理 ドップラー効果, 中1数学 一次方程式)
- `samples/` — rendered outputs

Status: prototype. Known gaps: the 「▶ いまここ」label is omitted; steps without a figure leave empty space; the intro is 4 s and the spec has no separate 27–30 s summary scene yet (target structure is 0–3 s hook / 3–27 s three steps / 27–30 s summary); the old 確認問題 scene has been removed from the renderer.
