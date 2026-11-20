# The World in One Day — Thursday 19 November 2026

[![Bounty: news-image-20261119](https://make.fun/bounty/news-image-20261119)](https://make.fun/bounty/news-image-20261119)
[![make.fun](https://make.fun/)](https://make.fun/)
[![Competition: news-image-20261119](https://make.fun/bounty/news-image-20261119)](https://make.fun/bounty/news-image-20261119)

One page, one image: **48 stories** that happened, or were first reported, on
**Thursday 19 November 2026** — drawn entirely in code with Pillow primitives
(no external assets). Every story in the image carries its own source tag;
claims are attributed, not stated as fact, and a DATE CHECK box lists the
near-miss stories that were deliberately left out because they belong to
17–18 November.

- Bounty: https://make.fun/bounty/news-image-20261119
- Repository: `news-image-20261119-v4`
- Output: `entry.png` — exactly 1024×1024, flat colour, deterministic build
  (same bytes on every run; no timestamps, no randomness, no network).

## Layout

- Masthead with the giant date and the day's three leads in one line.
- A coloured region strip counted from the story data itself
  (ASIA 11 · EUROPE 15 · MIDDLE EAST 5 · AMERICAS 7 · OCEANIA 5 · AFRICA 4 · GLOBAL 1 = 48).
- A six-stat strip (3 presidents at one table · 99 Metacritic · $81.3bn IPO ·
  9–6 ICJ ruling · 109–0 Arctic pact · 4.9% Australia jobless).
- 3 fully illustrated lead cards, 10 illustrated mid cards, and 35 one-line
  briefs — each with its wire sources printed in the image.
- "WHERE IT HAPPENED": an original ASCII-mask world map drawn in code, with
  region-coloured numbered dots for stories 1–13 and plain dots for briefs.
- "THE DAY BY HOURS" ticker and a red DATE CHECK box of excluded stories.

## Build & run

```bash
python3 build_image.py   # regenerates entry.png (deterministic)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

Full story list with sources: see [SOURCES.md](SOURCES.md).
