"""
Portfolio figures and ablation tables for the differentially private Adult analysis.

Standalone: reads adult_clean.csv (or rebuilds it from UCI), writes
  figures/*.png, figures/*.pdf   -- paper-quality figures
  RESULTS.md                     -- ablation and comparison tables

All privacy mechanisms come from IBM diffprivlib. Nothing is hand-rolled.
"""
import os, sys, warnings, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from sklearn.linear_model import LogisticRegression as SkLR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

from diffprivlib.mechanisms import Geometric, Exponential, PermuteAndFlip
from diffprivlib.models import LogisticRegression as DPLR

np.seterr(all="ignore")
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
os.makedirs(FIGDIR, exist_ok=True)

# ----------------------------------------------------------------------------- style
C = {"blue": "#2B6CB0", "green": "#2F855A", "rust": "#9C4221",
     "purple": "#553C9A", "grey": "#4A5568", "light": "#A0AEC0", "amber": "#B7791F"}
plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 220, "savefig.bbox": "tight",
    "font.family": "sans-serif", "font.size": 9.5,
    "axes.titlesize": 10.5, "axes.titleweight": "semibold", "axes.labelsize": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#CBD5E0", "axes.linewidth": 0.9,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "xtick.color": "#4A5568", "ytick.color": "#4A5568",
    "legend.frameon": False, "legend.fontsize": 8.5,
    "grid.color": "#E2E8F0", "grid.linewidth": 0.7,
})

def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIGDIR, f"{name}.{ext}"))
    plt.close(fig)
    print(f"  wrote figures/{name}.png|.pdf", flush=True)

def grid(ax, axis="both"):
    ax.grid(True, axis=axis, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

# ----------------------------------------------------------------------------- data
COLS = ["age","workclass","fnlwgt","education","education_num","marital_status","occupation",
        "relationship","race","sex","capital_gain","capital_loss","hours_per_week",
        "native_country","income"]

def load():
    for p in ["adult_clean.csv", "../adult_clean.csv",
              os.path.join(HERE, "..", "adult_clean.csv")]:
        try:
            return pd.read_csv(p, skipinitialspace=True)
        except (FileNotFoundError, OSError):
            continue
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
                     header=None, names=COLS, skipinitialspace=True, na_values=["?"])
    return df.dropna().reset_index(drop=True)

df = load()
FEATURES = ["age", "education_num", "hours_per_week"]
HIGH = ">50K"
PUBLIC_BOUNDS = {"age": (17, 90), "education_num": (1, 16), "hours_per_week": (1, 99)}
OCCUPATIONS = ["Adm-clerical","Armed-Forces","Craft-repair","Exec-managerial","Farming-fishing",
    "Handlers-cleaners","Machine-op-inspct","Other-service","Priv-house-serv","Prof-specialty",
    "Protective-serv","Sales","Tech-support","Transport-moving"]

