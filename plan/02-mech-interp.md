# Mechanistic Interpretability Track — 2 hrs/day, 5 days/week

Based on Neel Nanda's [How to become a mechanistic interpretability researcher](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher) (Sept 2025), revised for the field as of mid-2026. The core philosophy is preserved: **learn the minimum viable basics, then do research**. Mech interp is an empirical field — the feedback loops that matter come from building things, not from reading.

## What changed since the original post (and why this plan differs)

1. **SAEs are tools, not a research direction.** Google DeepMind's interp team published [negative results for SAEs on downstream tasks](https://deepmindsafetyresearch.medium.com/negative-results-for-sparse-autoencoders-on-downstream-tasks-and-deprioritising-sae-research-6cadcfc125b9) and deprioritized SAE research; the field followed. Learn to *use* pretrained SAEs for discovering unknown concepts ([discover, don't act](https://arxiv.org/abs/2506.23845)), but do not build projects around SAE training or architecture tweaks.
2. **"Pragmatic interpretability" is the current strategic frame.** Read [A Pragmatic Vision for Interpretability](https://www.lesswrong.com/posts/StENzDcD3kpfGJssR/a-pragmatic-vision-for-interpretability) early — the emphasis is on solving problems on the critical path to safe AGI with fast empirical feedback, not fully reverse-engineering networks.
3. **Attribution graphs / circuit tracing are now a first-class, accessible skill.** Anthropic's [Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) plus the open-source [circuit-tracer](https://github.com/safety-research/circuit-tracer) library and [Neuronpedia](https://www.neuronpedia.org)'s hosted UI make this a cheap, high-yield playground for mini-projects.
4. **Hot project areas in 2026:** model biology, model diffing / crosscoders ([entry point](https://arxiv.org/pdf/2510.13900)), chain-of-thought faithfulness & [monitorability](https://arxiv.org/pdf/2507.11473), [automated alignment auditing](https://alignment.anthropic.com/2025/automated-auditing/), and cheap probe-based monitoring. De-emphasized: grokking/toy models, incremental SAE papers, pure circuit-finding.
5. **MATS selection (Nanda stream) is now a ~12-hour time-boxed research task + write-up** — no interviews, no CV gate. The single best preparation is doing exactly that repeatedly: short projects with crisp write-ups. Details: [MATS admissions procedure](https://www.neelnanda.io/blog/mats-apps-9).
6. **Field map:** [Open Problems in Mechanistic Interpretability](https://arxiv.org/abs/2501.16496) replaces the older "200 Concrete Open Problems."

## Phase 1 — Foundations (Months 1–2, ~80 hrs) — HARD CAP

Do not extend this phase "to feel ready." The cap is the point.

- **Weeks 1–2:** Linear algebra intuition via [3Blue1Brown's Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra); PyTorch basics. Use a frontier LLM as a tutor — have it quiz you on SVD, change of basis, rank (with anti-sycophancy prompting). *(Math Academy overlap helps here — see the ML Foundations track.)*
- **Weeks 3–5:** Build GPT-2 from scratch: [ARENA Chapter 1.1](https://www.arena.education/chapter1) with Neel's video walkthroughs.
- **Weeks 6–8:** [ARENA 1.2](https://learn.arena.education/) — TransformerLens, hooks, direct logit attribution, activation patching. Prioritize the first three sections; skim the IOI material. Read *Biology of a Large Language Model* alongside. Set up Colab + [runpod.io](https://runpod.io)/[vast.ai](https://vast.ai).

**Exit criteria:** you can code activation patching, a linear probe, and max-activating examples from scratch; you can load a pretrained SAE and explore an attribution graph on Neuronpedia.

**Core tooling:** [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) (models ≤9B), [nnsight](https://nnsight.net) (larger models), [SAELens](https://github.com/decoderesearch/SAELens), [circuit-tracer](https://github.com/safety-research/circuit-tracer).

## Phase 2 — Mini-projects (Months 3–4.5, ~60 hrs)

Three or four **throwaway** 15–20 hr projects (1.5–2 weeks each at this pace). These train skills; the output does not matter. Menu, aimed at 2026-relevant directions:

- Replicate-and-extend [refusal is mediated by a single direction](https://arxiv.org/abs/2406.11717) (probing + steering).
- Attribution-graph exploration of a quirky behavior (e.g. why models say 9.8 < 9.11) using circuit-tracer/Neuronpedia.
- Model diffing: replicate the [activation-difference analysis of a narrow fine-tune](https://arxiv.org/pdf/2510.13900).
- A small CoT-faithfulness/monitorability experiment on an open reasoning model (e.g. a DeepSeek-R1 distill).

**Non-negotiable rituals** (from the original post):
- Two mindsets: *exploration* — maximize information gain per unit time, pivot after ~2 fruitless hours; *understanding* — assume results are false until proven ("excitement is evidence of bullshit").
- Every project ends with a 2-hour post-mortem and a 1-page write-up.
- Keep a research log and a "things I believe" doc — update both on Fridays.

## Phase 3 — Full project & public write-up (Months 5–7, ~80–100 hrs)

Take the most promising mini-project thread. Work in 2-week sprints with an explicit pivot/continue decision each sprint (default: pivot). Target one **public artifact** — a LessWrong/Alignment Forum post or short arXiv paper with 1–3 core claims, baselines, ablations, and non-cherry-picked examples. A public write-up is the single best career credential in this field.

## Phase 4 — MATS application sprint (Months 7–9, ~40 hrs)

- Twice, dry-run the actual application format: a strictly time-boxed 12-hour research task on a fresh problem, ending in an executive summary + write-up. Post-mortem both.
- Apply broadly when windows open: MATS (check [matsprogram.org/apply](https://www.matsprogram.org/apply) and [Neel's blog](https://www.neelnanda.io/blog) for the next cycle), Anthropic Fellows, LASR, Pivotal; part-time/remote stepping stones: SPAR, MARS.

## Weekly rhythm

- **Mon–Thu:** 2 hrs of core work (course exercises or project work).
- **Fri:** consolidation — research log, post-mortems, LLM-quizzing on the week's concepts, skeptic pass on results, community reading (EleutherAI Discord interp channels, Neuronpedia, Alignment Forum).
