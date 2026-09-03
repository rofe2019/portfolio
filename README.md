# Rafah Al Kassar — Portfolio

Static portfolio site (no build step for the site itself). Home page plus one detail page per project.

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Or open `index.html` directly in a browser / use the VS Code Live Server extension.

## Editing projects

All project content lives in `tools/projects.json` (title, tagline, category, tech tags, icon, screenshots, store/demo links, description). After editing it, regenerate the HTML:

```bash
pip install pillow   # once
python3 tools/build.py
```

This rewrites `index.html` and every `landingN.html` from the shared template in `tools/build.py`.
Site-wide copy (hero, services, skills, contact) is at the top of `tools/build.py`.

## Structure

- `assets/css/site.css` — design system (dark theme, gradients, components, responsive rules)
- `assets/js/site.js` — nav, scroll reveal, project filters, lightbox
- `assets/css/fontawesome-all.min.css` + `assets/webfonts/` — icons
- `assets/icons-ai/` — AI tool logos
- project folders (`flikk/`, `mrb/`, `dgold/`, …) — screenshots and icons
