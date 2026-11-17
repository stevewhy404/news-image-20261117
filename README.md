[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/stevewhy404/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/stevewhy404/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

# The World Today — 17 November 2026

A program that draws a newspaper front page summing up the world news of
Tuesday, 17 November 2026, as a single 1024×1024 image — for the
[make.fun](https://make.fun/bounty/news-image-20261117) competition
`news-image-20261117`.

`main.py` (Python 3.13, standard library only) draws the page pixel by
pixel with an embedded 5×7 bitmap font and a hand-rolled PNG encoder:
no network, no fonts on disk, fully deterministic — two runs write
byte-identical `entry.png` files.

Stories covered: the Kerch Bridge strike and the Kyiv bridge attacks;
tankers mined near the Strait of Hormuz as a third US carrier arrived;
Trump's Asia trip ahead of APEC and planned talks with Xi and Putin;
five EU states planning a Rwanda return hub; the JPMorgan banking
outage; and the failed ULA Vulcan launch that destroyed 40 Amazon
satellites. Sources: BBC, Al Jazeera, Reuters, AP, Spaceflight Now.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