TRUE_COUNT = int((df["income"] == HIGH).sum())
TRUE_HIST = df.loc[df["income"] == HIGH, "occupation"].value_counts()
TRUE_TOP3 = [o for o, _ in sorted(TRUE_HIST.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
print(f"data {df.shape} | true count {TRUE_COUNT} | true top3 {TRUE_TOP3}", flush=True)

EPS_GRID = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]

def scale(X, bounds):
    Xs = X.copy().astype(float)
    for c in FEATURES:
        lo, hi = bounds[c]
        Xs[c] = (Xs[c].clip(lo, hi) - lo) / (hi - lo)
    return Xs

def split(bounds=PUBLIC_BOUNDS):
    y = (df["income"] == HIGH).astype(int)
    X = scale(df[FEATURES], bounds)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def metrics(m, Xte, yte):
    p = m.predict(Xte)
    return dict(accuracy=accuracy_score(yte, p),
                precision=precision_score(yte, p, zero_division=0),
                recall=recall_score(yte, p, zero_division=0))

Xtr, Xte, ytr, yte = split()
BASE = SkLR(max_iter=1000).fit(Xtr, ytr)
BASE_M = metrics(BASE, Xte, yte)
print(f"baseline {BASE_M}", flush=True)

TABLES = {}

# ============================================================== FIG 1 : threat model
print("\n[1/4] threat model ...", flush=True)
t0 = time.time()

def attack_accuracy(eps, n_repeats, trials, rng):
    """Differencing attack. World 1: target is a high earner (gap 1). World 0: not (gap 0)."""
    mech = Geometric(epsilon=eps, sensitivity=1, random_state=int(rng.integers(1 << 30)))
    rest = TRUE_COUNT - 1
    correct = 0
    for _ in range(trials):
        world = rng.integers(2)
        a_true = rest + world
        obs_a = np.mean([mech.randomise(a_true) for _ in range(n_repeats)])
        obs_b = np.mean([mech.randomise(rest) for _ in range(n_repeats)])
        correct += int((obs_a - obs_b > 0.5) == bool(world))
    return 100 * correct / trials

REPEATS = [1, 2, 5, 10, 25, 50, 100]
ATTACK_EPS = [0.1, 0.5, 1.0, 5.0]
rng = np.random.default_rng(7)
attack = {e: [attack_accuracy(e, n, 1500, rng) for n in REPEATS] for e in ATTACK_EPS}
TABLES["attack"] = pd.DataFrame(attack, index=REPEATS).T

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))

ax = axes[0]
cols = [C["rust"], C["amber"], C["green"], C["blue"]]
for (e, ys), col in zip(attack.items(), cols):
    ax.plot(REPEATS, ys, "o-", color=col, ms=4.5, lw=1.7, label=f"DP, ε = {e}")
ax.axhline(100, ls="-", lw=1.6, color=C["grey"], alpha=0.85)
ax.text(1.15, 100.8, "no DP — target exposed on the first query", fontsize=8.2,
        color=C["grey"], va="bottom")
ax.axhline(50, ls=":", lw=1.2, color=C["light"])
ax.text(1.05, 46.5, "random guessing (50%)", fontsize=8, color=C["light"], ha="left")
ax.axvspan(0.9, 1.5, color=C["purple"], alpha=0.10, zorder=0)
ax.annotate("privacy budget\nstops the attacker here",
            xy=(1.5, 72), xytext=(4.2, 62), fontsize=8.2, color=C["purple"],
            arrowprops=dict(arrowstyle="->", color=C["purple"], lw=1.1))
ax.set_xscale("log"); ax.set_xticks(REPEATS); ax.set_xticklabels(REPEATS)
ax.set_ylim(40, 107)
ax.set_xlabel("repeated query pairs the attacker is allowed")
ax.set_ylabel("attacker accuracy (%)")
ax.set_title("(a) Differencing attack: noise alone is not enough")
ax.legend(loc="lower right"); grid(ax)

ax = axes[1]
show_eps = [0.05, 0.5, 5.0]
shades = [C["rust"], C["amber"], C["blue"]]
for e, col in zip(show_eps, shades):
    m = Geometric(epsilon=e, sensitivity=1, random_state=11)
    draws = np.array([m.randomise(TRUE_COUNT) for _ in range(30000)])
    lo, hi = np.percentile(draws, [0.5, 99.5])
    bins = np.arange(lo, hi + 2) - 0.5 if hi - lo < 400 else 80
    ax.hist(draws, bins=bins, density=True, histtype="stepfilled",
            color=col, alpha=0.30, lw=0)
    ax.hist(draws, bins=bins, density=True, histtype="step", color=col, lw=1.5,
            label=f"ε = {e}")
ax.set_yscale("log"); ax.set_ylim(1e-5, 3)
ax.axvline(TRUE_COUNT, color=C["grey"], ls="--", lw=1.4)
ax.text(TRUE_COUNT + 4, 1.4, f"true = {TRUE_COUNT:,}", fontsize=8.4, color=C["grey"])
ax.set_xlim(TRUE_COUNT - 130, TRUE_COUNT + 130)
ax.set_xlabel("released count"); ax.set_ylabel("density (log scale)")
ax.set_title("(b) What the released answer actually looks like")
ax.legend(loc="upper right"); grid(ax)

