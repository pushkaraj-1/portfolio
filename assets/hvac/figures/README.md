# Portfolio figures and tables

Every figure comes as PNG (300 dpi, for the website), SVG (scales cleanly), and PDF (for a paper or slides).
Tables come as PNG + SVG, and as Markdown in `tables.md`.

Regenerate everything with `python make_figures.py`. The numbers live in `results.json`, produced by
the project's offline evaluator on the held-out split (5,000 episodes, 15,565 steps).

## Suggested order and captions

**Figure 1. System overview** (`fig1_system_overview`)
(A) A Q-function is fit to the old policy's logs with Fitted Q-Iteration. Its greedy actions are relabelled by hard product rules, and the result is distilled into a depth-10 decision tree exported as plain Python. (B) Each candidate policy is scored on a held-out split by three off-policy estimators. The evaluator first has to recover the logged policy's known value (−13.46; it estimates −13.21).

**Figure 2. Message fatigue** (`fig2_message_fatigue`)
Opt-out rate on outbound messages in the logs. (a) The rate roughly doubles at the third message (6.4% → 13.2%). (b) Sales actions carry about 1.5× the risk of service check-ins. At −62.6 per opt-out, an average message starts at about −5.6 expected value.

**Table 1. Outcome structure** (`table1_outcomes`)
Opt-outs are 7.9% of steps at −62.6 each, more than half the value of a sale (+116.8).

**Table 2. Unhappy customers** (`table2_unhappy_customers`)
When the customer is unhappy, every outbound action loses money and only escalation pays (+21.0). This is why escalation is a hard rule.

**Table 3. Evaluator sanity check** (`table3_sanity_check`)
Scored on its own logs, the old policy's value is recovered within 1.9%.

**Table 4 / Figure 3. Main results** (`table4_main_results`, `fig3_main_results`)
The shipped policy earns +15.25 per thread (DR +16.79, 95% CI [+14.6, +16.0]) against −13.46 for the logged policy and +1.10 for sending nothing. DM and DR agree within 1.54 on every policy.

**Table 5 / Figure 4. Ablation** (`table5_ablation`, `fig4_ablation`)
(a) The unconstrained FQI teacher scores +21.06. Guardrails cost 4.9 and distillation to a tree costs 0.9: the price of an auditable, rule-safe policy. (b) Removing the learned model drops value by 14.2. The runtime guardrails barely move the number because the tree already learned them.

**Table 8 / Figure 5. Distillation depth** (`table8_depth_sweep`, `fig5_depth_sweep`)
Value flattens after depth 10: depth 14 more than doubles the leaves (376 vs 148) for +0.02.

**Table 6 / Figure 6. Customer segments** (`table6_slices`, `fig6_slices`)
The shipped policy is best on 3 of 6 segments and overall. Most of the gain is on open estimates (+35.93 vs +8.48). Hand-written rules still win on unhappy customers and positive signals. Doing nothing is best on membership renewal.

**Figure 7 / Table 7. Behaviour change and data support** (`fig7_action_distribution`, `table7_action_support`)
The shipped policy cuts estimate nudges from 31.8% to 2.3% of decisions. It shifts volume to waiting, parking stale threads, and scheduling. The two terminal actions (park, escalate) have the least logged data, and the new policy uses both more.
