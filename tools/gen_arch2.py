import sys; sys.path.insert(0, ".")
from svglib import SVG, INK, MUTED, FAINT, MONO, SANS

OUT = "../project_images/diagrams/"
IND="#6366f1"; TEAL="#0d9488"; VIO="#8b5cf6"; ROSE="#e11d48"; AMB="#d97706"; SKY="#0284c7"; SLATE="#64748b"

def head(s, t, sub):
    s.text(26, 32, t, size=14.5, weight=700, color=INK)
    s.text(26, 50, sub, size=11, color=MUTED, font=MONO)

# ------------------------------------------------- Travel agent (eval-gated)
s = SVG(900, 400)
head(s, "Eval-gated skill development", "a skill ships only if the evals prove it helps")
s.node(26, 92, 168, 62, "skill registry", "17 skills, versioned", SLATE, tsize=12.5)
s.node(232, 92, 150, 62, "release CLI", "cut a version", SLATE, tsize=12.5)
s.node(420, 92, 168, 62, "LangGraph agent", "travel planning", IND, tsize=12.5)
s.node(626, 92, 168, 62, "task bank", "466 tasks", TEAL, tsize=12.5)
s.arrow(194,123,228,123); s.arrow(382,123,416,123); s.arrow(588,123,622,123)

s.band(26, 178, 848, 104, "A/B evaluation  -  same agent, skill injected vs. withheld")
s.node(48, 210, 236, 56, "with injection", "skill in context", TEAL, tsize=12.5)
s.node(332, 210, 236, 56, "without injection", "control arm", SLATE, tsize=12.5)
s.node(616, 210, 236, 56, "delta", "+17 pts top skill", VIO, tsize=12.5)
s.arrow(284,238,328,238); s.arrow(568,238,612,238)

s.band(26, 300, 530, 82, "3-tier CI gates   ~$0.03 / PR")
for i,(n,d) in enumerate([("tier 1","smoke"),("tier 2","regression"),("tier 3","full bank")]):
    s.node(44+i*168, 328, 158, 44, n, d, ROSE, tsize=12)
s.node(592, 316, 130, 56, "merge", "gate passed", TEAL, tsize=12.5)
s.node(744, 316, 130, 56, "block", "gate failed", ROSE, tsize=12.5)
s.arrow(556,344,588,344)
s.save(OUT+"travel-agent.svg", "Eval-gated skill pipeline")

# ------------------------------------------------- Godot MCP
s = SVG(900, 330)
head(s, "MCP server for the Godot engine", "natural language -> validated engine operations")
s.node(26, 104, 176, 74, "LLM client", "Claude, Cursor", IND, tsize=13)
s.node(258, 96, 210, 90, "MCP server", "30+ tools", VIO, tsize=13)
s.node(524, 104, 176, 74, "path validation", "sandboxed writes", ROSE, tsize=12.5)
s.node(742, 104, 132, 74, "Godot 4", "project", TEAL, tsize=13)
s.arrow(202,141,254,141,"MCP")
s.arrow(468,141,520,141,"tool call")
s.arrow(700,141,738,141)
s.band(26, 208, 848, 100, "tool surface")
for i,(n,d) in enumerate([("scene","node tree"),("script","GDScript"),("execution","run / debug"),("assets","import")]):
    s.node(46+i*208, 240, 190, 50, n, d, SKY, tsize=12.5)
s.save(OUT+"godot-mcp.svg", "Godot MCP architecture")

# ------------------------------------------------- InfoDistill
s = SVG(900, 300)
head(s, "Agentic research summarization", "extract -> classify -> summarize, no labeled data required")
s.node(26, 104, 150, 70, "sources", "tech feeds", SLATE, tsize=13)
s.node(216, 104, 168, 70, "extraction", "article parse", IND, tsize=13)
s.node(424, 104, 190, 70, "zero-shot classify", "new labels, no retrain", TEAL, tsize=12.5)
s.node(654, 104, 220, 70, "BART", "abstractive summary", VIO, tsize=13)
for a,b in ((176,216),(384,424),(614,654)): s.arrow(a,139,b-4,139)
s.text(450, 232, "FastAPI pipeline  -  stages run and debug independently  -  React frontend",
       size=11.5, color=MUTED, anchor="middle", font=MONO)
s.text(450, 262, "zero-shot classification means the topic taxonomy can change without collecting labels",
       size=10.5, color=FAINT, anchor="middle", font=MONO)
s.save(OUT+"infodistill.svg", "InfoDistill pipeline")

# ------------------------------------------------- DefiLlama RPC failover
s = SVG(900, 340)
head(s, "RPC endpoint resolution and failover", "user endpoints win; failing providers are quarantined, not discarded")
s.node(26, 96, 150, 62, "request", None, SLATE, tsize=13)
s.node(216, 88, 210, 78, "resolve endpoint", "user-defined first", IND, tsize=12.5)
s.node(466, 96, 170, 62, "healthy pool", "in rotation", TEAL, tsize=12.5)
s.node(704, 96, 170, 62, "response", None, TEAL, tsize=13)
s.arrow(176,127,212,127); s.arrow(426,127,462,127); s.arrow(636,127,700,127)
s.text(321, 182, "Fixes #162 - defaults no longer override user config",
       size=10, color=FAINT, anchor="middle", font=MONO)

s.node(466, 226, 170, 62, "quarantine", "10 min cooldown", ROSE, tsize=12.5)
s.elbow(551, 158, 551, 226, via_y=204, label="5 failures", color=ROSE)
s.path("M 636 257 L 760 257 L 760 164", stroke=TEAL, dash="5 4")
s.text(700, 249, "cooldown elapsed -> retry", size=10, color=MUTED, anchor="middle", font=MONO)
s.text(450, 312, "bounds the blast radius of one bad provider without permanently dropping it",
       size=10.5, color=FAINT, anchor="middle", font=MONO)
s.save(OUT+"defillama.svg", "RPC failover state machine")
print("4 more diagrams written")
