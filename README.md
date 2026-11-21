# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Raafi1234/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Raafi1234/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for make.fun **news-image-20261120**: one image that sums up the world's news of Friday, 20 November 2026.

## Run it

```sh
make run
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=waxf8q9w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>

## The World in One Day — Friday, 20 November 2026

A newspaper front page summing up the world's news of Friday, 20 November 2026, for the make.fun `news-image-20261120` competition.

**Headline story:** Russian missiles and a jet drone enter Polish airspace during a massive attack on Ukraine — Warsaw calls it a deliberate provocation. Also inside: the global market sell-off, the Houthi missile strike on Riyadh's PIF Tower, the US Senate's blocked Iran war-powers vote, COP31 running into overtime, and GTA VI's record $3.79bn first day.

## How it is made

`compose.py` (Pillow) draws the whole front page: the masthead, headlines and captions are all set programmatically, and the six panel illustrations in `panels/` (flat editorial artwork, no text inside them) are placed into the layout. The result is `entry.png` (1024×1024). `main.ts` (Node 22, standard library only) copies that image to the output directory.

See `NEWS.md` for the researched stories and their sources.

This builds `entry.png` and copies it to `out/entry.png`, the same way the grader runs the entry. `make check` additionally verifies the output size and that both copies are byte-identical.

## License

MIT — see `LICENSE`.
