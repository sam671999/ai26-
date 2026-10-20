# Lesson 1: Sections 15.1 and 15.2 — Beliefs, desires, and why "utility" exists

## 1. The big picture
An agent must act without knowing exactly what will happen. Two things are needed:
- **Beliefs** (probability theory): how likely is each outcome of each action?
- **Desires** (utility theory): how much do I like each outcome?

**Decision theory = probability theory + utility theory.** This is the idea of section 15.1, and it is the foundation of everything in Tutorial 9.

## 2. The formulas (define every symbol)
- a = an action the agent could take.
- e = the evidence (what the agent has observed so far).
- s′ = a possible outcome state.
- P(RESULT(a) = s′ | a, e) = the probability that doing a leads to outcome s′.
- U(s′) = the **utility** of s′, a number saying how desirable s′ is (bigger is better).

**Expected utility of an action:**

> EU(a | e) = Σ over s′ of  P(RESULT(a) = s′ | a, e) × U(s′)

It is a weighted average: each outcome's utility multiplied by its probability, added up.

**The Maximum Expected Utility (MEU) principle:**

> A rational agent chooses  a* = argmax over a of EU(a | e).

`max` gives the best *value*; `argmax` gives *which action* achieves it. Tutorial 9 Q2(b) literally says "use the Maximum Expected Utility principle".

## 3. Worked example (not a grid)
Two job offers; utilities are 0–100.
- Offer X: 60% chance of a great job (U = 100), 40% chance of a mediocre one (U = 20).
 EU(X) = 0.6 × 100 + 0.4 × 20 = 60 + 8 = **68**
- Offer Y: a guaranteed decent job (U = 70). EU(Y) = **70**

MEU says take Y. X looks exciting (it has the best possible outcome), but the *average* is lower. Decision theory judges actions by the weighted average, not the best case and not the worst case.

**Link to the tutorial:** at cell (1,2), West has outcomes {70% → the +20 cell, 30% → a −1 cell}: EU-style value 0.7×20 + 0.3×(−1) = 13.7. East: 0.6×5 + 0.4×(−1) = 2.6. MEU picks West.

## 4. What MEU does and does not say
- It is a **standard of rationality**, not a recipe for computing. Finding the probabilities and the utilities, and computing EU for huge problems, can be hard. That difficulty is why ch.16 exists.
- The utility U(s′) of an outcome should already include everything the agent cares about (not just immediate pleasure).
- In ch.16 the "outcome" becomes a *state in a long process*, and U(s) means the expected total reward from then on.

## 5. Section 15.2: why should anyone believe in MEU?
Instead of assuming utilities, the book starts from **preferences**:
- A ≻ B: the agent prefers A to B.
- A ∼ B: the agent is indifferent.
- A ≿ B: the agent prefers A or is indifferent.

A **lottery** is a list of outcomes with probabilities: L = [p₁, S₁; p₂, S₂; …; pₙ, Sₙ], where the probabilities sum to 1 and each Sᵢ can itself be another lottery.

### The six constraints on rational preferences (the "axioms")
| Name | Meaning | Why it is reasonable |
|---|---|---|
| Orderability | Exactly one of A ≻ B, B ≻ A, A ∼ B holds. | A rational agent can compare any two options. |
| Transitivity | If A ≻ B and B ≻ C then A ≻ C. | See the money pump below. |
| Continuity | If A ≻ B ≻ C, some probability p makes B ∼ [p, A; 1−p, C]. | Some gamble between best and worst is as good as the middle option. |
| Substitutability | If A ∼ B then [p, A; 1−p, C] ∼ [p, B; 1−p, C]. | Swapping equally-good prizes does not change the lottery's worth. |
| Monotonicity | If A ≻ B, then a lottery giving A with a higher probability is preferred: [p, A; 1−p, B] ≿ [q, A; 1−q, B] exactly when p ≥ q. | More chance of the better prize is better. |
| Decomposability | Nested lotteries can be flattened: [p, A; 1−p, [q, B; 1−q, C]] ∼ [p, A; (1−p)q, B; (1−p)(1−q), C]. | "No fun in gambling": only the final probabilities matter. |

**Worked decomposability:** [0.5, A; 0.5, [0.4, B; 0.6, C]] ∼ [0.5, A; 0.2, B; 0.3, C], because 0.5 × 0.4 = 0.2 and 0.5 × 0.6 = 0.3. Check: 0.5 + 0.2 + 0.3 = 1.

### The money pump (why transitivity matters)
Suppose an agent has A ≻ B, B ≻ C, and C ≻ A. If it holds C, you can offer to swap C for B if it pays a small fee, then B for A for a fee, then A for C for a fee. It is back where it started and poorer. Repeat forever. Irrational preferences are exploitable.

### The result (von Neumann–Morgenstern theorem, as in the book)
If an agent's preferences obey the constraints, then there exists a function U such that:
1. U(A) > U(B) exactly when A ≻ B, and U(A) = U(B) exactly when A ∼ B (the utility function *represents* preferences).
2. **U([p₁, S₁; …; pₙ, Sₙ]) = Σ pᵢ U(Sᵢ)**: the utility of a lottery is its expected utility.

So an agent with consistent preferences *behaves as if* it maximises expected utility. This is an existence result: it does not say the agent computes utilities consciously.

### Utilities are not unique
If U is a utility function, so is **U′(s) = a·U(s) + b with a > 0** (a positive affine transformation): the agent behaves identically.
Check: U = (0, 50, 100) for outcomes (s₁, s₂, s₃), U′ = 2U + 10 = (10, 110, 210). Lottery [0.5, s₁; 0.5, s₃]: EU = 50, EU′ = 0.5×10 + 0.5×210 = 110 = 2×50 + 10 ✓. Same ordering of lotteries.

In a world with no uncertainty, only the *order* matters (any increasing transformation works). With lotteries, you need the affine class.

**Why this matters for MDPs:** multiplying every reward by a positive constant never changes the best policy. Adding a constant to every reward *can* change it when there are terminal states, because it changes how much one extra step costs. (Tutorial 9 Q2(d): changing the step reward from negative to positive can make "stay" optimal.)

## 6. Exam traps
- Weighted average, not simple average: multiply by the probabilities.
- Don't confuse the expected utility of an *action* with the utility of an *outcome*.
- A positive affine transformation (a > 0) is safe; a negative a reverses preferences.

## Checkpoint questions (paper, one at a time)
1. Action A: 50% × (+10) and 50% × (−2). Action B: a guaranteed +3. What are the expected utilities and which does MEU choose?
2. Flatten [0.5, A; 0.5, [0.4, B; 0.6, C]]. Do the probabilities sum to 1?
3. Utilities of three outcomes are (0, 30, 60). A new scale is U′ = 3U + 5. What are the new values, and does the choice between a sure 30 and the lottery [0.5, 0; 0.5, 60] change?
4. In one sentence: what does the MEU principle tell a rational agent to do?

<details><summary>Answers</summary>

1. EU(A) = 0.5×10 + 0.5×(−2) = 5 − 1 = **4**. EU(B) = **3**. MEU chooses A.
2. [0.5, A; 0.2, B; 0.3, C]; 0.5 + 0.2 + 0.3 = 1.
3. U′ = (5, 95, 185). Original: sure 30 → 30; lottery → 0.5×0 + 0.5×60 = 30, so tied. New: sure → 95; lottery → 0.5×5 + 0.5×185 = 95, still tied. The choice does not change.
4. Choose the action whose probability-weighted average utility of outcomes is highest.
</details>
