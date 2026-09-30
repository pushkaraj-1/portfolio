"""Render every portfolio figure and table from results.json.

Usage (from this folder):  python make_figures.py

Writes each figure as PNG (300 dpi), SVG and PDF, each table as PNG + SVG,
and all tables as Markdown in tables.md. results.json holds the numbers
from the offline evaluator run on the held-out split (5,000 episodes).
"""
from __future__ import annotations

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "results.json")))

OURS, LOGGED, BASE = "#2a78d6", "#eb6834", "#9aa0a8"
INK, INK2, INK3, HAIR, PANEL = "#16191e", "#4a505a", "#7b818b", "#dde0e4", "#f1f3f5"
OURS_SOFT = "#e3eefb"

plt.rcParams.update({
    "font.family": "Helvetica Neue",
    "font.size": 9.5,
    "axes.edgecolor": INK3, "axes.linewidth": 0.8,
    "axes.labelcolor": INK2, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlecolor": INK, "axes.titlepad": 10,
    "xtick.color": INK3, "ytick.color": INK3,
    "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "xtick.major.size": 0, "ytick.major.size": 0,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": HAIR, "grid.linewidth": 0.8,
    "axes.axisbelow": True, "legend.frameon": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
MONO = "Menlo"


def save(fig, name, pdf=True):
    for ext in (["png", "svg", "pdf"] if pdf else ["png", "svg"]):
        fig.savefig(os.path.join(HERE, f"{name}.{ext}"), dpi=300, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("wrote", name)


def sgn(v, d=2):
    return ("+" if v > 0 else "−" if v < 0 else "") + f"{abs(v):.{d}f}"


# ---------------------------------------------------------------- Figure 1
def fig_system():
    fig = plt.figure(figsize=(10, 4.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 960); ax.set_ylim(430, 0); ax.axis("off")

    def node(x, y, w, h, title, lines, kind="plain"):
        fc, ec, ls = {"plain": ("white", INK3, "-"), "hl": (OURS_SOFT, OURS, "-"), "gate": (PANEL, INK3, "--")}[kind]
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=4",
                                    fc=fc, ec=ec, lw=1, ls=ls))
        ax.text(x + 11, y + 21, title, fontsize=9.5, fontweight="bold", color=INK, va="baseline")
        for i, ln in enumerate(lines):
            ax.text(x + 11, y + 40 + i * 15, ln, fontsize=7.8, family=MONO, color=INK2, va="baseline")

    def arrow(pts):
        xs, ys = zip(*pts)
        ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=INK2, lw=1.1, solid_capstyle="butt")
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.1, mutation_scale=9, shrinkA=0, shrinkB=0))

    def line(pts):
        xs, ys = zip(*pts); ax.plot(xs, ys, color=INK2, lw=1.1)

    band = dict(fontsize=7.8, color=INK3, fontweight="bold")
    ax.text(24, 24, "A · LEARN FROM LOGS  —  TRAIN SPLIT · 24,000 EPISODES · 74,733 STEPS", **band)
    xs = [24, 210, 396, 582, 768]
    node(xs[0], 38, 164, 88, "Logged transitions", ["(s, a, r, s′, π_β)", "old policy, 8 actions", "≤ 4 steps / episode"])
    node(xs[1], 38, 164, 88, "Feature encoder", ["31 features", "decision-time fields", "only (no leakage)"])
    node(xs[2], 38, 164, 88, "Fitted Q-Iteration", ["5 rounds, γ = 1", "boosted trees for", "Q(s,a), all 8 actions"])
    node(xs[3], 38, 164, 88, "Guardrail relabel", ["a* = argmax Q(s,·)", "rules override", "31.3% of labels"])
    node(xs[4], 38, 168, 88, "Distil to CART", ["depth 10, 148 leaves", "85.5% fidelity", "→ policy.py (stdlib)"], "hl")
    for a, b in zip(xs[:-1], xs[1:]):
        arrow([(a + 164, 82), (b - 1, 82)])
    arrow([(852, 126), (852, 158), (8, 158), (8, 256), (23, 256)])

    ax.text(24, 196, "B · EVALUATE OFF-POLICY  —  HELD-OUT SPLIT · 5,000 EPISODES · 15,565 STEPS", **band)
    node(24, 220, 164, 72, "Candidate π", ["guardrails first,", "then tree"], "hl")
    node(24, 310, 164, 72, "Held-out logs", ["never seen in", "training"])
    line([(188, 256), (218, 256)]); line([(188, 346), (218, 346)]); line([(218, 246), (218, 374)])
    for y in (246, 310, 374):
        arrow([(218, y), (249, y)])
    node(250, 220, 210, 52, "SNIPS", ["per step, weights clipped at 10"])
    node(250, 284, 210, 52, "Direct method (FQE)", ["model-based, per episode"])
    node(250, 348, 210, 52, "Doubly robust", ["FQE + importance correction"])
    for y in (246, 310, 374):
        line([(460, y), (486, y)])
    line([(486, 246), (486, 374)]); arrow([(486, 310), (515, 310)])
    node(516, 262, 196, 96, "Sanity gate", ["score π_β on its own logs", "truth −13.46, FQE −13.21", "pass: error 1.9%"], "gate")
    arrow([(712, 310), (739, 310)])
    node(740, 262, 196, 96, "Reported per policy", ["value per episode", "effective sample size", "95% bootstrap CI"])
    save(fig, "fig1_system_overview")


