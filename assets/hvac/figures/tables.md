# Result tables

All values from the offline evaluator on the held-out split (5,000 episodes, 15,565 steps) unless noted.

**Table 1. Outcome structure of the logged data (90,298 steps)**

| Outcome | Steps | Share | Mean reward |
|:--|--:|--:|--:|
| Continue (no reply yet) | 61,298 | 67.9% | −2.6 |
| Episode hit 4 steps | 12,181 | 13.5% | −3.3 |
| Opted out | 7,136 | 7.9% | −62.5 |
| Booked appointment | 2,343 | 2.6% | +33.4 |
| Escalated to human | 2,178 | 2.4% | −15.6 |
| Sold estimate | 1,648 | 1.8% | +116.8 |
| Parked | 1,574 | 1.7% | −5.5 |
| Positive review | 1,300 | 1.4% | +9.8 |
| Membership converted | 640 | 0.7% | +18.1 |

**Table 2. Logged reward when the customer is unhappy**

| Action taken | n | Mean reward |
|:--|--:|--:|
| ESCALATE_TO_HUMAN | 164 | +21.0 |
| WAIT | 257 | −0.1 |
| MEMBERSHIP_TOUCH | 193 | −7.3 |
| PARK_THREAD | 50 | −7.8 |
| CHECK_IN | 911 | −11.5 |
| ASK_OBJECTION | 382 | −17.4 |
| ESTIMATE_NUDGE | 676 | −18.8 |
| OFFER_SCHEDULING | 357 | −23.5 |

**Table 3. Evaluator sanity check (target policy = logging policy)**

| Quantity | Value |
|:--|--:|
| Empirical mean episode return (ground truth) | −13.46 |
| FQE estimate at turn 0 | −13.21 |
| Absolute error | 0.26 (1.9%) |
| SNIPS with π = π_β | −4.33 |
| Empirical mean reward per step | −4.33 |

**Table 4. Off-policy value on 5,000 held-out episodes**

| Policy | DM / episode | 95% CI | DR / episode | SNIPS / step | ESS | Send rate |
|:--|--:|--:|--:|--:|--:|--:|
| Shipped: distilled FQI + guardrails | +15.25 | [+14.6, +16.0] | +16.79 | +11.32 | 1,448 | 46.9% |
| Hand-written rule policy | +4.35 | [+4.0, +4.7] | +5.55 | +3.68 | 1,253 | 25.3% |
| always_wait | +1.10 | [+0.9, +1.2] | +0.90 | −0.18 | 1,031 | 0.0% |
| simple_rule | −3.71 | [−4.2, −3.3] | −3.79 | +1.07 | 2,547 | 78.6% |
| always_park | −8.79 | — | −8.86 | −5.70 | 297 | 0.0% |
| always_escalate | −19.13 | — | −19.08 | −16.17 | 345 | 0.0% |
| always_check_in | −19.58 | — | −19.45 | −4.57 | 1,946 | 100.0% |
| always_estimate_nudge | −46.39 | — | −46.53 | −10.50 | 3,386 | 100.0% |
| Logged policy | −13.46 | — | — | −4.33 | 15,565 | 89.2% |

**Table 5. Component ablation (held-out)**

| Variant | DM / episode | Δ DM | DR / episode | SNIPS / step | Send rate |
|:--|--:|--:|--:|--:|--:|
| Shipped: guardrails + tree (d=10) | +15.25 | — | +16.79 | +11.32 | 46.9% |
| − guardrails (tree alone) | +15.24 | −0.01 | +16.53 | +11.07 | 49.2% |
| − escalation rule | +15.60 | +0.35 | +16.82 | +11.32 | 47.0% |
| − membership rule | +15.14 | −0.11 | +16.60 | +11.25 | 48.7% |
| − learned model (rules, else WAIT) | +1.07 | −14.18 | +1.55 | +0.71 | 3.1% |
| FQI teacher, no guardrails | +21.06 | +5.81 | +22.31 | +13.34 | 56.5% |
| FQI teacher + guardrails (not distilled) | +16.14 | +0.89 | +17.85 | +12.08 | 42.3% |

**Table 6. DM value per episode by customer segment (best per row in bold)**

| Slice | Steps | Episodes | Shipped (ours) | Rule policy | always_wait | simple_rule |
|:--|--:|--:|--:|--:|--:|--:|
| Open estimates | 5,377 | 1,671 | +35.93 | +8.48 | +4.57 | +2.88 |
| Turn 0 only | 5,000 | 5,000 | +14.59 | +1.66 | −2.04 | +5.02 |
| Weather extreme | 1,860 | 606 | +5.61 | −2.21 | −1.07 | −5.82 |
| Positive signal | 1,438 | 1,202 | +14.21 | +15.72 | +0.32 | −0.64 |
| Unhappy customers | 535 | 432 | +18.56 | +20.36 | −3.60 | +23.31 |
| Membership renewal | 1,920 | 630 | −1.29 | −0.39 | +0.40 | −11.07 |
| Overall | 15,565 | 5,000 | +15.25 | +4.35 | +1.10 | −3.71 |

**Table 7. Data support per action vs how often the shipped policy uses it**

| Action | Logged rows | Logged share | Shipped share |
|:--|--:|--:|--:|
| ESTIMATE_NUDGE | 4,945 | 31.8% | 2.3% |
| ASK_OBJECTION | 3,201 | 20.6% | 9.3% |
| CHECK_IN | 2,846 | 18.3% | 3.7% |
| OFFER_SCHEDULING | 2,097 | 13.5% | 17.4% |
| WAIT | 1,048 | 6.7% | 22.5% |
| MEMBERSHIP_TOUCH | 781 | 5.0% | 14.1% |
| ESCALATE_TO_HUMAN | 350 | 2.2% | 4.9% |
| PARK_THREAD | 297 | 1.9% | 25.7% |

**Table 8. Distillation depth sweep**

| Depth | Leaves | Fidelity | Weighted F1 | DM / episode | DR / episode |
|:--|--:|--:|--:|--:|--:|
| 2 | 3 | 27.8% | 22.5% | −7.26 | −6.76 |
| 4 | 9 | 64.6% | 67.0% | +11.85 | +12.94 |
| 6 | 27 | 75.9% | 76.0% | +13.87 | +15.62 |
| 8 | 67 | 81.5% | 82.6% | +14.96 | +16.72 |
| 10 | 148 | 85.5% | 86.7% | +15.25 | +16.79 |
| 14 | 376 | 87.9% | 88.6% | +15.27 | +16.91 |
