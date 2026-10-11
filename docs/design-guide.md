# Design guide — 駅案内サイン風 (station wayfinding style)

Every video looks the same so students instantly know where to look.

- Canvas: 1080×1920 (9:16), 28–30 s, captions only, no audio.
- Background: white. Text: bold black Japanese gothic (Noto Sans CJK JP Bold).
- Header: black bar with the title / question. Footer bar: 「次は ③ …」.
- Step colors (fixed, never change):
  | Step | Color | Hex |
  |---|---|---|
  | ① | red | `#E5322D` |
  | ② | blue | `#1E6FD9` |
  | ③ | green | `#1E9E4A` |
  | ④ | orange | `#F08C00` |
  | ⑤ | purple | `#8E44AD` |
- Steps drawn as a station-route diagram (① → ② → ③); diagrams/arrows use the step's color.
- Current step: yellow box marked 「▶ いまここ」; other steps greyed out.
- Opening 0–3 s: hook question in the header. Ending: summary listing all steps in their colors.
- Safe area: no text in the top/bottom ~10% or right ~12% (SNS UI overlays).
- Don't: gradients, glow, chalkboard or dark themes.

Example frame from the Doppler demo (#7, 「遠ざかると？」): [`assets/screenshot.png`](../assets/screenshot.png)
