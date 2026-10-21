# Lesson 4: Section 16.2 — Algorithms for MDPs

This is the core of Tutorial 9 Question 2. Lesson 3 told you *what* U(s) and π* are. This lesson is *how to compute them*.

## 1. The Bellman equation and the Q-value
For each state s (rewards on transitions, as in the book):

> U(s) = max over a of  Σ_{s′} P(s′ | s, a) · [ R(s, a, s′) + γ · U(s′) ]

Define the **Q-value** of an action: Q(s, a) = Σ_{s′} P(s′|s,a) · [R(s,a,s′) + γU(s′)] = the expected total value of taking a in s and then behaving optimally. Then:
- **U(s) = max_a Q(s, a)**
- **π\*(s) = argmax_a Q(s, a)**

With rewards on **states** (the tutorial's form) this becomes:

> U(s) = R(s) + γ · max_a Σ_{s′} T(s, a, s′) · U(s′)

where T(s,a,s′) is the transition probability. R(s) and γ are the same for all actions, so they do not affect which action is best.

There is one such equation per state, and each contains `max`, so it is non-linear and can't be solved by ordinary algebra. Hence iteration.

## 2. Value iteration

**Algorithm**
1. Set U₀(s) = 0 for all states.
2. Repeat: for every state compute (the **Bellman update**)

> U_{i+1}(s) = R(s) + γ · max_a Σ_{s′} T(s,a,s′) · U_i(s′)

   using **only the old table U_i** on the right.
3. Stop when the values stop changing (or change by less than a threshold).

Terminal states: U(s) = R(s) at every iteration (no future after a terminal).

**What U_i means:** the best expected total reward if you only get to experience *i* states. So value "leaks outward" from large rewards one step per iteration. U₁ is just the rewards.

### A tiny worked example (all numbers verified)
States A and B are non-terminal with R = −1; G is terminal with R = +10; γ = 1. Layout: A → B → G. The only action, *Right*, works 80% of the time (moves one step) and 20% of the time you stay put.

| i | U_i(A) | U_i(B) | U_i(G) |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | −1 | −1 | 10 |
| 2 | −2 | 6.8 | 10 |
| 3 | 4.04 | 8.36 | 10 |
| 4 | 6.496 | 8.672 | 10 |
| 5 | 7.2368 | 8.7344 | 10 |

How U₂(B) is computed: −1 + [0.8 × U₁(G) + 0.2 × U₁(B)] = −1 + [8 + (−0.2)] = **6.8**.
How U₂(A): −1 + [0.8 × U₁(B) + 0.2 × U₁(A)] = −1 + [−0.8 − 0.2] = **−2**.
How U₃(B): −1 + [0.8×10 + 0.2×6.8] = −1 + 9.36 = **8.36**.

The values converge to the exact answers **U(B) = 8.75, U(A) = 7.5** (checked below with policy evaluation).

### Convergence (what the book proves)
- Each Bellman update is a **contraction** (in the max norm) by a factor γ: the largest error shrinks by at least a factor γ per iteration. So for γ < 1 value iteration converges to the unique solution of the Bellman equations. With γ = 1 it still works when terminal states are reachable (proper policies), as in the tutorial.
- **Stopping rule:** stop when the biggest change ≤ ε(1−γ)/γ; then the error is at most ε.
- **Policy loss:** the policy you extract can be good long before the values have converged. In practice the argmax actions settle well before the numbers do. (In Tutorial Q2(b), the policy read from U₂ differs from the final policy in a couple of cells.)

### Cost (trade-offs)
- **Time per iteration:** O(|S|² |A|) with a dense transition table; much less if each action has few possible outcomes (as in grid worlds, where each action has only 2).
- **Space:** one utility per state, plus the model.
- **Optimality:** converges to the optimal utilities and therefore an optimal policy.
- **Completeness:** n/a (it always produces a policy).

## 3. Policy extraction
Given a utility table U:

> π(s) = argmax_a Σ_{s′} T(s,a,s′) · U(s′)

No R, no γ needed. If two actions tie, either is optimal (state the tie).

## 4. Policy evaluation (a given policy)
If a policy π is *fixed*, the Bellman equation loses its `max`:

> U^π(s) = R(s) + γ · Σ_{s′} T(s, π(s), s′) · U^π(s′)

Two ways to solve it:
1. **Iteration:** repeat the update starting from 0 (this is what Tutorial Q2(c) asks).
2. **Exactly:** it is a **linear** system of n equations in n unknowns, solved by algebra (cost about O(n³)).

**Worked (same tiny chain, policy "Right"):**
- U(B) = −1 + 0.8 × 10 + 0.2 × U(B) → 0.8 U(B) = 7 → **U(B) = 8.75**
- U(A) = −1 + 0.8 × U(B) + 0.2 × U(A) → 0.8 U(A) = −1 + 7 = 6 → **U(A) = 7.5**
This matches the limit of the value-iteration table above ✓.

## 5. Policy iteration
An alternative to value iteration:
1. Start with any policy π₀.
2. **Policy evaluation:** compute U^{π_i} (the section above).
3. **Policy improvement:** π_{i+1}(s) = argmax_a Σ T(s,a,s′) U^{π_i}(s′) for every state.
4. Stop when the policy no longer changes; it is then optimal.

Why it terminates: each improvement step makes the policy at least as good, and there are only finitely many policies.
**Modified policy iteration:** instead of solving the linear system exactly, do just a few evaluation updates (k simplified Bellman updates) per round.

### Value iteration vs policy iteration
| | Value iteration | Policy iteration |
|---|---|---|
| Idea | iterate the Bellman update on U | alternate evaluate / improve |
| Cost per round | cheap (O(\|S\|²\|A\|)) | evaluation costs up to O(\|S\|³) |
| Number of rounds | many (geometric convergence) | few, usually |
| Result | converges only in the limit (but policy settles early) | exact optimal policy in finitely many rounds |
| Best when | big state space, cheap rounds | small/medium state space |

## 6. Two more ideas (low priority; know the names)
- **Linear programming:** the Bellman equations can be posed as a linear program (find the smallest utilities that satisfy all the inequalities U(s) ≥ Σ …).
- **Online algorithms:** for huge state spaces, don't compute a whole table; at each real decision, look ahead from the *current* state with search (e.g., sampling-based tree search) and act on that.

## 7. Map to Tutorial 9
| Tutorial part | Lesson 4 idea |
|---|---|
| Q2(a)(i) two iterations, (ii) three iterations | value iteration (Section 2) |
| Q2(b) policy after 2 iterations (MEU) | policy extraction (Section 3) |
| Q2(c) evaluate a given policy | policy evaluation by iteration (Section 4) |
| Q2(d) can *stay* be optimal? | positive rewards (Lesson 3, Section 6) |

## 8. Exam traps
- Fill the new table only from the old table.
- Terminal states: U = R, no max.
- Put R(s) once outside the max.
- Policy extraction has no R and no γ; policy evaluation has no max.
- Say "tie" when there is one.

## Checkpoint questions (paper)
1. Same chain as the example (A → B → G, R = −1, G = +10, γ = 1) but the move succeeds with probability **0.5** and you stay with probability 0.5. Compute U₁, U₂, U₃ for A and B.
2. Find the exact utilities for that chain under policy "Right" by solving the two linear equations.
3. In one sentence: what is the difference between a `max` and an `argmax`?
4. Why do we not put R(s) or γ inside the argmax for policy extraction?
5. Give one advantage of policy iteration over value iteration, and one of value iteration over policy iteration.

<details><summary>Answers</summary>

1. U₁: A = −1, B = −1, G = 10.
   U₂(B) = −1 + 0.5×10 + 0.5×(−1) = **3.5**; U₂(A) = −1 + 0.5×(−1) + 0.5×(−1) = **−2**.
   U₃(B) = −1 + 0.5×10 + 0.5×3.5 = **5.75**; U₃(A) = −1 + 0.5×3.5 + 0.5×(−2) = **−0.25**.
2. U(B) = −1 + 5 + 0.5U(B) → 0.5U(B) = 4 → **U(B) = 8**. U(A) = −1 + 0.5×8 + 0.5U(A) → 0.5U(A) = 3 → **U(A) = 6**.
3. `max` returns the best value; `argmax` returns the action that achieves it.
4. They are the same for every action in state s, so they cannot change which action is best.
5. Policy iteration: converges to the exact optimum in few rounds. Value iteration: each round is cheap (no linear system to solve).
</details>