# ---------------------------------------------------------------- Figure 2
def fig_fatigue():
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.6), layout="constrained")
    fig.get_layout_engine().set(wspace=0.08)
    f = D["fatigue"]
    a.bar([f'{r["k"]}\nn={r["n"]:,}' for r in f], [r["v"] for r in f], width=0.55,
          color=[LOGGED if r["v"] > 10 else BASE for r in f])
    a.set_title("(a) Opt-out rate by messages already sent")
    a.set_xlabel("Messages already sent in this thread")
    pa = D["perAction"]
    b.bar([f'{r["k"]}\nn={r["n"]:,}' for r in pa], [r["v"] for r in pa], width=0.55,
          color=[LOGGED if r["v"] > 9 else BASE for r in pa])
    b.set_title("(b) Opt-out rate by action")
    b.tick_params(axis="x", labelsize=8)
    for ax, rows in ((a, f), (b, pa)):
        ax.set_ylim(0, 15.5); ax.set_yticks([0, 5, 10, 15]); ax.set_yticklabels(["0%", "5%", "10%", "15%"])
        ax.grid(axis="x", visible=False)
        for i, r in enumerate(rows):
            ax.text(i, r["v"] + 0.35, f'{r["v"]:.1f}%', ha="center", fontsize=8.5, family=MONO, color=INK)
    save(fig, "fig2_message_fatigue")


# ---------------------------------------------------------------- Figure 3
def fig_main():
    P = D["policies"]
    truth = next(p for p in P if p.get("logged"))["dm"]
    cands = [p for p in P if not p.get("logged")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 4.1), layout="constrained", gridspec_kw=dict(width_ratios=[1.15, 1]))

    ys = list(range(len(cands)))[::-1]
    for y, p in zip(ys, cands):
        col = OURS if p.get("ours") else BASE
        if p.get("ci"):
            a.plot(p["ci"], [y, y], color=col, lw=5, alpha=0.35, solid_capstyle="butt")
        a.plot(p["dm"], y, "o", ms=5.5 if p.get("ours") else 4.5, color=col, zorder=3)
        left = truth - 10 < p["dm"] < truth
        a.text(p["dm"] + (-1.4 if left else 1.4), y, sgn(p["dm"]), fontsize=7.8, va="center",
               family=MONO, color=INK if p.get("ours") else INK2, ha="right" if left else "left",
               fontweight="bold" if p.get("ours") else "normal")
    a.axvline(truth, color=LOGGED, lw=1.3, ls=(0, (4, 3)))
    a.text(truth - 0.8, len(cands) - 0.35, f"logged policy {sgn(truth)}", color=LOGGED, fontsize=7.8, ha="right")
    a.axvline(0, color=INK3, lw=0.8)
    a.set_yticks(ys); a.set_yticklabels([p.get("short") or p["name"] for p in cands])
    for t, p in zip(a.get_yticklabels(), cands):
        if p.get("ours"):
            t.set_fontweight("bold"); t.set_color(INK)
    a.set_xlim(-50, 25); a.set_ylim(-0.7, len(cands) - 0.1)
    a.grid(axis="y", visible=False); a.spines["left"].set_visible(False)
    a.set_xlabel("Estimated value per episode (DM)")
    a.set_title("(a) Held-out value, 95% bootstrap CI")

    est = [p for p in P if p.get("dr") is not None]
    b.plot([-50, 22], [-50, 22], color=INK3, lw=0.8, ls=(0, (3, 3)))
    offs = {"ours": (-1.5, 1.2, "right"), "rules": (1.5, -0.5, "left"), "wait": (1.5, -1.8, "left"),
            "simple_rule": (1.5, -4.2, "left"), "park": (1.5, -3.2, "left"), "escalate": (1.5, 1.2, "left"),
            "check_in": (1.5, -4.0, "left"), "estimate_nudge": (1.8, -1.2, "left")}
    for p in est:
        col = OURS if p.get("ours") else BASE
        b.plot(p["dm"], p["dr"], "o", ms=6.5 if p.get("ours") else 5, color=col, mec="white", mew=1.2, zorder=3)
        dx, dy, ha = offs.get(p.get("lab"), (1.5, 0, "left"))
        b.text(p["dm"] + dx, p["dr"] + dy, p.get("lab", ""), fontsize=7.8, ha=ha,
               color=INK if p.get("ours") else INK2, fontweight="bold" if p.get("ours") else "normal")
    gap = max(abs(p["dm"] - p["dr"]) for p in est)
    b.text(-48, 17, f"max |DM − DR| = {gap:.2f}", fontsize=8, color=INK2)
    b.set_xlim(-50, 22); b.set_ylim(-50, 22); b.set_aspect("equal", adjustable="box")
    b.set_xlabel("DM value per episode"); b.set_ylabel("DR value per episode")
    b.set_title("(b) Agreement between estimators")
    save(fig, "fig3_main_results")


