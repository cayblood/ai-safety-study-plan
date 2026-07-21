# ML Foundations Track — 2 hrs/day, 5 days/week (Math Academy)

The empirical half of the plan rests on genuinely solid math. The backbone is [Math Academy](https://mathacademy.com)'s four-course sequence — mastery-based, adaptive, and honest about prerequisites:

1. [Mathematical Foundations I](https://mathacademy.com/courses/mathematical-foundations-i) — **in progress, ~80% complete**
2. [Mathematical Foundations II](https://mathacademy.com/courses/mathematical-foundations-ii)
3. [Mathematical Foundations III](https://mathacademy.com/courses/mathematical-foundations-iii)
4. [Mathematics for Machine Learning](https://mathacademy.com/courses/mathematics-for-machine-learning)

## How this track works

- **2 hours/day, 5 days/week**, aiming for roughly 100–150 XP/day (their XP ≈ minutes of focused work) — a significant step up from previous pace, so the sequence should move noticeably faster. Do it *before* the mech interp block when possible — math first, applied second.
- Trust the diagnostic and the spaced-repetition reviews. Do not skip reviews to chase new topics; retention is the entire value proposition.
- When a course reaches a topic that mech interp uses directly (below), pause for a short "bridge" session connecting it to transformer internals.

## Bridge points (where this track feeds the mech interp track)

| Math Academy topic | Mech interp payoff |
|---|---|
| Linear algebra (MF II–III): matrix decompositions, SVD, change of basis, rank | Reading weight matrices, low-rank structure, residual stream geometry |
| Multivariable calculus (MF III): gradients, Jacobians, chain rule | Backprop, attribution methods, gradient-based patching |
| Probability (MF II–III): distributions, expectation, KL divergence | Loss functions, logit lens, calibration |
| MML: optimization, gradient descent variants | Training dynamics, fine-tuning behavior |
| MML: regression, classification, regularization | Linear probes (the workhorse of applied interp) |
| MML: neural networks | ARENA Chapter 1.1's transformer-from-scratch |

## Milestones

1. **Weeks 1–3:** finish the last ~20% of Mathematical Foundations I.
2. **Months 1–4:** Mathematical Foundations II. The linear algebra here is the first big mech interp payoff — don't wait for it to arrive on its own; the 3Blue1Brown supplement covers the geometric intuition ARENA needs in the meantime.
3. **Months 4–7:** Mathematical Foundations III (multivariable calculus, more linear algebra, probability) — in parallel with mech interp Phase 2 mini-projects.
4. **Months 7+:** Mathematics for Machine Learning. This overlaps the MATS application sprint; that's fine — by then the mech interp track is the priority and this course becomes consolidation.

Pacing note: at ~500–600 XP/week these estimates are rough — the adaptive diagnostic and per-course XP totals will give real dates within the first couple of weeks. The plan doesn't require the whole sequence to be finished before research starts; mech interp Phase 1 needs only comfortable linear algebra intuition.

Supplement (optional, only when stuck): [3Blue1Brown Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) and [Neural Networks](https://www.3blue1brown.com/topics/neural-networks) series for geometric intuition.
