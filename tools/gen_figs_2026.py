"""Figure for the Sep 2026 dp-adult project (warp-tote uses its own report figures).

Run from tools/:  python3 gen_figs_2026.py
"""
import sys; sys.path.insert(0, ".")
from svglib import SVG, INK, MUTED, FAINT, MONO

OUT = "../assets/img/diagrams/"
IND="#6366f1"; TEAL="#0d9488"; VIO="#8b5cf6"; ROSE="#e11d48"; AMB="#d97706"
SKY="#0284c7"; SLATE="#64748b"; LIGHT="#94a3b8"

def head(s, t, sub):
    s.text(26, 32, t, size=14.5, weight=700, color=INK)
    s.text(26, 50, sub, size=11, color=MUTED, font=MONO)

def bars(s, rows, x0, y0, bw, rowh, vmax, fmt, gap=10):
    """Horizontal bars from zero; rows = [(label, value, color, bold)]."""
    for i, (lab, v, col, bold) in enumerate(rows):
        y = y0 + i * rowh
        w = max(bw * v / vmax, 2)
        s.rect(x0, y, w, rowh - gap, fill=col, stroke="none", rx=3, opacity=0.92 if bold else 0.45)
        ty = y + (rowh - gap) / 2 + 4
        s.text(x0 - 12, ty, lab, size=10.5, anchor="end", font=MONO,
               color=INK if bold else MUTED, weight=700 if bold else 400)
        s.text(x0 + w + 8, ty, fmt(v), size=10.5, font=MONO,
               color=INK if bold else MUTED, weight=700 if bold else 400)

# ------------------------------------------------------------ dp pipeline
s = SVG(900, 350)
head(s, "Three releases, one privacy budget",
     "30,162 census rows -> three diffprivlib mechanisms -> sequential composition")
s.node(26, 150, 130, 64, "Adult data", "30,162 rows", SLATE, mono=True, tsize=12)
tasks = [("count > $50K", "geometric, sens 1", SKY),
         ("top-3 occupations", "noisy hist + max", IND),
         ("logistic regression", "objective perturb.", VIO)]
for i, (t, sub, c) in enumerate(tasks):
    ty = 82 + i * 74
    s.path(f"M 156 182 C 190 182 190 {ty+28} 222 {ty+28}", stroke=FAINT)
    s.node(226, ty, 200, 56, t, sub, c, mono=True, tsize=12)
    s.arrow(426, ty + 28, 476, ty + 28, label="eps = 1")
    s.node(480, ty, 150, 56, "DP release", None, TEAL, mono=True, tsize=12)
    s.path(f"M 630 {ty+28} C 660 {ty+28} 660 182 688 182", stroke=FAINT)
s.node(692, 146, 182, 72, "BudgetAccountant", "total eps = 3.0", AMB, mono=True, tsize=12)
s.text(783, 244, "4th query refused", size=10.5, anchor="middle", font=MONO, color=ROSE, weight=600)
s.caption(26, 320, "public category list and schema-derived norm bounds: nothing about the data leaks through keys or bounds")
s.save(OUT + "dp-adult.svg", "DP releases under one budget")

print("1 figure written")