# ---------------------------------------------------------------- Figure 4
def fig_ablation():
    A = {a["name"]: a for a in D["ablation"]}
    steps = [("FQI teacher\n(no guardrails)", A["FQI teacher, no guardrails"]["dm"]),
             ("+ guardrails", A["FQI teacher + guardrails (not distilled)"]["dm"]),
             ("+ distil to\ndepth-10 tree\n(shipped)", A["Shipped: guardrails + tree (d=10)"]["dm"])]
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 3.7), layout="constrained", gridspec_kw=dict(width_ratios=[1, 1.2]))
    fig.get_layout_engine().set(wspace=0.1)
    prev = None
    for i, (lab, v) in enumerate(steps):
        if prev is None:
            a.bar(i, v, width=0.55, color=BASE)
        else:
            a.bar(i, v, width=0.55, color=OURS if i == 2 else BASE)
            a.annotate("", xy=(i - 0.3, v), xytext=(i - 0.7, prev),
                       arrowprops=dict(arrowstyle="-|>", color=INK3, lw=1, mutation_scale=8))
            a.text(i - 0.42, (prev + v) / 2 + 0.9, sgn(v - prev), ha="left", fontsize=8, family=MONO, color="#c43a3a")
        a.text(i, v + 0.5, sgn(v), ha="center", fontsize=8.5, family=MONO, color=INK)
        prev = v
    a.set_xticks(range(3)); a.set_xticklabels([s[0] for s in steps], fontsize=8)
    a.set_ylim(0, 24); a.grid(axis="x", visible=False)
    a.set_ylabel("DM value per episode")
    a.set_title("(a) Cost of guardrails and distillation")

    rows = [("− learned model (rules, else WAIT)", A["− learned model (rules, else WAIT)"]["dm"]),
            ("− membership rule", A["− membership rule"]["dm"]),
            ("− guardrails at runtime (tree alone)", A["− guardrails (tree alone)"]["dm"]),
            ("− escalation rule", A["− escalation rule"]["dm"])]
    full = A["Shipped: guardrails + tree (d=10)"]["dm"]
    ys = range(len(rows))
    for y, (lab, v) in zip(ys, rows):
        d = v - full
        b.barh(y, d, height=0.5, color="#c43a3a" if d < -0.05 else "#0f8a0f" if d > 0.05 else BASE)
        b.text(d + (0.25 if d >= 0 else -0.25), y, sgn(d), va="center", ha="left" if d >= 0 else "right",
               fontsize=8, family=MONO, color=INK)
    b.axvline(0, color=INK3, lw=0.8)
    b.set_yticks(list(ys)); b.set_yticklabels([r[0] for r in rows], fontsize=8.3)
    b.set_xlim(-17, 3); b.set_xticks([-15, -10, -5, 0]); b.grid(axis="y", visible=False); b.spines["left"].set_visible(False)
    b.set_xlabel(f"Δ DM vs shipped policy ({sgn(full)})")
    b.set_title("(b) Remove one component at a time")
    save(fig, "fig4_ablation")


