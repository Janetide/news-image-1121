# The World in One Page — 21 November 2026

![Date](https://img.shields.io/badge/date-21_Nov_2026-red)
![Stories](https://img.shields.io/badge/stories-43-blue)
![Size](https://img.shields.io/badge/image-1024x1024-green)

One image summing up the world's news of Saturday 21 November 2026:
3 illustrated headlines, 10 illustrated story cards, a numbered world map,
region stats, a numbers bar, a UTC timeline and 30 illustrated briefs —
43 stories in all, every one with its own drawn picture.

## How it is built

`draw_news.py` draws the whole front page with Pillow only (no photos, no
network, deterministic bytes). `main.ts` copies the resulting `entry.png`
to the grader's output directory and verifies the copy with sha256.

```sh
python3 draw_news.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Al Jazeera, BBC, Guardian, Reuters, UPI, DW, CBC, France 24 and others —
reports of 21 Nov 2026, checked 22 Nov 2026.

## License

MIT — see `LICENSE`.