fig.suptitle("Threat model: why differential privacy needs both noise and a budget",
             fontsize=12, fontweight="semibold", y=1.02)
save(fig, "fig1_threat_model")
print(f"  ({time.time()-t0:.0f}s)", flush=True)

# ====================================================== FIG 2 : selection / rank stability
print("\n[2/4] selection mechanisms ...", flush=True)
t0 = time.time()

def top3_histogram(eps, seed):
    m = Geometric(epsilon=eps, sensitivity=2, random_state=seed)
    noisy = {o: m.randomise(int(TRUE_HIST.get(o, 0))) for o in OCCUPATIONS}
    return [o for o, _ in sorted(noisy.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]

def _peel(mech_cls, eps, seed):
    """Top-3 by peeling: 3 rounds at eps/3, removing the winner each round."""
    remaining, chosen = list(OCCUPATIONS), []
    rs = np.random.default_rng(seed)
    for _ in range(3):
        util = [float(TRUE_HIST.get(o, 0)) for o in remaining]
        mech = mech_cls(epsilon=eps / 3, sensitivity=1, utility=util,
                        candidates=remaining, monotonic=False,
                        random_state=int(rs.integers(1 << 30)))
        pick = mech.randomise()
        chosen.append(pick); remaining.remove(pick)
    return chosen

top3_exponential = lambda eps, seed: _peel(Exponential, eps, seed)
top3_permuteflip = lambda eps, seed: _peel(PermuteAndFlip, eps, seed)

MECHS = [("Noisy histogram\n(report-noisy-max)", top3_histogram, C["blue"]),
         ("Exponential\n(peeling, ε/3)", top3_exponential, C["green"]),
         ("PermuteAndFlip\n(peeling, ε/3)", top3_permuteflip, C["rust"])]
N_SEL = 1200
sel_rows, rank_track = [], {o: {e: 0 for e in EPS_GRID} for o in OCCUPATIONS}

for name, fn, _ in MECHS:
    for e in EPS_GRID:
        exact = same = 0
        for s in range(N_SEL):
            r = fn(e, s)
            exact += int(r == TRUE_TOP3); same += int(set(r) == set(TRUE_TOP3))
            if fn is top3_histogram:
                for o in r:
                    rank_track[o][e] += 1
        sel_rows.append(dict(mechanism=name.replace("\n", " "), epsilon=e,
                             exact_pct=100*exact/N_SEL, set_pct=100*same/N_SEL))
SEL = pd.DataFrame(sel_rows)
TABLES["selection"] = SEL

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))

ax = axes[0]
for (name, fn, col) in MECHS:
    sub = SEL[SEL.mechanism == name.replace("\n", " ")]
    ax.plot(sub.epsilon, sub.exact_pct, "o-", color=col, ms=4.5, lw=1.8,
            label=name.replace("\n", " "))
ax.set_xscale("log"); ax.set_ylim(0, 104)
ax.set_xlabel("ε (total, log scale)"); ax.set_ylabel("exact top-3 recovered (%)")
ax.set_title("(a) Selection mechanisms, head to head")
ax.legend(loc="lower right"); grid(ax)

ax = axes[1]
interesting = ["Exec-managerial", "Prof-specialty", "Sales", "Craft-repair", "Adm-clerical"]
pal = [C["blue"], C["green"], C["rust"], C["amber"], C["light"]]
for o, col in zip(interesting, pal):
    ys = [100 * rank_track[o][e] / N_SEL for e in EPS_GRID]
    ax.plot(EPS_GRID, ys, "o-", color=col, ms=4, lw=1.7,
            label=f"{o} ({int(TRUE_HIST.get(o,0)):,})")
ax.set_xscale("log"); ax.set_ylim(-3, 104)
ax.set_xlabel("ε (log scale)"); ax.set_ylabel("appears in released top-3 (%)")
ax.set_title("(b) Rank stability: margin decides, not dataset size")
ax.legend(loc="center right", title="occupation (true count)", title_fontsize=8)
grid(ax)

