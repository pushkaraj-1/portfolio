import sys; sys.path.insert(0, ".")
from svglib import SVG, INK, MUTED, FAINT, GRID, MONO, SANS

OUT = "../project_images/diagrams/"
TEAL="#0d9488"; ROSE="#e11d48"; SLATE="#94a3b8"; IND="#6366f1"; AMB="#d97706"

def head(s, t, sub):
    s.text(26, 32, t, size=14.5, weight=700, color=INK)
    s.text(26, 50, sub, size=11, color=MUTED, font=MONO)

def hbar(s, rows, x0, y0, bw, rowh, vmin, vmax, unit="", gap=8):
    """Horizontal bars on a shared zero axis; rows = [(label, value, color, bold)].

    Value labels sit inside the bar when it is wide enough, so long bars never
    collide with the row-label gutter.
    """
    span = vmax - vmin
    zx = x0 + bw * (0 - vmin) / span
    s.line(zx, y0 - 8, zx, y0 + len(rows) * rowh + 2, stroke="#cbd5e1", sw=1)
    for i, (lab, v, col, bold) in enumerate(rows):
        y = y0 + i * rowh
        vx = x0 + bw * (v - vmin) / span
        left, w = min(zx, vx), abs(vx - zx)
        s.rect(left, y, max(w, 1.5), rowh - gap, fill=col, stroke="none", rx=3,
               opacity=0.95 if bold else 0.42)
        ty = y + rowh/2 - gap/2 + 3.5
        s.text(x0 - 14, ty, lab, size=10.5, anchor="end", font=MONO,
               color=INK if bold else MUTED, weight=700 if bold else 400)
        val = f"{v:+.2f}{unit}"
        inside = w >= 62
        if inside:
            tx = (vx - 9) if v >= 0 else (vx + 9)
            anc = "end" if v >= 0 else "start"
            colr = "#ffffff" if bold else MUTED
        else:
            tx = (vx + 8) if v >= 0 else (vx - 8)
            anc = "start" if v >= 0 else "end"
            colr = INK if bold else FAINT
        s.text(tx, ty, val, size=10.5, anchor=anc, font=MONO, color=colr,
               weight=700 if bold else 400)

# ----------------------------------------------------- HVAC policy comparison
s = SVG(900, 430)
head(s, "Offline policy comparison", "direct-method value per episode, held-out validation (5,000 episodes)")
rows = [
    ("distilled FQI + guardrails", 15.25, TEAL, True),
    ("hand-written rules",          4.35, SLATE, False),
    ("always_wait",                 1.10, SLATE, False),
    ("simple_rule (starter)",      -3.71, SLATE, False),
    ("always_park",                -8.79, SLATE, False),
    ("old policy (logged)",       -13.46, ROSE,  True),
    ("always_escalate",           -19.13, SLATE, False),
    ("always_check_in",           -19.58, SLATE, False),
    ("always_estimate_nudge",     -46.39, SLATE, False),
]
hbar(s, rows, x0=232, y0=86, bw=560, rowh=36, vmin=-50, vmax=20)
s.text(232, 412, "+28.7 per follow-up thread vs. the policy it replaces  -  DM, DR and SNIPS all agree on the ranking",
       size=10.5, color=FAINT, font=MONO)
s.save(OUT+"hvac-results.svg", "HVAC policy comparison")

# ----------------------------------------------------- SLAM ATE
s = SVG(900, 300)
head(s, "Trajectory error after factor-graph fusion", "absolute trajectory error, KITTI sequence 00, Umeyama-aligned")
x0, bw = 300, 470
s.line(x0, 96, x0, 214, stroke="#cbd5e1", sw=1)
for i,(lab, v, col, note) in enumerate([
        ("VO only (dead reckoning)", 95.0, ROSE, "scale drift accumulates"),
        ("+ sparse depth + GPS in GTSAM", 1.2, TEAL, "metric scale anchored")]):
    y = 104 + i*62
    w = bw * (v / 100.0)
    s.rect(x0, y, max(w, 3), 40, fill=col, stroke="none", rx=4, opacity=0.9)
    s.text(x0-12, y+25, lab, size=10.5, anchor="end", font=MONO,
           color=INK, weight=700 if i==1 else 400)
    s.text(x0+max(w,3)+10, y+25, f"~{v:g} m ATE", size=11.5, anchor="start",
           font=MONO, color=INK, weight=700)
    s.text(x0+max(w,3)+10, y+39, note, size=9.5, anchor="start", font=MONO, color=FAINT)
s.text(300, 250, "~79x reduction  -  running at 20-25 FPS on noisy indoor sequences",
       size=11, color=MUTED, font=MONO, weight=600)
s.text(300, 272, "loop factors contribute rotation only; translation stays with GPS and depth",
       size=10, color=FAINT, font=MONO)
s.save(OUT+"slam-results.svg", "SLAM trajectory error")

# ----------------------------------------------------- Travel agent lift
s = SVG(900, 300)
head(s, "Skill selection under Thompson sampling", "mean task score across the 466-task bank")
x0, bw = 250, 480
for i,(lab, v, col, note) in enumerate([
        ("uniform skill selection", 0.33, SLATE, "baseline router"),
        ("Thompson-sampling optimizer", 0.60, TEAL, "+0.27 mean score")]):
    y = 100 + i*66
    w = bw * v
    s.rect(x0, y, w, 42, fill=col, stroke="none", rx=4, opacity=0.9)
    s.text(x0-12, y+26, lab, size=10.5, anchor="end", font=MONO, color=INK,
           weight=700 if i==1 else 400)
    s.text(x0+w+10, y+26, f"{v:.2f}", size=12.5, anchor="start", font=MONO,
           color=INK, weight=700)
    s.text(x0+w+10, y+40, note, size=9.5, anchor="start", font=MONO, color=FAINT)
s.text(250, 248, "13.9K traces retired a router that was misrouting 35% of tasks",
       size=11, color=MUTED, font=MONO, weight=600)
s.text(250, 270, "top skill measured at +17 points with vs. without injection, at ~$0.03 per PR",
       size=10, color=FAINT, font=MONO)
s.save(OUT+"travel-agent-results.svg", "Thompson sampling lift")
print("3 result plots written")
