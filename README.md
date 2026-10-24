# AlsonEntuna.github.io
My personal portfolio website: [alsonentuna.github.io](https://alsonentuna.github.io/)

Plain HTML and CSS, with no framework and no build step. GitHub Pages serves this repo as-is.

## Structure
- `*.html`: one file per page. The header and footer are repeated at the top and bottom of each page, so update them in every file when you change them.
- `assets/css/site.css`: all styles. Colors, spacing and type sizes are variables at the top, with a dark theme below them.
- `assets/js/site.js`: theme toggle, mobile menu, scroll reveal and gallery lightbox.
- `assets/img/`: optimized WebP images used by the pages.
- `tools/images.py`: image helper (see below).

## Editing
1. Edit the HTML/CSS.
2. Preview locally: `python -m http.server 8000`, then open http://localhost:8000
3. Commit and push to `master`. GitHub Pages deploys automatically.

## Adding images
```
pip install pillow
python tools/images.py convert path/to/photo.jpg   # writes assets/img/photo.webp (+ photo-600.webp)
python tools/images.py annotate                    # fills in width/height/srcset on <img> tags
```
Then reference it as `<img src="assets/img/photo.webp" alt="..." loading="lazy">`.