fig.suptitle("Task 2: private selection over a public category list",
             fontsize=12, fontweight="semibold", y=1.02)
save(fig, "fig2_selection")
print(f"  ({time.time()-t0:.0f}s)", flush=True)

# ============================================================ FIG 3 : model stability
print("\n[3/4] model stability ...", flush=True)
t0 = time.time()
MODEL_EPS = [0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
N_MODEL = 25
coef_runs, acc_runs = {e: [] for e in MODEL_EPS}, {e: [] for e in MODEL_EPS}
for e in MODEL_EPS:
    for s in range(N_MODEL):
        m = DPLR(epsilon=e, data_norm=float(np.sqrt(3)), max_iter=1000, random_state=s).fit(Xtr, ytr)
        coef_runs[e].append(m.coef_[0]); acc_runs[e].append(metrics(m, Xte, yte)["accuracy"])
    print(f"    eps={e} done", flush=True)

fig, axes = plt.subplots(1, 4, figsize=(15, 4.0))
pos = np.arange(len(MODEL_EPS))
for i, (feat, col) in enumerate(zip(FEATURES, [C["blue"], C["green"], C["rust"]])):
    ax = axes[i]
    data = [[c[i] for c in coef_runs[e]] for e in MODEL_EPS]
    bp = ax.boxplot(data, positions=pos, widths=0.55, patch_artist=True,
                    medianprops=dict(color="white", lw=1.4),
                    flierprops=dict(ms=2.5, mfc=col, mec="none", alpha=.5))
    for b in bp["boxes"]:
        b.set(facecolor=col, alpha=0.75, lw=0)
    for w in bp["whiskers"] + bp["caps"]:
        w.set(color=col, lw=1.1)
    ax.axhline(BASE.coef_[0][i], ls="--", lw=1.4, color=C["grey"])
    ax.set_xticks(pos); ax.set_xticklabels([str(e) for e in MODEL_EPS], rotation=45)
    ax.set_xlabel("ε"); ax.set_title(f"({'abc'[i]}) coefficient: {feat}")
    if i == 0: ax.set_ylabel("fitted coefficient")
    grid(ax, axis="y")

ax = axes[3]
data = [acc_runs[e] for e in MODEL_EPS]
bp = ax.boxplot(data, positions=pos, widths=0.55, patch_artist=True,
                medianprops=dict(color="white", lw=1.4),
                flierprops=dict(ms=2.5, mfc=C["purple"], mec="none", alpha=.5))
for b in bp["boxes"]:
    b.set(facecolor=C["purple"], alpha=0.75, lw=0)
for w in bp["whiskers"] + bp["caps"]:
    w.set(color=C["purple"], lw=1.1)
ax.axhline(BASE_M["accuracy"], ls="--", lw=1.4, color=C["grey"])
ax.set_xticks(pos); ax.set_xticklabels([str(e) for e in MODEL_EPS], rotation=45)
ax.set_xlabel("ε"); ax.set_ylabel("test accuracy"); ax.set_title("(d) test accuracy")
grid(ax, axis="y")

fig.legend(handles=[Line2D([], [], ls="--", color=C["grey"], lw=1.4)],
           labels=["non-private value"], loc="upper right", bbox_to_anchor=(0.995, 1.01))
fig.suptitle(f"Task 3: coefficient and accuracy stability over {N_MODEL} private refits per ε",
             fontsize=12, fontweight="semibold", y=1.03)
save(fig, "fig3_model_stability")
TABLES["model"] = pd.DataFrame([
    dict(epsilon=e,
         acc_mean=np.mean(acc_runs[e]), acc_std=np.std(acc_runs[e]),
         **{f"{f}_std": np.std([c[i] for c in coef_runs[e]]) for i, f in enumerate(FEATURES)})
    for e in MODEL_EPS])
print(f"  ({time.time()-t0:.0f}s)", flush=True)

# ================================================================ FIG 4 + ablations
print("\n[4/4] ablations ...", flush=True)
t0 = time.time()

# --- A: sensitivity misspecification (the silent bug) ---
rows = []
for e in [0.05, 0.1, 0.5, 1.0]:
    for sens, label in [(1, "Δ=1  (incorrect)"), (2, "Δ=2  (correct)")]:
        ex = 0
        for s in range(1500):
            m = Geometric(epsilon=e, sensitivity=sens, random_state=s)
            noisy = {o: m.randomise(int(TRUE_HIST.get(o, 0))) for o in OCCUPATIONS}
            top = [o for o, _ in sorted(noisy.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
            ex += int(top == TRUE_TOP3)
        rows.append(dict(epsilon=e, setting=label, exact_pct=100*ex/1500,
                         claimed_eps=e, actual_eps=e if sens == 2 else 2*e))
SENS = pd.DataFrame(rows); TABLES["sensitivity"] = SENS

# --- B: budget allocation ---
alloc = [("Equal split", 1.0, 1.0, 1.0), ("Utility-aware", 0.1, 0.4, 2.5),
         ("Utility-aware, half budget", 0.05, 0.2, 1.25), ("Minimal", 0.05, 0.1, 0.35)]
rows = []
for name, e1, e2, e3 in alloc:
    m1 = Geometric(epsilon=e1, sensitivity=1, random_state=3)
    errs = [abs(m1.randomise(TRUE_COUNT) - TRUE_COUNT) for _ in range(1500)]
    ex = sum(top3_histogram(e2, s) == TRUE_TOP3 for s in range(800)) / 800 * 100
    accs = [metrics(DPLR(epsilon=e3, data_norm=float(np.sqrt(3)), max_iter=1000,
                         random_state=s).fit(Xtr, ytr), Xte, yte)["accuracy"] for s in range(12)]
    rows.append(dict(strategy=name, total_eps=e1+e2+e3, eps_count=e1, eps_top3=e2, eps_model=e3,
                     count_err=np.mean(errs), top3_pct=ex, acc_mean=np.mean(accs)))
ALLOC = pd.DataFrame(rows); TABLES["allocation"] = ALLOC

# --- C: how loose a public bound costs you ---
BOUNDSETS = {
    "Data-derived (leaks)": {c: (int(df[c].min()), int(df[c].max())) for c in FEATURES},
    "Documented (used here)": PUBLIC_BOUNDS,
    "Loose but safe": {"age": (0, 120), "education_num": (0, 20), "hours_per_week": (0, 168)},
}
rows = []
for name, bnd in BOUNDSETS.items():
    xtr, xte, ytr_, yte_ = split(bnd)
    accs = [metrics(DPLR(epsilon=1.0, data_norm=float(np.sqrt(3)), max_iter=1000,
                         random_state=s).fit(xtr, ytr_), xte, yte_)["accuracy"] for s in range(15)]
    rows.append(dict(bounds=name, spec=str({k: tuple(v) for k, v in bnd.items()}),
                     acc_mean=np.mean(accs), acc_std=np.std(accs),
                     leaks="yes" if "Data" in name else "no"))
BOUNDS = pd.DataFrame(rows); TABLES["bounds"] = BOUNDS

fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.2))
fig.subplots_adjust(wspace=0.38)

ax = axes[0]
w = 0.36; xs = np.arange(len(SENS.epsilon.unique()))
for k, (lab, col) in enumerate(zip(["Δ=1  (incorrect)", "Δ=2  (correct)"], [C["rust"], C["blue"]])):
    sub = SENS[SENS.setting == lab]
    ax.bar(xs + (k - .5) * w, sub.exact_pct, w, color=col, alpha=.85, label=lab, zorder=3)
ax.set_xticks(xs); ax.set_xticklabels([str(e) for e in SENS.epsilon.unique()])
ax.set_xlabel("ε"); ax.set_ylabel("exact top-3 recovered (%)")
ax.set_ylim(0, 124)
ax.set_title("(a) Sensitivity bug is invisible in the output")
ax.legend(loc="lower right"); grid(ax, axis="y")
ax.text(0.02, 0.995, "Δ=1 scores higher at every ε —\nwhile silently spending 2ε",
        transform=ax.transAxes, va="top", fontsize=8.3, color=C["rust"])

ax = axes[1]
sat_eps = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]
sat_acc, sat_err = [], []
for e in sat_eps:
    sat_acc.append(np.mean([metrics(DPLR(epsilon=e, data_norm=float(np.sqrt(3)), max_iter=1000,
                                         random_state=s_).fit(Xtr, ytr), Xte, yte)["accuracy"]
                            for s_ in range(8)]))
    mm = Geometric(epsilon=e, sensitivity=1, random_state=5)
    sat_err.append(np.mean([abs(mm.randomise(TRUE_COUNT) - TRUE_COUNT) for _ in range(3000)]))
