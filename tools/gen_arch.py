import sys; sys.path.insert(0, ".")
from svglib import SVG, INK, MUTED, FAINT, MONO, SANS

OUT = "../project_images/diagrams/"
IND="#6366f1"; TEAL="#0d9488"; VIO="#8b5cf6"; ROSE="#e11d48"; AMB="#d97706"; SKY="#0284c7"; SLATE="#64748b"

def head(s, t, sub):
    s.text(26, 32, t, size=14.5, weight=700, color=INK)
    s.text(26, 50, sub, size=11, color=MUTED, font=MONO)

# ---------------------------------------------------------------- HVAC
s = SVG(900, 400)
head(s, "Offline policy optimization from logged data",
     "fitted Q-iteration -> distillation -> guardrails")
y = 92
s.node(26, y, 150, 62, "Logged data", "74.7K steps", SLATE, mono=True)
s.node(216, y, 150, 62, "Fitted Q-Iteration", "Q(s,a) on logs", IND, mono=True)
s.node(406, y, 150, 62, "Distill", "-> decision tree", VIO, mono=True)
s.node(596, y, 150, 62, "Guardrails", "hard safety rules", ROSE, mono=True)
for x in (176, 366, 556):
    s.arrow(x, y+31, x+38, y+31)
s.arrow(746, y+31, 800, y+31)
s.node(786, y-4, 88, 70, "action", None, TEAL, mono=True, tsize=12)

# action space
s.band(26, 196, 848, 76, "action space  (8)")
acts = ["WAIT","CHECK_IN","ESTIMATE_NUDGE","ASK_OBJECTION","OFFER_SCHEDULING","MEMBERSHIP_TOUCH","PARK_THREAD","ESCALATE"]
bx = 42
for i,a in enumerate(acts):
    w = 6.6*len(a)+14
    s.rect(bx, 228, w, 26, fill=TEAL, stroke="none", rx=6, opacity=0.10)
    s.text(bx+w/2, 245, a, size=8.6, color=MUTED, anchor="middle", font=MONO)
    bx += w + 7

# OPE validation
s.band(26, 292, 848, 84, "off-policy evaluation  (3 independent estimators agree)")
for i,(n,d) in enumerate([("Direct Method","model-based Q"),("Doubly Robust","model + IPS"),("SNIPS","self-norm. IPS")]):
    s.node(46+i*282, 320, 258, 44, n, d, AMB, tsize=12)
s.save(OUT+"hvac.svg", "HVAC offline RL pipeline")

# ---------------------------------------------------------------- SLAM
s = SVG(900, 420)
head(s, "Real-time visual SLAM with learned features",
     "XFeat frontend -> NetVLAD loop closure -> GTSAM factor-graph backend")
s.node(26, 96, 118, 54, "images", "KITTI 00", SLATE, mono=True, tsize=12)
s.node(184, 96, 118, 54, "XFeat", "keypoints", IND, mono=True, tsize=12)
s.node(342, 96, 130, 54, "LighterGlue", "matching", IND, mono=True, tsize=12)
s.node(512, 96, 140, 54, "recoverPose", "RANSAC, E-matrix", VIO, mono=True, tsize=12)
for a,b in ((144,184),(302,342),(472,512)):
    s.arrow(a, 123, b-4, 123)
s.text(672, 118, "relative pose", size=11, color=MUTED, font=MONO)
s.text(672, 134, "unit-norm t", size=10, color=FAINT, font=MONO)
s.arrow(652, 123, 668, 123)

# loop closure branch
s.node(342, 186, 130, 50, "NetVLAD", "64 clusters", TEAL, mono=True, tsize=12)
s.node(512, 186, 118, 50, "FAISS", "top-5 L2", TEAL, mono=True, tsize=12)
s.node(670, 186, 158, 50, "loop verify", ">=150 inliers", TEAL, mono=True, tsize=12)
s.elbow(407, 150, 407, 186, via_y=170)
s.arrow(472, 211, 508, 211); s.arrow(630, 211, 666, 211)

