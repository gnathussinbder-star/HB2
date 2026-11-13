# Hussein Badr English

Free, static, Arabic-first English learning platform (A1 → C1). No build step, no backend: plain HTML/CSS/JS, deployable on GitHub Pages. Progress is stored locally in the browser.

Live: https://gnathussinbder-star.github.io/Hussien-/ · Arabic docs: [README.ar.md](README.ar.md)

## Structure
```
index.html, lessons.html, ...   main pages (+ lesson-*.html, 18 lessons)
grammar.html  grammar/          12 grammar topics
vocabulary.html  vocabulary/    10 vocabulary topics (12 words each)
levels.html  levels/            CEFR level guides A1–C1
assets/css, assets/js, assets/img
sw.js, manifest.webmanifest     offline support / PWA
tools/validate.py               link, asset, sitemap and SEO checks
docs/placement-notes.md         notes on the placement test
```

## Develop
```
python3 -m http.server 8000     # open http://localhost:8000
python3 tools/validate.py       # must print OK before publishing
```
Brand colors: navy `#102B4C`, yellow `#FFD447`, support blue `#7598BD`, pale `#F5F7FA`.

© 2026 Hussein Badr. All rights reserved (see LICENSE).
