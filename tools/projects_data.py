# -*- coding: utf-8 -*-
"""Project content. Each `body` is HTML rendered onto that project's own page."""

D = "assets/img/diagrams/"
W = "assets/warp/figures/"   # warp-tote report figures
H = "assets/hvac/figures/"   # hvac report figures

def fig(src, alt, cap=None, wide=False):
    """wide=True lets very wide multi-panel plots break out of the text column."""
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    cls = "fig fig-wide" if wide else "fig"
    return (f'<figure class="{cls}"><a href="{src}" target="_blank" rel="noopener" '
            f'title="Open full size"><img src="{src}" alt="{alt}" loading="lazy"></a>{c}</figure>')

PROJECTS = [
{
 "slug":"hvac", "title":"HVAC Follow-up Policy Optimization",
 "category":"Machine Learning & Decision Systems",
 "tagline":"Offline reinforcement learning on 74.7K logged steps — fitted Q-iteration distilled into an auditable depth-10 decision tree, checked by three off-policy estimators that first had to recover the old policy's known value.",
 "short":"Offline RL that learns <em>when not to act</em>. FQI distilled into a depth-10 tree with guardrails; value per thread from −13.46 to +15.25.",
 "image": H+"fig1_system_overview.png", "dates":"Aug 2026",
 "tags":["Offline RL","Fitted Q-Iteration","Off-policy Evaluation","Policy Distillation","scikit-learn","Python"],
 "links":[],
 "body": f"""
<p>A follow-up policy for HVAC contractors that decides <strong>when and how</strong> to contact a
homeowner after a service visit: check in, nudge an open estimate, ask what the objection is,
offer scheduling, touch membership, park the thread, or escalate to a human.</p>

<p>The hard constraint is that you cannot experiment on real customers. All you have are logs from
an older policy, which only recorded outcomes for the actions <em>it</em> chose. Every claim about
an unexplored action is model-based extrapolation, so the work is as much about <strong>honest
evaluation</strong> as about the policy itself.</p>

{fig(H+"fig1_system_overview.png","Pipeline: logged transitions, feature encoder, fitted Q-iteration, guardrail relabel, distillation to a decision tree, then off-policy evaluation on held-out logs","(A) Learn from 74,733 logged steps. (B) Score each candidate on 5,000 held-out episodes with three estimators, after a sanity gate.", wide=True)}

<h2>Why the default is silence</h2>
{fig(H+"fig2_message_fatigue.png","Opt-out rate by messages already sent and by action","Opt-out rate in the logs roughly doubles at the third message, and sales actions carry about 1.5× the risk of service check-ins.", wide=True)}
<p>Opt-outs are 7.9% of logged steps at <strong>−62.6</strong> each, more than half the value of a
sale (+116.8). So an average message starts at about <strong>−5.6 expected value</strong> before any
upside. That reframes the problem: the policy's job is to prove that speaking beats staying quiet.
It is why <code>always_wait</code>, doing literally nothing, scores +1.10 and beats the old policy's
−13.46.</p>

<h2>Approach</h2>
<ol>
<li><strong>Fitted Q-Iteration</strong> (5 rounds, boosted trees) over <strong>74,733 logged
training steps</strong> from 24,000 episodes, using 31 features visible at decision time only.
Everything is evaluated on 15,565 held-out steps the model never saw.</li>
<li><strong>Guardrail relabelling.</strong> Hard product rules override the model's greedy action
on 31.3% of labels: escalate whenever the customer is unhappy or
<code>service_risk_score &gt; 0.7</code>. In the logs, escalation is the only action that pays when a
customer is unhappy (+21.0; every outbound message loses money).</li>
<li><strong>Distillation</strong> into a <strong>depth-10 decision tree</strong> (148 leaves, 85.5%
agreement with the full model), exported as one dependency-free Python file that a domain expert
can read.</li>
</ol>

<h2>Results</h2>
{fig(H+"fig3_main_results.png","Held-out value per policy with bootstrap intervals, and agreement between the direct-method and doubly robust estimators","Before scoring anything new, the evaluator had to recover the logged policy's known value: truth −13.46, estimate −13.21 (1.9% error).", wide=True)}
<p>Seven baselines were compared on <strong>5,000 held-out episodes</strong>. The shipped policy
scores <strong>+15.25</strong> per episode (95% CI +14.6 to +16.0) against <strong>−13.46</strong>
for the old policy, a gain of +28.7 per thread. Doubly robust gives +16.79 and SNIPS +11.32. All
three estimators rank the learned policy first; the direct method and doubly robust agree on the
full ranking to within 1.54 per episode. SNIPS differs only on the order of
<code>always_wait</code> and <code>simple_rule</code>.</p>

<h2>What each component costs and buys</h2>
{fig(H+"fig4_ablation.png","Cost of guardrails and distillation, and the effect of removing one component at a time", wide=True)}
<p>The unconstrained FQI teacher scores +21.06. Guardrails cost 4.9 and distillation 0.9: that is
the price of a policy that is auditable and rule-safe. Removing the learned model drops value by
14.2, while removing the runtime guardrails barely moves it, because the tree has already learned
them.</p>

{fig(H+"fig5_depth_sweep.png","Tree fidelity and held-out value by maximum depth", "Value flattens after depth 10: depth 14 more than doubles the leaves (376 vs 148) for +0.02.", wide=True)}

<h2>Where it wins, and where it does not</h2>
{fig(H+"fig6_slices.png","Held-out value by customer segment for four policies")}
<p>The shipped policy is best overall and on 3 of 6 segments (open estimates, weather extremes,
first touches). Most of the gain is on <strong>open estimates, +35.93 against +8.48</strong> for
hand-written rules. On unhappy customers every policy with the escalation rule scores between +18.6
and +23.3, and the starter rules score highest: the hard rule, not the learned model, is doing the
work. Hand-written rules also edge it on positive signals, and doing nothing is best on membership
renewal. Those are reported, not hidden.</p>

{fig(H+"fig7_action_distribution.png","Share of each action under the logged and shipped policies")}
<p>The behaviour change is large: estimate nudges fall from 31.8% to 2.3% of decisions, and volume
shifts to waiting, parking stale threads and scheduling. Measured on the shipped policy, it is not
the behaviour you might guess. Only <strong>27% of scheduling offers follow a positive
reply</strong>; most follow a stated objection (price, spouse or competitor).
<code>ASK_OBJECTION</code> is a proactive probe, with 93% of uses coming before the customer has
said anything. And every park comes from the hard rule, not the model.</p>

<h2>What this evaluation cannot prove</h2>
<ul>
<li><strong>No counterfactuals.</strong> The old policy almost never waited on turn 0 of an open
estimate, so the value of doing so is extrapolation, not measurement.</li>
<li><strong>Thin-data actions.</strong> Parking and escalation have the least logged support (297
and 350 rows), and the new policy uses both far more: parking goes from 1.9% to 25.7% of
decisions. That is where the estimates are weakest.</li>
<li><strong>Pushing a booking on an objecting customer.</strong> Because most scheduling offers
follow an objection, the likeliest real-world failure is an offer that reads as pushy. That is a
cost the logs price only through opt-outs.</li>
<li><strong>Distribution shift.</strong> If the new policy changes customer behaviour, the logs no
longer describe the world it operates in.</li>
</ul>
<p>The rollout plan follows from those limits: 5% of traffic, with opt-out rate and escalation
volume as the primary rollback triggers.</p>
"""},

{
 "slug":"travel-agent", "title":"Eval-Gated Skill Development",
 "category":"Agentic AI & LLM Systems",
 "tagline":"An agent-skills platform where every skill must prove its value on a 466-task bank before it can ship — A/B evals wired into CI gates at ~$0.03 per PR.",
 "short":"A skill does not merge unless an eval proves it helps. 17-skill registry, 466-task bank, 3-tier CI gates.",
 "image": D+"travel-agent.svg", "dates":"May 2026 – Jun 2026",
 "tags":["LangGraph","FastAPI","Streamlit","Langfuse","Thompson Sampling","CI/CD"],
 "links":[],
 "body": f"""
<p>Most agent "skills" are added on vibes: someone writes a prompt fragment, it looks better on
three examples, it ships. This project treats a skill like a code change — <strong>it does not
merge unless an eval proves it helps.</strong></p>

{fig(D+"travel-agent.svg","Eval-gated skill development pipeline")}

<h2>The platform</h2>
<p>A <strong>versioned 17-skill registry</strong> with a release CLI, and a LangGraph
travel-planning agent as the system under test. Versioning matters because a skill's effect is only
meaningful relative to a specific agent version and task set — without it, "this skill helps" is an
unfalsifiable claim.</p>

<h2>The measurement</h2>
<p>Each skill is scored <strong>with vs. without injection</strong>: the identical agent runs the
same tasks from a <strong>466-task bank</strong>, differing only in whether the skill is in
context. That difference is the skill's contribution, isolated from everything else. The top skill
measured at <strong>+17 points</strong>.</p>

<p>This runs as <strong>3-tier CI gates</strong> — a cheap smoke tier, a regression tier, then the
full bank — so most pull requests are settled by the cheap tier and the full run is reserved for
changes that survive it. The whole gate costs about <strong>$0.03 per PR</strong>, which is what
makes running it on every change realistic rather than aspirational.</p>

<h2>Optimization</h2>
{fig(D+"travel-agent-results.svg","Thompson sampling score lift")}

<p>A <strong>Thompson-sampling optimizer</strong> over skill selection lifted mean task score from
<strong>0.33 to 0.60</strong>. Thompson sampling suits this well: skill performance is uncertain
and unevenly sampled, and the sampler naturally spends its budget on skills whose value is still
ambiguous rather than re-confirming known winners.</p>

<p>Separately, <strong>13.9K collected traces</strong> exposed and retired a router that was
<strong>misrouting 35% of tasks</strong> — a failure invisible in aggregate score, and only
findable because the traces were there to inspect.</p>
"""},

{
 "slug":"agentpay", "title":"AgentPay",
 "category":"Agentic AI & LLM Systems",
 "tagline":"An autonomous agent economy where AI agents discover, hire, and pay each other on-chain, with reputation staked as collateral against bad work.",
 "short":"Agents hire and pay each other on-chain. Reputation is bonded capital, so cheating is economically punished rather than merely recorded.",
 "image": D+"agentpay.svg", "dates":"Feb 2026",
 "tags":["Rust","Anchor","Solana","Avalanche","LangChain","Next.js","D3.js"],
 "links":[("Live demo","https://agent-pay-lake.vercel.app/"),("GitHub","https://github.com/Pushks18/AgentPay")],
 "body": f"""
<p><strong>AgentPay</strong> is a decentralized agent economy: agents autonomously discover one
another, negotiate work, and settle payment on-chain — no human in the loop. Built at the
<strong>Southern California Blockchain Hackathon (SCBC 2026)</strong>.</p>

{fig(D+"agentpay.svg","AgentPay architecture")}

<h2>The trust problem</h2>
<p>If an agent hires another agent, what stops the callee from taking payment and returning
garbage? There is no shared principal to appeal to, and no reputation system that a fresh keypair
cannot escape.</p>

<p>AgentPay answers this with <strong>escrow plus stake slashing</strong>. Reputation is a
<em>bonded</em> asset rather than a score in a database — an agent must put capital at risk to
participate, and dishonest work destroys that capital. This makes cheating economically punished
rather than merely recorded, and makes a throwaway identity expensive instead of free.</p>

<h2>Architecture</h2>
<ul>
<li><strong>Smart contract layer</strong> — Rust/Anchor programs on Solana and Avalanche
implementing the agent registry, escrow accounts, reputation staking, and slashing conditions.</li>
<li><strong>Agent orchestration</strong> — LangChain multi-agent workflows with custom
<code>x402</code> payment tooling, achieving sub-30s end-to-end cycles from discovery through
settlement.</li>
<li><strong>Live visualizer</strong> — a Next.js + D3.js dashboard streaming agent interactions,
network topology, and payment flows over WebSockets.</li>
</ul>
"""},

]


