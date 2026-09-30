# Where to put your files

Everything the site displays lives under `assets/`. Drop files at these exact
paths and they appear automatically — no code changes needed.

## Your photo

| Path | What it is |
| --- | --- |
| `assets/img/profile.jpg` | Hero photo, top of the homepage. Square crop, at least 600×600. JPG or PNG. |

## Resume

| Path | What it is |
| --- | --- |
| `assets/resume/resume.pdf` | The file the **Download resume** button serves. Overwrite it to update. |

The **View resume** button opens a Google Drive link instead — that lives in
`_data/site.yml` as `resume_view_url`, not in this folder.

## Company & organisation logos

Square logos, 128×128 or larger, transparent PNG or SVG. Used beside each
experience entry and each activity.

| Path | Where it shows |
| --- | --- |
| `assets/img/logos/tabhi.png` | Experience — Tabhi |
| `assets/img/logos/usc.png` | Experience — USC (also USC mentorship) |
| `assets/img/logos/ymt-medical.png` | Experience — YMT Medical |
| `assets/img/logos/technoriya.png` | Experience — Technoriya ERP |
| `assets/img/logos/rotaract.png` | Activities — Rotaract Club |
| `assets/img/logos/mumbai.png` | Education — University of Mumbai |

Adding a new organisation? Drop the logo here and reference it by filename in
the matching entry in `_data/cv.yml` or `_data/activities.yml`.

## Project images

One folder per project. Anything you drop in is available to that project's page.

| Folder | Project |
| --- | --- |
| `assets/img/projects/hvac/` | HVAC Follow-up Policy Optimization |
| `assets/img/projects/travel-agent/` | Eval-Gated Skill Development |
| `assets/img/projects/agentpay/` | AgentPay |
| `assets/img/projects/image-rag/` | Hierarchical Multimodal Image RAG |
| `assets/img/projects/infodistill/` | InfoDistill |
| `assets/img/projects/nei-slam/` | Real-Time Visual SLAM |
| `assets/img/projects/godot-mcp/` | Godot MCP |
| `assets/img/projects/defillama/` | DefiLlama SDK |

Useful things to add per project: `screenshot.png` (a real UI shot),
`demo.gif` (short screen capture), `result.png` (a plot or output figure).

To use one on the page, reference it from that project's markdown in
`_projects/`, e.g.:

```html
<img src="/assets/img/projects/hvac/screenshot.png" alt="...">
```

To make it the card thumbnail on the projects grid, set `img:` in that file's
front matter.

## Generated diagrams — do not edit by hand

| Path | What it is |
| --- | --- |
| `assets/img/diagrams/*.svg` | The 11 architecture diagrams and result plots. |

These are **generated**. Edit the Python in `tools/` and regenerate:

```bash
cd tools
python3 gen_arch.py && python3 gen_arch2.py && python3 gen_plots.py
python3 check_bounds.py        # verifies nothing overflows the canvas
```

Editing the `.svg` files directly means your changes are lost the next time
anyone regenerates.