TABLES["saturation"] = pd.DataFrame(dict(epsilon=sat_eps, model_acc=sat_acc, count_abs_err=sat_err))

ax.plot(sat_eps, sat_acc, "o-", color=C["blue"], ms=4.5, lw=1.8, label="model accuracy")
ax.axhline(BASE_M["accuracy"], ls="--", lw=1.2, color=C["grey"])
ax.set_xscale("log"); ax.set_ylim(0.66, 0.80)
ax.set_xlabel("ε allocated to that one task (log)")
ax.set_ylabel("model accuracy", color=C["blue"])
ax.tick_params(axis="y", colors=C["blue"])
ax.axvspan(0.5, 2.3, color=C["blue"], alpha=0.07, zorder=0)
ax.text(0.013, 0.767, "model gains nothing\nbeyond ε ≈ 0.5", fontsize=8.2, color=C["blue"])

ax2 = ax.twinx()
ax2.plot(sat_eps, sat_err, "s--", color=C["rust"], ms=4, lw=1.6, label="count error")
ax2.set_yscale("log"); ax2.set_ylabel("count abs. error (log)", color=C["rust"])
ax2.tick_params(axis="y", colors=C["rust"]); ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_color("#CBD5E0")
ax2.text(0.013, 1.9, "count error keeps\nfalling all the way", fontsize=8.2, color=C["rust"])
ax.set_title("(b) The two tasks saturate at different ε")
grid(ax)
ax.plot([], [], "s--", color=C["rust"], ms=4, lw=1.6, label="count error (right axis)")
ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.015))

