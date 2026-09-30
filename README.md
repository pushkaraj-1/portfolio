# pushkaraj.dev

Personal portfolio of **Pushkaraj Baradkar** — MS Computer Science @ USC Viterbi.

Static HTML/CSS/JS. No framework, no build step required to view or deploy.

## Run it locally

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

That's it — no Ruby, no Node, no dependencies.

## Editing content

All text lives in two Python files, so you never hand-edit nine HTML files to
change one sentence:

| File | Contains |
| --- | --- |
| `tools/content.py` | Name, bio, resume links, experience, education, skills, research, activities, awards |
| `tools/projects_data.py` | The eight projects — title, tagline, tags, links, and full page body |

After editing either, regenerate:

```bash
python3 tools/build_site.py
```

This rewrites `index.html`, the section pages, `projects/*.html`, and
`search-index.json`.

You *can* edit the generated `.html` directly — it is plain HTML — but running
the build again will overwrite it. For anything you want to keep, edit the
Python.

## Layout

The homepage is a two-column `page-layout`:

```
main.page-layout
├── .sidebar     profile · news · service & activities · selected projects
└── .content     experience · research & publications · skills · education
```

```
index.html            Two-column homepage
experience.html       Full role detail + awards
projects.html         All projects, grouped by category
projects/<slug>.html  One page per project, with diagrams and results
skills.html           Full stack
education.html        Degrees and coursework
activities.html       Service and activities
styles.css            Ported layout + an "Additions" block at the foot
script.js             Theme toggle, mobile nav, scroll-cards, search
search-index.json     Generated search index
```

`styles.css` is the reference layout's stylesheet, unmodified, with every
site-specific rule appended in the clearly-marked **Additions** block at the
end. Keeping that split means the base can be re-synced without losing custom
work.

## Adding your files

See **[ASSETS.md](ASSETS.md)** for exactly where photos, logos, the resume, and
project screenshots go.

## Diagrams

The architecture diagrams and result plots are generated SVG:

```bash
cd tools
python3 gen_arch.py && python3 gen_arch2.py && python3 gen_plots.py && python3 gen_pub.py
python3 check_bounds.py     # verifies nothing overflows its canvas
```

## Checks

With the local server running:

```bash
python3 tools/check_pages.py
```

Loads every page in a headless browser and reports broken images, dead internal
links, JS errors, and horizontal overflow at 320–1440px.

## Deploying

Pushing to `main` publishes via `.github/workflows/deploy.yml` (GitHub Pages,
static upload). Enable Pages → Source → **GitHub Actions** in repo settings.