# depth branch
s.node(26, 186, 118, 50, "stereo SGBM", "disparity", AMB, mono=True, tsize=11.5)
s.node(184, 186, 118, 50, "4x4 grid", "16 (u,v,Z)", AMB, mono=True, tsize=12)
s.arrow(144, 211, 180, 211)
s.elbow(85, 150, 85, 186, via_y=170)

# backend
s.band(26, 264, 848, 130, "C++ GTSAM backend  ->  Levenberg-Marquardt")
for i,(n,d) in enumerate([("PriorFactor","X(0) origin"),("BetweenFactor","VO odometry"),
                          ("ProjectionFactor","Huber 4px"),("GPSFactor","every 5 frames"),
                          ("LoopFactor","rotation only")]):
    s.node(44+i*166, 296, 156, 48, n, d, ROSE, tsize=11.5)
s.text(450, 378, "-> optimised trajectory   ~95 m  ->  ~1.2 m ATE   @ 20-25 FPS",
       size=11.5, color=INK, anchor="middle", font=MONO, weight=600)
s.save(OUT+"slam.svg", "Visual SLAM architecture")

# ---------------------------------------------------------------- Image RAG
s = SVG(900, 340)
head(s, "Hierarchical multimodal image RAG",
     "bi-encoder recall -> cross-encoder precision, over multiple rounds")
s.band(26, 78, 848, 108, "round 1  -  cluster routing + candidate generation")
s.node(46, 112, 150, 54, "text query", None, SLATE, mono=True, tsize=12)
s.node(232, 112, 176, 54, "Qwen3-VL embed", "bi-encoder", IND, mono=True, tsize=12)
s.node(444, 112, 190, 54, "FAISS IVFFlat", "nprobe = 5", TEAL, mono=True, tsize=12)
s.node(670, 112, 184, 54, "top-50", "cosine scores", TEAL, mono=True, tsize=12)
for a,b in ((196,232),(408,444),(634,670)): s.arrow(a,139,b-4,139)

s.band(26, 200, 848, 118, "round 2+  -  reranking + refinement")
s.node(46, 236, 150, 54, "follow-up", "query", SLATE, mono=True, tsize=12)
s.node(232, 236, 176, 54, "Qwen3-VL rerank", "cross-encoder", VIO, mono=True, tsize=12)
s.node(444, 236, 190, 54, "score fusion", "rerank x cos", VIO, mono=True, tsize=12)
s.node(670, 236, 184, 54, "top-10 -> top-3", "DAG-tracked", ROSE, mono=True, tsize=12)
for a,b in ((196,263),(408,263),(634,263)): pass
for a,b in ((196,232),(408,444),(634,670)): s.arrow(a,263,b-4,263)
s.elbow(762, 166, 762, 236, via_y=196, label="candidates")
s.save(OUT+"image-rag.svg", "Multimodal image RAG")

# ---------------------------------------------------------------- AgentPay
s = SVG(900, 360)
head(s, "Autonomous agent economy", "discovery -> escrow -> verified settlement, no human in the loop")
s.node(26, 100, 150, 66, "Agent A", "hirer", IND, tsize=13)
s.node(700, 100, 150, 66, "Agent B", "worker", IND, tsize=13)
s.node(300, 96, 276, 74, "on-chain registry", "Rust / Anchor - Solana, Avalanche", VIO, tsize=13)
s.arrow(176, 122, 296, 122, "discover")
s.arrow(576, 122, 696, 122, "hire")
s.node(300, 210, 276, 62, "escrow account", "funds locked", TEAL, tsize=13)
s.elbow(101, 166, 300, 232, via_y=232, label="fund")
s.elbow(776, 166, 576, 232, via_y=232, label="deliver")
s.node(26, 210, 200, 62, "reputation stake", "slash on default", ROSE, tsize=12.5)
s.arrow(300, 241, 230, 241, "verify")
s.text(450, 312, "LangChain orchestration + x402 payment tooling   ->   <30s end-to-end cycle",
       size=11.5, color=INK, anchor="middle", font=MONO, weight=600)
s.save(OUT+"agentpay.svg", "AgentPay architecture")
print("4 diagrams written")