PROJECTS += [
{
 "slug":"warp-tote", "title":"Warehouse Tote Perception",
 "category":"Computer Vision & Perception",
 "tagline":"A four-stage vision pipeline for a robotic pack station: find the tote, segment what is in it, decide what is an item, and place the suction cup — 0.958 pick score at 619 ms on a laptop.",
 "short":"Where should the suction cup land? FastSAM proposals, a 2-of-3 tote/item vote, and a distance-transform pick point: 0.958 pick score vs 0.31 baseline.",
 "image": W+"fig12_stages.jpg", "dates":"Aug 2026",
 "tags":["FastSAM","OpenCV","PyTorch","Segmentation","Robotic Picking","Python"],
 "links":[("GitHub","https://github.com/Pushks18/warp-robotics")],
 "body": f"""
<p>Given a top-down photo of a warehouse tote, the pipeline answers three questions: what is in
there, where should the suction cup land, and is this a tote the robot should attempt at all.
Built for the Warp Robotics perception challenge on 120 images from Amazon's
<strong>ARMBench</strong>. It runs fully locally, with no hosted models.</p>

<p>On the dev split it reaches a <strong>pick score of 0.958</strong> (108 correct picks, 5 wrong,
7 flagged) against 0.31 for flagging every tote, and a detection F1 of 0.589. Bootstrapping the 120
images gives a 90% interval of 0.925–0.983 for the pick score.</p>

{fig(W+"fig12_stages.jpg","A sparse, a crowded and an empty tote at each of the four stages","One sparse, one crowded and one empty tote at each stage. FastSAM proposes about a hundred regions per image; the vote and set cover keep the items. The empty tote is flagged because nothing survives the vote.", wide=True)}

<h2>How it works</h2>
<ol>
<li><strong>Find the tote.</strong> The crop is keyed on <em>bright OR saturated</em>, not on tote
colour, because keying on the vivid yellow and blue bins failed on 16 of 120 images: some totes
are beige. It keeps <strong>every item pixel on all 120 images</strong> while discarding ~14% of
each frame.</li>
<li><strong>Propose regions.</strong> FastSAM-x over the crop. A class-agnostic segmenter is the
right tool, since the ground truth has no category labels: the task is "where does one thing end
and the next begin", not "find the bottle". MobileSAM's automatic mode took 20.6 s per image,
which would have been 41 minutes per pass over the split.</li>
<li><strong>Decide what is an item.</strong> Masks are kept by a <strong>2-of-3 vote</strong> over
three cues measured on 604 labelled masks: chromatic distance from the tote colour (0.859 balanced
accuracy), chromatic spread within the mask (0.870) and edge density (0.840). The vote reaches
0.908, beating every AND/OR chain tried, and overlaps are resolved by greedy set cover.</li>
<li><strong>Choose the pick.</strong> The suction point is the peak of the item's distance
transform, the point furthest from any edge.</li>
</ol>

<h2>What each stage buys</h2>
{fig(W+"fig01_ablation.png","Cumulative ablation of detection F1 and pick score","Each row adds one stage to the row above. The mask-level chroma filter alone is worth +0.21 F1 and +0.27 pick score.", wide=True)}

<h2>Why not the centre of mass</h2>
{fig(W+"fig14_pick_point.jpg","Distance-transform peak versus centre of mass on a bent item")}
<p>A suction cup needs the flattest, most continuous surface to seal on, and the grader erodes each
item by 4 px before testing the pick. Across the 637 masks the pipeline detects, the centre of mass
lands off its own item <strong>39 times (6.1%)</strong>; the distance-transform peak
<strong>never does</strong>, by construction.</p>

<h2>Clutter, and an error that changes sign</h2>
{fig(W+"fig03_clutter.png","Detection F1 and predicted boxes per item by clutter level")}
<p>F1 falls from 0.875 on empty totes to 0.354 at 11+ items, but the boxes-per-item ratio crosses
1.0: sparse totes are cut into too many pieces, crowded ones into too few. One declining curve is
hiding two different errors. Picking stays at 0.93–1.00 across every clutter level, because a
pick only has to land on <em>a</em> real item.</p>

<h2>Measured, not claimed</h2>
{fig(W+"fig05_flag_policy.png","Pick confidence of correct and wrong picks, and points lost by every flag threshold", "Flagging costs 0.25 on a tote with items, so a confidence gate must be right more than 3 times in 4. Four of the five wrong picks are more confident than the median correct one, and every gate setting loses points.", wide=True)}
<p>So the pipeline flags only when nothing survives detection, which correctly flags 7 of 8 empty
totes. My confidence score measures pick quality, not the probability of being right; making it
calibrated is the highest-value next step.</p>

{fig(W+"fig04_robustness.png","Detection F1 and pick score with the tote recoloured")}
<p>To test the colour-agnostic claim, I recoloured every tote to colours that appear nowhere in
the split, leaving the items and the grader untouched. Hue costs nothing: green and magenta land
within one bootstrap standard error. Grey and white bins cost ~0.11 F1, since they remove the
strongest cue. That is exactly the loss the 2-of-3 vote was designed to survive.</p>

<h2>Where it fails</h2>
{fig(W+"fig13_failures.jpg","Four failure modes: definition mismatch, occlusion, merged lookalikes, and a non-item at the frame edge","Ground truth above, this pipeline below. Images: ARMBench (Amazon), CC BY 4.0.", wide=True)}
<p>The dominant failure is a <strong>definition mismatch</strong>, not a segmentation error: an
item is one pickable unit, but a class-agnostic segmenter cannot know that clear plastic is a
container. Four targeted attempts to raise F1, each aimed at a different stage, moved it by at most
+0.004, and adding more proposals made it worse. The remaining error is in the segmenter's notion
of an object, so the fixes are fine-tuning on ARMBench's instance labels and depth sensing for
heavily occluded totes.</p>

<h2>Latency</h2>
<p><strong>619 ms median</strong> (908 ms p95) per image on an unloaded M4 MacBook Air with no GPU.
On battery, the more pessimistic condition, steady state is 711 ms median and 1,045 ms p95, still
under a second. The very first run after a fresh install is about 2.4× slower (1,676 ms median),
because Metal kernels compile on first use. The two runs produce byte-identical outputs; only the
clock differs.</p>
"""},

{
 "slug":"dp-adult", "title":"Differentially Private Analysis of the UCI Adult Dataset",
 "category":"Privacy & Trustworthy ML",
 "tagline":"A count, a top-3 selection, and a logistic regression released under pure ε-differential privacy with IBM diffprivlib — plus an empirical study of what each design decision actually costs.",
 "short":"Three DP releases budget-capped at ε = 3, a differencing attack that shows why the cap matters, and an ablation that proved my own budget hypothesis backwards.",
 "image": D+"dp-adult.svg", "dates":"Sep 2026",
 "tags":["Differential Privacy","diffprivlib","scikit-learn","Python"],
 "links":[],
 "body": f"""
<p>Three releases over 30,162 census records: how many people earn over $50K, the three most
common occupations among them, and a logistic regression predicting income. Every mechanism comes
from IBM <code>diffprivlib</code>; none is hand-implemented. Beyond building them, the study
measures <strong>what each design decision costs</strong>, using 1,200–3,000 trials per sampling
experiment and 25 private refits per ε for the model.</p>

{fig(D+"dp-adult.svg","Three DP releases under one privacy budget")}

<h2>Why the budget is not bookkeeping</h2>
<p>A <strong>differencing attack</strong> asks two aggregate queries that differ by one person and
subtracts them. Without DP the target is exposed on the first query. At ε = 1 one query pair leaks
only a little (64.7% attacker accuracy against 50% chance), but <strong>100 repetitions reach
99.8%</strong>: averaging defeats the noise. Noise stops the single query; only an enforced budget
stops the repeated one. So a <code>BudgetAccountant</code> caps the three releases at
<strong>ε = 3</strong> and refuses a fourth query.</p>
{fig("assets/teppit/figures/fig1_threat_model.png","Differencing attack accuracy vs repeated queries, and released-count distributions","(a) attacker accuracy vs repeated query pairs, 1,500 trials per cell; (b) released count on a log density axis.")}

<h2>Top-3 selection: the margin decides</h2>
<p>A list of names cannot be noised directly, so three selection mechanisms were compared at
matched total ε. The <strong>noisy histogram with report-noisy-max</strong> wins at every ε below 1
(93.3% exact recovery at ε = 0.1, against 78.3% for PermuteAndFlip and 65.2% for the exponential
mechanism), even when handicapped with twice the sensitivity. The reason is parallel composition:
the 14 disjoint buckets cost ε once, while peeling splits ε three ways. PermuteAndFlip beating the
exponential mechanism matches McKenna &amp; Sheldon (2020).</p>
{fig("assets/teppit/figures/fig2_selection.png","Selection mechanism comparison and rank stability","(a) exact top-3 recovery, 1,200 trials per ε; (b) how often each occupation appears in the released top-3.")}
<p>Every failure in that table is the same swap: <strong>Sales (970) and Craft-repair (908), 62
people apart</strong>, trading third place. Selection accuracy is set by the margin between
candidates, not by dataset size.</p>

<h2>Accuracy hides sign errors</h2>
{fig("assets/teppit/figures/fig3_model_stability.png","Coefficient and accuracy spread over 25 private refits per epsilon", wide=True)}
<p>At ε = 0.01 the mean accuracy is 0.69, but individual runs land anywhere from 0.57 to 0.79.
Worse, the coefficients span roughly −17 to +20, and the median <code>hours_per_week</code>
coefficient is <strong>negative</strong>: the model learned the opposite of the true relationship
while still scoring 0.69, because 75% of people are in the majority class. By ε = 0.5 it is
indistinguishable from the non-private 0.784.</p>

<h2>Ablations</h2>
{fig("assets/teppit/figures/fig4_ablations.png","Ablations: sensitivity bug, per-task saturation, and public bounds", wide=True)}
<ul>
<li><strong>A bug that improves your metrics.</strong> The histogram's L1 sensitivity is 2; using
1 is a natural mistake. The wrong setting scores <em>better</em> at every ε (93.3% vs 75.6% at
ε = 0.05) while silently spending twice the claimed ε, and nothing in the output reveals it.
Δ = 1 at ε = 0.05 and Δ = 2 at ε = 0.10 both score exactly 93.3%, since both give noise scale
20.</li>
<li><strong>A hypothesis that turned out backwards.</strong> I expected starving the cheap count and
feeding the model to beat an equal split. It does not: the model saturates around ε = 0.25–0.5,
while the count keeps improving across the whole range. The better split is count 0.7 / top-3 0.3
/ model 0.5, a <strong>total of ε = 1.5</strong>: half the privacy cost with comparable utility.</li>
<li><strong>Correctness is free.</strong> Bounds taken from public metadata instead of the data
cost nothing measurable. Even deliberately loose bounds (age 0–120, hours 0–168) cost 0.0002
accuracy, well inside run-to-run noise.</li>
</ul>

<h2>Two leaks that noise does not fix</h2>
<ul>
<li><strong>Histogram keys.</strong> Two occupations have exactly one high earner. Iterating over
the categories <em>present in the data</em> would reveal that person through the key alone, however
much noise the value gets. The histogram iterates over a fixed public list of 14 occupations and
noises the empty buckets too.</li>
<li><strong>Norm bounds.</strong> A <code>data_norm</code> inferred from the training data is a
statistic about the most extreme person, released in the clear. Features are scaled with public
schema ranges and clipped, bounding every row's norm by √3 without looking at the data.</li>
</ul>
"""},

{
 "slug":"infodistill", "title":"InfoDistill",
 "category":"Agentic AI & LLM Systems",
 "tagline":"An agentic research-summarization platform that extracts, classifies, and condenses technical articles using BART and zero-shot classification.",
 "short":"Raw feeds to readable digest. Zero-shot classification means the topic taxonomy can change without retraining.",
 "image": D+"infodistill.svg", "dates":"2025",
 "tags":["FastAPI","Hugging Face","BART","Zero-Shot","React","Python"],
 "links":[("Live site","https://info-distill.vercel.app/"),("GitHub","https://github.com/Pushks18/Info-Distill")],
 "body": f"""
<p><strong>InfoDistill</strong> automates the whole path from raw source to readable digest: pull
technical articles from multiple feeds, classify them by topic, and summarize them.</p>

{fig(D+"infodistill.svg","InfoDistill pipeline")}

<p>Classification is <strong>zero-shot</strong> rather than a trained classifier, which means new
topic labels can be added without collecting labeled data or retraining — an important property
when the taxonomy of "things worth reading" shifts every few months. Summarization runs on
<strong>BART</strong>, chosen for abstractive quality on long-form technical prose rather than
extractive sentence-picking.</p>

<p>The FastAPI backend composes the stages so extraction, classification, and summarization can
each be run and debugged independently — which matters because these failure modes look identical
from the outside: a bad digest could be a parse failure, a misclassification, or a bad summary.</p>
"""},

{
 "slug":"nei-slam", "title":"Real-Time Visual SLAM with Learned Features",
 "category":"Computer Vision & Perception",
 "tagline":"Monocular VO on an XFeat/LighterGlue frontend, NetVLAD loop closure, and a C++ GTSAM factor-graph backend — ~95 m to ~1.2 m ATE on KITTI.",
 "short":"Learned features survive motion blur where ORB and SIFT do not; a factor graph lets loop closures correct drift retroactively.",
 "image": D+"slam.svg", "dates":"Nov 2025 – May 2026",
 "tags":["C++","GTSAM","PyTorch","OpenCV","XFeat","NetVLAD","FAISS","CMake"],
 "links":[],
 "body": f"""
<p>Built during my research assistantship at <strong>USC</strong> on the NEI smart-glasses platform.
The goal was a monocular SLAM stack that survives what a wearable actually sees: motion blur,
sudden rotation, and no reliable depth sensor.</p>

{fig(D+"slam.svg","Visual SLAM architecture")}

<p>Two decisions drive the design. Classical hand-crafted detectors (ORB, SIFT) degrade badly under
blur, so the frontend runs <strong>learned features</strong>. And the backend is a <strong>factor
graph</strong> rather than a filter, so loop closures and sparse depth can correct drift
<em>retroactively</em> — a filter would have already marginalized that information away.</p>

<h2>What each stage does</h2>
<ul>
<li><strong>VO frontend</strong> — XFeat keypoints with LighterGlue matching per frame pair, then
<code>findEssentialMat</code> (RANSAC) and <code>recoverPose</code> for relative rotation and
translation. Translation is unit-norm; metric scale is recovered later in the backend.</li>
<li><strong>Simulated ToF depth</strong> — rather than relying on a 360° LiDAR the wearable does
not have, depth comes from the stereo pair via OpenCV SGBM disparity
(<code>Z = fx · baseline / d</code>), sampled on a 4×4 grid over the central image region to emit
16 <code>(u, v, Z)</code> tuples per frame.</li>
<li><strong>Place recognition</strong> — every 10th frame becomes a keyframe with a 64-cluster
NetVLAD descriptor (VGG16 conv5_3 → NetVLAD → L2-normalized, dim 32768), indexed in FAISS. Top-5 L2
search, rejecting anything within 100 frames of the current pose.</li>
<li><strong>Loop verification</strong> — candidates are re-matched with XFeat and pose-checked,
accepted only at ≥150 RANSAC inliers <strong>and</strong> ≥0.25 inlier ratio. Only the rotation is
kept: the loop factor uses tight rotation noise (σ = 0.1 rad) and effectively-free translation
(σ = 100 m), so metric scale stays anchored to GPS and depth rather than leaking in through loop
closures.</li>
<li><strong>C++ GTSAM backend</strong> — a <code>NonlinearFactorGraph</code> combining a prior at
the origin, <code>BetweenFactorPose3</code> odometry with noise scaled by inverse inlier ratio,
<code>GenericProjectionFactor</code> for each depth point under a Huber-robust 4px cost, periodic
<code>GPSFactor</code> constraints, and loop-closure between-factors — solved with
Levenberg–Marquardt.</li>
</ul>

<h2>Results</h2>
{fig(D+"slam-results.svg","Trajectory error reduction")}

<p>Evaluated as ATE against KITTI sequence 00 ground truth with Umeyama scale alignment, the
standard protocol for monocular trajectories. Debugging sensor noise, calibration drift, and VO
failures also reduced tracking dropouts by ~30%.</p>
"""},

{
 "slug":"godot-mcp", "title":"Godot MCP",
 "category":"Developer Tools & Open Source",
 "tagline":"An MCP server letting LLM agents drive the Godot 4 engine in natural language — 30+ tools behind strict path validation.",
 "short":"LLM agents control a game engine. The tool boundary is the security boundary, so it has to hold even when the model is wrong.",
 "image": D+"godot-mcp.svg", "dates":"Apr 2026 – Present",
 "tags":["TypeScript","Node.js","MCP","Godot 4","CI/CD"],
 "links":[("GitHub","https://github.com/Pushks18/Godot-MCP-Pilot")],
 "body": f"""
<p>An MCP server that lets LLM agents (Claude, Cursor) control <strong>Godot 4</strong> projects
through natural language. Used by <strong>10+ active users</strong>.</p>

{fig(D+"godot-mcp.svg","Godot MCP architecture")}

<h2>Design</h2>
<p><strong>30+ tools</strong> span scene manipulation, script authoring, project execution, and
asset management — enough surface area for end-to-end 2D and 3D workflow automation rather than a
demo that can only do one thing.</p>

<p>The part that needed the most care is <strong>path validation</strong>. An agent with write
access to a project directory and a natural-language interface is one hallucinated path away from
writing outside the project. Every filesystem-touching tool validates and sandboxes its paths, and
routing is structured rather than string-assembled — the tool boundary is the security boundary, so
it has to hold even when the model is wrong.</p>

<p>Beyond the tools: CI/CD, auto-config detection so the server finds a Godot install without
manual setup, and multi-client integration so the same server works across IDEs.</p>
"""},

{
 "slug":"defillama", "title":"DefiLlama SDK — RPC Reliability &amp; Failover",
 "category":"Developer Tools & Open Source",
 "tagline":"Open-source contribution redesigning RPC endpoint resolution and adding runtime quarantine with cooldown to a production Web3 SDK.",
 "short":"User endpoints were silently overridden by defaults. Fixed resolution order, then added quarantine so one bad provider cannot degrade everything.",
 "image": D+"defillama.svg", "dates":"Apr 2026",
 "tags":["TypeScript","Node.js","Web3","Jest","Open Source"],
 "links":[("GitHub","https://github.com/DefiLlama/defillama-sdk")],
 "body": f"""
<p>A contribution to the <strong>DefiLlama SDK</strong>, a widely-used TypeScript library for
on-chain data access, fixing how the SDK resolves and recovers from RPC endpoints.</p>

{fig(D+"defillama.svg","RPC resolution and failover")}

<h2>The bug</h2>
<p>User-supplied RPC endpoints were being silently overridden by defaults (<em>Fixes #162</em>). If
you configured your own node — typically because you were paying for reliability the public
endpoints do not provide — the SDK could ignore it. Worse, it failed silently: you would see
degraded performance with no signal that your configuration was not being used. I redesigned the
chain RPC resolution logic so user-defined endpoints correctly take priority.</p>

<h2>Failover</h2>
<p>Beyond the fix, dead endpoints were retried indefinitely, so a single bad RPC could degrade every
downstream call. I added <strong>runtime RPC quarantine</strong>: an endpoint that fails 5 times is
pulled from rotation for a 10-minute cooldown, then allowed back.</p>

<p>The cooldown is the important detail. Permanently blacklisting a failing endpoint is wrong — most
RPC failures are transient, and a provider having a bad minute should not be discarded for the life
of the process. Quarantine bounds the blast radius without making the decision irreversible.</p>

<p>Shipped with <strong>8 unit tests</strong> covering both override precedence and the
failure-handling paths, plus expanded documentation on RPC configuration.</p>
"""},
]

# display order: category order on the site follows first appearance here
_ORDER = ["hvac", "warp-tote", "nei-slam", "dp-adult", "travel-agent", "agentpay",
          "infodistill", "godot-mcp", "defillama"]
PROJECTS.sort(key=lambda p: _ORDER.index(p["slug"]))