# ---------------------------------------------------------------- Figure 5
def fig_depth():
    dp = D["depth"]
    xs = [p["d"] for p in dp]
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.5), layout="constrained")
    fig.get_layout_engine().set(wspace=0.08)
    for ax, key, fmt, title, lims in (
        (a, "fid", lambda v: f"{v:.0f}%", "(a) Fidelity to relabelled teacher (train)", (20, 100)),
        (b, "dm", lambda v: sgn(v), "(b) Held-out policy value (DM)", (-10, 20)),
    ):
        ys = [p[key] for p in dp]
        ax.axvline(10, color=OURS, lw=0.9, ls=(0, (3, 3)))
        ax.text(10.3, lims[1] - (lims[1] - lims[0]) * 0.06, "shipped", color=OURS, fontsize=7.8)
        ax.plot(xs, ys, color=OURS, lw=1.8, marker="o", ms=4.5, mec="white", mew=1)
        for p, y in zip(dp, ys):
            if p["d"] in (2, 10, 14):
                if p["d"] == 2:
                    ax.text(p["d"] + 0.5, y, fmt(y), fontsize=8, family=MONO, va="center")
                elif p["d"] == 10:
                    ax.text(p["d"] + 0.35, y - (lims[1] - lims[0]) * 0.07, fmt(y), fontsize=8, family=MONO, ha="left",
                            color=OURS, fontweight="bold")
                else:
                    ax.text(p["d"], y + (lims[1] - lims[0]) * 0.05, fmt(y), fontsize=8, family=MONO, ha="center")
        ax.set_xticks(xs); ax.set_xticklabels([f'{p["d"]}\n{p["leaves"]}' for p in dp])
        ax.set_xlim(0.5, 15.5); ax.set_ylim(*lims)
        ax.set_xlabel("Tree max depth  (second row: leaves)"); ax.set_title(title)
    a.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    b.yaxis.set_major_formatter(lambda v, _: sgn(v, 0) if v else "0")
    b.axhline(0, color=INK3, lw=0.8)
    save(fig, "fig5_depth_sweep")


# ---------------------------------------------------------------- Figure 6
def fig_slices():
    sl = D["slices"]
    names = [s["k"] for s in sl][::-1]
    series = [("ours", "Shipped (ours)", OURS), ("rule", "Rule policy", "#6b7079"),
              ("wait", "always_wait", BASE), ("simple", "simple_rule", "#c9ccd1")]
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    h = 0.19
    for j, (k, lab, col) in enumerate(series):
        ys = [i + (1.5 - j) * h for i in range(len(names))]
        ax.barh(ys, [s[k] for s in sl][::-1], height=h * 0.9, color=col, label=lab)
    for i, s in enumerate(sl[::-1]):
        ax.text(max(s["ours"], 0) + 0.8, i + 1.5 * h, sgn(s["ours"]), va="center", fontsize=7.5, family=MONO, color=OURS)
    ax.axvline(0, color=INK3, lw=0.8)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
    for t in ax.get_yticklabels():
        if t.get_text() == "Overall":
            t.set_fontweight("bold"); t.set_color(INK)
    ax.axhline(0.5, color=INK3, lw=0.6)
    ax.grid(axis="y", visible=False); ax.spines["left"].set_visible(False)
    ax.set_xlabel("DM value per episode (held-out)")
    ax.set_title("Value by customer segment", pad=30)
    ax.legend(ncol=4, loc="lower left", bbox_to_anchor=(0, 1.0), fontsize=8, handlelength=1, handleheight=0.8, borderaxespad=0.3)
    save(fig, "fig6_slices")


