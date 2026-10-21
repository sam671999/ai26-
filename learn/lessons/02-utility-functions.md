# Lesson 2: Section 15.3 — Utility Functions

Lesson 1 showed that rational preferences imply a utility function. This section asks: **where do the numbers come from, and what do real utility functions look like?**

Exam importance for Tutorial 9 is low to medium. Read for understanding and learn the three small calculations below. (Subsection names below are from memory of the 4th edition; yours may differ slightly.)

## 1. Utility assessment and scales
To make utilities usable, fix a **normalised scale**:
- U(best possible outcome) = 1 (call it u⊤)
- U(worst possible outcome, "catastrophe") = 0 (call it u⊥)

**Standard gamble (how to measure U(S) for an outcome S):** find the probability p at which the agent is indifferent between getting S for sure and a lottery [p, u⊤; 1−p, u⊥]. Then **U(S) = p**.

Worked: an agent is indifferent between a sure outcome S and a 90% chance of the best / 10% chance of the worst. Then U(S) = 0.9.

Practical units for safety and health decisions:
- **Micromort**: a one-in-a-million chance of death.
- **QALY** (quality-adjusted life year): a year of life weighted by its quality.

## 2. The utility of money
Money is the classic case. Compare:
- **EMV** (expected monetary value): the plain probability-weighted average of the money amounts.
- **EU** (expected utility): the probability-weighted average of the *utilities* of the amounts.

For most people U(money) is **concave** (diminishing returns): the 1,000,001st dollar is worth less than the 1st.

Worked example. Utility U(x) = √x. Lottery: 50% $0, 50% $100.
- EMV = 0.5 × 0 + 0.5 × 100 = **$50**
- EU = 0.5 × √0 + 0.5 × √100 = 0 + 5 = **5**
- The utility of a *sure* $50 is √50 ≈ 7.07, which is **more** than 5, so the agent prefers a sure $50 to the gamble: **risk-averse**.
- **Certainty equivalent (CE)**: the sure amount worth the same as the lottery. Solve √CE = 5 → **CE = $25**.
- **Risk premium** (insurance premium) = EMV − CE = 50 − 25 = **$25**: what the agent gives up to avoid the risk. This is why insurance can be sold.

| Shape of U | Behaviour | Test |
|---|---|---|
| Concave (e.g., √x) | risk-averse | CE < EMV |
| Linear (U = x) | risk-neutral | CE = EMV |
| Convex (e.g., x²) | risk-seeking | CE > EMV |

Worked convex example: U(x) = x², lottery 50% $0 / 50% $10. EMV = 5. EU = 0.5×0 + 0.5×100 = 50. CE = √50 ≈ 7.07 > 5 → risk-seeking.

## 3. Expected utility and post-decision disappointment (the optimizer's curse)
Estimates of EU are *noisy*. If you choose the option with the highest estimate, you tend to pick one whose estimate was too high. So the **true** value of the chosen option is, on average, lower than its estimate: "post-decision disappointment".

Worked intuition: ten options are all truly worth 0, but each estimate has random noise of about ±1. The largest of ten noisy estimates is typically about +1.5, so you pick one that *looks* like 1.5 but is really 0. Remedies: shrink estimates toward a prior (Bayesian reasoning), use better estimates.

## 4. Human judgment and irrationality
Real people violate the axioms. The textbook's classic examples:

**Allais paradox.** Choose in two separate decisions:
- Decision 1: **A** = $1M for sure, or **B** = 10% $5M, 89% $1M, 1% $0.
- Decision 2: **C** = 11% $1M, 89% $0, or **D** = 10% $5M, 90% $0.

Most people choose A over B *and* D over C. This **cannot** be explained by any utility function:
- A ≻ B means U(1M) > 0.1·U(5M) + 0.89·U(1M) + 0.01·U(0), i.e. 0.11·U(1M) > 0.1·U(5M) + 0.01·U(0).
- D ≻ C means 0.1·U(5M) + 0.90·U(0) > 0.11·U(1M) + 0.89·U(0), i.e. 0.1·U(5M) + 0.01·U(0) > 0.11·U(1M).
These two inequalities contradict each other. People are reacting to the *certainty* of A (the "certainty effect").

Other effects to name: **Ellsberg paradox** (people avoid ambiguity, i.e. unknown probabilities), **framing** (the same choice worded as gains vs losses gets different answers), **anchoring**. **Prospect theory** is a descriptive model of how people actually choose (e.g., losses hurt more than equal gains please).

**Why this matters:** decision theory is a *normative* standard (what a rational agent should do), and it is what we build into AI agents, not a perfect description of people.

## Checkpoint questions
1. U(x) = √x, lottery 50% $0 / 50% $64. Find EMV, EU, certainty equivalent, and say if the agent is risk-averse.
2. For U(x) = x, lottery 50% $0 / 50% $10: what is the CE and the type?
3. Why does picking the highest estimated EU tend to disappoint?
4. In the Allais paradox, which two choices are inconsistent with expected-utility maximisation?

<details><summary>Answers</summary>

1. EMV = 32. EU = 0.5×0 + 0.5×8 = 4. √CE = 4 → CE = 16 < 32 → **risk-averse** (risk premium 16).
2. EU = 5, so CE = 5 = EMV → **risk-neutral**.
3. Noisy estimates: the maximum picks up positive errors, so the true value is lower on average.
4. A over B together with D over C.
</details>
