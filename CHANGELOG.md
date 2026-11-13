# Changelog

## 6.0 — 2026-11-13
### Fixed
- Missing `assets/` folder: 36 pages referenced icons that did not exist; images, CSS and JS now live in `assets/img|css|js`.
- Home page pointed to a PDF and cover image that were not in the repository; replaced with real course/guide links.
- `.grid-2` was never defined, so two-column sections stacked on desktop.
- Service worker: wrong paths, no offline page, cached failed responses; rewritten and registered from any folder depth.
- Mixed design systems (blue vs. navy/yellow brand); unified on the brand palette.
- Duplicate/stale files removed (3 Arabic READMEs, 2 manifests, snippet page, unused CSS/JS, duplicate logo).
- Sitemap listed 16 pages; now generated for all pages. 404 page got description and better links.
- Navigation overflow between 780–1100px; menu now collapses earlier and supports dark mode.
- Inline quiz feedback always wrote to the first quiz on a page.
### Added
- 12 grammar topics, 10 vocabulary topics, 5 level guides, glossary, accessibility statement, sitemap and offline pages.
- `tools/validate.py` and a GitHub Actions workflow that runs it.