# ---------------------------------------------------------------- Figure 7
def fig_mix():
    mix = sorted(D["mix"], key=lambda r: -r["old"])
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ys = list(range(len(mix)))[::-1]
    h = 0.36
    ax.barh([y + h / 2 for y in ys], [r["old"] for r in mix], height=h * 0.92, color=LOGGED, label="Logged policy")
    ax.barh([y - h / 2 for y in ys], [r["nw"] for r in mix], height=h * 0.92, color=OURS, label="Shipped policy")
    for y, r in zip(ys, mix):
        ax.text(r["old"] + 0.4, y + h / 2, f'{r["old"]:.1f}%', va="center", fontsize=7.5, color=INK2)
        ax.text(r["nw"] + 0.4, y - h / 2, f'{r["nw"]:.1f}%', va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(ys); ax.set_yticklabels([r["k"] for r in mix], family=MONO, fontsize=8)
    ax.set_xlim(0, 36); ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share of 15,565 held-out decisions")
    ax.set_title("Action distribution, logged vs shipped")
    ax.legend(loc="lower right", fontsize=8.5)
    save(fig, "fig7_action_distribution")


# ---------------------------------------------------------------- Tables
def table_png(name, title, header, rows, align=None, highlight=(), bold=None, col_w=None, note=None):
    """Booktabs-style table: top/mid/bottom rules, no verticals."""
    n = len(header)
    align = align or (["left"] + ["right"] * (n - 1))
    col_w = col_w or ([2.6] + [1.2] * (n - 1))
    W = sum(col_w); rh = 0.27
    H = rh * (len(rows) + 1) + 0.55 + (0.3 if note else 0)
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    ax.text(0, 0.22, title, fontsize=9, color=INK, va="center", fontweight="bold")
    y0 = 0.42
    xs = [sum(col_w[:i]) for i in range(n)]

    def cell_x(i):
        return xs[i] + 0.06 if align[i] == "left" else xs[i] + col_w[i] - 0.06

    ax.plot([0, W], [y0, y0], color=INK, lw=1.3)
    for i, h in enumerate(header):
        ax.text(cell_x(i), y0 + rh / 2, h, ha=align[i], va="center", fontsize=8.3, fontweight="bold", color=INK)
    ax.plot([0, W], [y0 + rh, y0 + rh], color=INK, lw=0.8)
    for r, row in enumerate(rows):
        yy = y0 + rh * (r + 1)
        if r in highlight:
            ax.add_patch(plt.Rectangle((0, yy), W, rh, color=OURS_SOFT, lw=0))
        for i, v in enumerate(row):
            b = bold and bold(r, i)
            ax.text(cell_x(i), yy + rh / 2, str(v), ha=align[i], va="center", fontsize=8.2,
                    family=MONO if i else "Helvetica Neue", color=INK, fontweight="bold" if b else "normal")
    yb = y0 + rh * (len(rows) + 1)
    ax.plot([0, W], [yb, yb], color=INK, lw=1.3)
    if note:
        ax.text(0, yb + 0.2, note, fontsize=7.2, color=INK3, va="center")
    save(fig, name, pdf=False)


def md_table(title, header, rows):
    out = [f"**{title}**", "", "| " + " | ".join(header) + " |",
           "|" + "|".join([":--"] + ["--:"] * (len(header) - 1)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def tables():
    md = ["# Result tables\n", "All values from the offline evaluator on the held-out split (5,000 episodes, 15,565 steps) unless noted.\n"]

    # T1 outcomes
    h = ["Outcome", "Steps", "Share", "Mean reward"]
    rows = [[o["k"], f'{o["n"]:,}', f'{o["share"]:.1f}%', sgn(o["r"], 1)] for o in D["outcomes"]]
    t = "Table 1. Outcome structure of the logged data (90,298 steps)"
    table_png("table1_outcomes", t, h, rows, col_w=[2.4, 1.0, 0.9, 1.1]); md.append(md_table(t, h, rows))

    # T2 unhappy
    h = ["Action taken", "n", "Mean reward"]
    rows = [[u["k"], f'{u["n"]:,}', sgn(u["r"], 1)] for u in D["unhappy"]]
    t = "Table 2. Logged reward when the customer is unhappy"
    table_png("table2_unhappy_customers", t, h, rows, highlight=(0,), col_w=[2.4, 0.8, 1.1]); md.append(md_table(t, h, rows))

    # T3 sanity
    h = ["Quantity", "Value"]
    rows = [["Empirical mean episode return (ground truth)", "−13.46"], ["FQE estimate at turn 0", "−13.21"],
            ["Absolute error", "0.26 (1.9%)"], ["SNIPS with π = π_β", "−4.33"], ["Empirical mean reward per step", "−4.33"]]
    t = "Table 3. Evaluator sanity check (target policy = logging policy)"
    table_png("table3_sanity_check", t, h, rows, col_w=[3.4, 1.2]); md.append(md_table(t, h, rows))

    # T4 main
    P = D["policies"]
    h = ["Policy", "DM / episode", "95% CI", "DR / episode", "SNIPS / step", "ESS", "Send rate"]
    rows = [[p["name"], sgn(p["dm"]), f'[{sgn(p["ci"][0], 1)}, {sgn(p["ci"][1], 1)}]' if p.get("ci") else "—",
             sgn(p["dr"]) if p.get("dr") is not None else "—", sgn(p["snips"]), f'{p["ess"]:,}', f'{p["send"]:.1f}%'] for p in P]
    t = "Table 4. Off-policy value on 5,000 held-out episodes"
    table_png("table4_main_results", t, h, rows, highlight=(0,), bold=lambda r, i: r == 0 and i in (1, 3, 4),
              col_w=[2.9, 1.05, 1.2, 1.05, 1.05, 0.75, 0.9],
              note="DM/DR per episode; SNIPS per step (different scale). Logged policy DM = empirical return. CI: episode bootstrap, Q-model fixed.")
    md.append(md_table(t, h, rows))

    # T5 ablation
    A = D["ablation"]; full = A[0]["dm"]
    h = ["Variant", "DM / episode", "Δ DM", "DR / episode", "SNIPS / step", "Send rate"]
    rows = [[a["name"], sgn(a["dm"]), "—" if i == 0 else sgn(a["dm"] - full), sgn(a["dr"]), sgn(a["snips"]), f'{a["send"]:.1f}%']
            for i, a in enumerate(A)]
    t = "Table 5. Component ablation (held-out)"
    table_png("table5_ablation", t, h, rows, highlight=(0,), col_w=[3.1, 1.05, 0.8, 1.05, 1.05, 0.9],
              note="“−” rows remove a rule at inference only; the tree was still trained on relabelled targets.")
    md.append(md_table(t, h, rows))

    # T6 slices
    h = ["Slice", "Steps", "Episodes", "Shipped (ours)", "Rule policy", "always_wait", "simple_rule"]
    rows, best = [], []
    for s in D["slices"]:
        vals = [s["ours"], s["rule"], s["wait"], s["simple"]]
        best.append(3 + vals.index(max(vals)))
        rows.append([s["k"], f'{s["steps"]:,}', f'{s["eps"]:,}'] + [sgn(v) for v in vals])
    t = "Table 6. DM value per episode by customer segment (best per row in bold)"
    table_png("table6_slices", t, h, rows, bold=lambda r, i: i == best[r], col_w=[1.9, 0.8, 0.85, 1.15, 1.0, 1.0, 1.0])
    md.append(md_table(t, h, rows))

    # T7 support
    h = ["Action", "Logged rows", "Logged share", "Shipped share"]
    rows = [[r["k"], f'{r["n"]:,}', f'{r["old"]:.1f}%', f'{r["nw"]:.1f}%'] for r in D["support"]]
    t = "Table 7. Data support per action vs how often the shipped policy uses it"
    table_png("table7_action_support", t, h, rows, highlight=(6, 7), col_w=[2.2, 1.1, 1.1, 1.1])
    md.append(md_table(t, h, rows))

    # T8 depth
    h = ["Depth", "Leaves", "Fidelity", "Weighted F1", "DM / episode", "DR / episode"]
    rows = [[p["d"], p["leaves"], f'{p["fid"]:.1f}%', f'{p["f1"]:.1f}%', sgn(p["dm"]), sgn(p["dr"])] for p in D["depth"]]
    t = "Table 8. Distillation depth sweep"
    table_png("table8_depth_sweep", t, h, rows, highlight=(4,), col_w=[0.8, 0.8, 0.95, 1.05, 1.1, 1.1])
    md.append(md_table(t, h, rows))

    open(os.path.join(HERE, "tables.md"), "w").write("\n".join(md))
    print("wrote tables.md")


if __name__ == "__main__":
    fig_system(); fig_fatigue(); fig_main(); fig_ablation(); fig_depth(); fig_slices(); fig_mix()
    tables()
