# ML Foundations Track — 2 hrs/day, 5 days/week (Math Academy)

The empirical half of the plan rests on genuinely solid math. [Math Academy](https://mathacademy.com)'s **Foundations of Machine Learning** sequence (Mathematical Foundations I–III → Machine Learning) is the backbone here: mastery-based, adaptive, and honest about prerequisites, which makes it a good fit for filling gaps quickly without re-taking whole courses.

## How this track works

- **2 hours/day, 5 days/week** on Math Academy, aiming for roughly 100–150 XP/day (their XP ≈ minutes of focused work). Do it *before* the mech interp block when possible — math first, applied second.
- Trust the diagnostic and the spaced-repetition reviews. Do not skip reviews to chase new topics; retention is the entire value proposition.
- When Math Academy's ML course reaches a topic that mech interp uses directly (below), pause for a short "bridge" session connecting it to transformer internals.

## Bridge points (where this track feeds the mech interp track)

| Math Academy topic | Mech interp payoff |
|---|---|
| Linear algebra: matrix decompositions, SVD, change of basis, rank | Reading weight matrices, low-rank structure, residual stream geometry |
| Multivariable calculus: gradients, Jacobians, chain rule | Backprop, attribution methods, gradient-based patching |
| Probability: distributions, expectation, KL divergence | Loss functions, logit lens, calibration |
| Optimization: gradient descent variants | Training dynamics, fine-tuning behavior |
| ML course: regression, classification, regularization | Linear probes (the workhorse of applied interp) |
| ML course: neural nets from scratch | ARENA Chapter 1.1's transformer-from-scratch |

## Milestones

1. **Month 1–2:** clear any diagnostic gaps in algebra/precalc remnants; core linear algebra to comfort with SVD and eigendecomposition.
2. **Month 3–4:** multivariable calculus + probability; start Math Academy's ML content.
3. **Month 5+:** Foundations of ML course proper — regression → neural networks, in parallel with mech interp Phase 2 mini-projects.

Supplement (optional, only when stuck): [3Blue1Brown Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) and [Neural Networks](https://www.3blue1brown.com/topics/neural-networks) series for geometric intuition.
