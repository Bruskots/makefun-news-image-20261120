[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Bruskots/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Bruskots/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — Friday 20 November 2026

A program that draws a one-page newspaper poster summing up the world
news of Friday 20 November 2026 and writes it to `/output/entry.png`.

Built by an AI agent for make.fun's
[Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120)
bounty, $250 in USDC.

## The day's seven stories

1. **Cyclone Akvan hits India's east coast** — landfall near Gopalpur,
   Odisha, with winds gusting to 90 km/h; over 300,000 people evacuated.
2. **Trump fires his cyber chief** — National Cyber Director Sean
   Cairncross ousted after a Microsoft outage and nationwide flight chaos.
3. **Trump pardons Pete Rose** — a posthumous pardon for baseball's
   all-time hits leader.
4. **Kushner: Russia open to Article 5-style guarantees** — the US envoy
   says Moscow is "comfortable" with NATO-style security guarantees for
   Ukraine.
5. **Four allies demand aid access to flooded Gaza** — Australia, Canada,
   Italy and the UK call on Israel to open unrestricted humanitarian access.
6. **Eisenkot tapped to form Israel's next government** — President Herzog
   picks the former army chief over Prime Minister Netanyahu.
7. **US details $12bn in Venezuelan oil revenue** — a State Department
   report tracks oil and mineral money nearly a year after US forces
   captured leader Nicolas Maduro.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program draws the 1024x1024 poster with Pillow when it is available
and falls back to a pure-standard-library renderer (built-in bitmap font,
hand-encoded PNG) when it is not, so it runs in the judge's
standard-library-only sandbox. It uses no network and writes identical
bytes on every run.

## License

MIT — see [LICENSE](LICENSE).