ax = axes[2]
cols = [C["rust"], C["blue"], C["amber"]]
ax.barh(range(len(BOUNDS)), BOUNDS.acc_mean, xerr=BOUNDS.acc_std,
        color=cols, alpha=.85, height=.55, zorder=3,
        error_kw=dict(ecolor=C["grey"], lw=1.1, capsize=3))
ax.set_yticks(range(len(BOUNDS)))
ax.set_yticklabels(["Data-derived\n(leaks)", "Documented\n(used here)", "Loose\nbut safe"], fontsize=8.5)
ax.axvline(BASE_M["accuracy"], ls="--", lw=1.3, color=C["grey"])
ax.set_xlim(0.70, 0.80); ax.invert_yaxis()
ax.set_xlabel("model accuracy (ε = 1)")
ax.set_title("(c) Using public bounds costs nothing"); grid(ax, axis="x")
ax.text(0.703, 0.5, "rows 1 and 2 are identical here — but you can\nonly know that by looking, and the looking is the leak",
        fontsize=7.6, color=C["grey"], va="center")

fig.suptitle("Ablations: what each design decision actually buys",
             fontsize=12, fontweight="semibold", y=1.02)
fig.tight_layout(rect=[0, 0, 1, 0.97]); fig.subplots_adjust(wspace=0.42)
save(fig, "fig4_ablations")
print(f"  ({time.time()-t0:.0f}s)", flush=True)

# ----------------------------------------------------------------------------- tables
import pickle
with open(os.path.join(HERE, "_tables.pkl"), "wb") as f:
    pickle.dump({k: v for k, v in TABLES.items()}, f)
print("\nAll figures written. Tables pickled for RESULTS.md.", flush=True)
for k, v in TABLES.items():
    print(f"\n===== {k} =====\n{v.round(4).to_string(index=False)}", flush=True)
