# Lesson 3: Section 16.1 — Sequential Decision Problems

This is the core of Tutorial 9 Question 1.

## 1. Why a new chapter?
Ch.15 handled **one** decision. Real agents make **a sequence** of decisions: what I do now changes where I am next, which changes my later options and rewards. And outcomes are **uncertain**.

Compare:
- **Search (earlier weeks):** deterministic actions, the answer is a **plan**, a fixed list of actions.
- **MDP:** random outcomes, the answer is a **policy**, a rule saying what to do in *every* state you might end up in. After one step you might be somewhere unexpected, so a fixed list is useless.

## 2. The MDP definition
A Markov decision process consists of:
| Piece | Meaning | Tutorial 9 example |
|---|---|---|
| States S, with an initial state s₀ | where the agent can be | 9 grid cells; s₀ = (3,3) |
| ACTIONS(s) | the choices in state s | N, E, S, W, Stay |
| Transition model P(s′ \| s, a) | probability of landing in s′ after a in s | the 70/30, 60/40, 80/20 rules |
| Reward function | the immediate reward signal | 20, −20, 5, and −1 elsewhere |
| Terminal states | episode ends here | (1,1), (3,1), (1,3) |

**Markov property:** P(s′ | s, a) depends only on the current state and action, not on history. That is why a table per state is enough.

**Two reward conventions** (the tutorial's Q3 is about converting between them):
- **R(s)**: reward for *being in* state s (the tutorial and many AI slides).
- **R(s, a, s′)**: reward for the *transition* (the textbook's general form, and Silver's RL course).
The R(s) form is a special case of the R(s,a,s′) form. Converting the other way may need extra states.

## 3. Policies
A **policy** π maps each state to an action: π(s). Because of randomness, the same policy can produce different histories each time you run it, so the **quality of a policy is the expected utility of the histories it produces**. The **optimal policy** π* is the best one.

## 4. Utility of sequences: how to add up rewards over time
Given a state sequence s₀, s₁, s₂, … with rewards R₀, R₁, R₂, …:
- **Finite horizon:** the game stops after a fixed number of steps N. Then the best action can depend on the time left, so optimal behaviour is *nonstationary*.
- **Infinite horizon:** no deadline. The optimal policy depends only on the state, so it is *stationary* (the usual case, and the one we study).

If the agent's preferences over sequences are *stationary* (if two sequences start with the same state, preferences between them are the same as preferences between their continuations), there are only two sensible forms of utility:

> **Additive:**  U = R₀ + R₁ + R₂ + …
> **Discounted:**  U = R₀ + γR₁ + γ²R₂ + …    with the discount factor γ between 0 and 1

Tutorial convention: s₀'s own reward counts at full weight (γ⁰ = 1).

### Why discount?
1. **Sooner is better** (a reward now is more certain than one later; like interest).
2. **The mathematics**: with γ < 1, an infinite sum of bounded rewards is finite:

> U ≤ Rmax / (1 − γ)   (if every reward is at most Rmax)

   Geometric series: r + γr + γ²r + … = r / (1 − γ).

**Worked examples**
- Constant −1 forever, γ = 0.5: −1 / (1 − 0.5) = **−2** (this is Tutorial Q1(b)(b)).
- Rewards −1, −1, −1, +10 with γ = 0.9: −1 − 0.9 − 0.81 + 0.729×10 = −2.71 + 7.29 = **4.58**.
- Rmax = 5, γ = 0.8: U ≤ 5 / 0.2 = **25**.

### Three ways to handle infinite sequences
1. Use γ < 1 (discounting).
2. Make sure every policy reaches a terminal state with probability 1 (**proper** policies); then γ = 1 is fine. Tutorial Q2 uses γ = 1 for exactly this reason.
3. Use the average reward per step (a different criterion).

## 5. Utility of a state vs reward of a state (very important)
- **Reward R:** what you get *now* for being somewhere.
- **Utility U(s):** the expected total (discounted) reward from s onward, if you behave in a certain way.

For a policy π: **U^π(s) = E[ Σ γᵗ R(...) ]** summed over the whole future, starting in s and following π. The optimal utility **U(s) = max over π of U^π(s)**.

Fact (for the infinite-horizon discounted case): the optimal policy does not depend on where you started, so there is **one** π* for all states. And **π\*(s) = argmax_a Σ P(s′|s,a) U(s′)** (one-step lookahead on utilities).

A square can have a poor reward but a great utility if it is next to something good.

## 6. How the reward numbers shape behaviour (and Tutorial Q2(d))
In the textbook's grid example (+1 and −1 terminals, a small cost per step), changing the per-step reward changes the optimal policy:
- **Very negative** step cost: "life is painful": rush to the nearest terminal, even the bad one.
- **Moderately negative**: take a longer route to avoid the risk of the bad terminal.
- **Slightly negative**: take the safest path, even if it is long.
- **Positive**: the agent *avoids terminals forever*: every step earns reward, so ending is bad. Staying in place can then be optimal.
This last case is exactly Tutorial 9 Q2(d) ("can *stay* be optimal?" Yes, with positive non-terminal rewards).

## 7. Preview: the Bellman equation (full treatment in Lesson 4)
Split the future into "now" and "everything after":

> U(s) = max over a of  Σ P(s′ | s, a) · [ R(s, a, s′) + γ · U(s′) ]

With rewards on states: **U(s) = R(s) + γ · max_a Σ P(s′|s,a) · U(s′)**.

## 8. Exam traps
- Policy ≠ plan. A policy gives an action for **every** state.
- U(s) is long-term; R(s) is immediate.
- Include R(s₀) with weight 1 when the question says Σ from i = 0.
- Infinite additive sums are −∞ or +∞; use discounting to compare.

## Checkpoint questions
1. In one sentence, why can't a fixed list of moves solve a random-outcome problem?
2. Rewards −2, −2, +10 with γ = 0.5: compute the additive and discounted return.
3. A never-ending stream of +2 rewards, γ = 0.9: total? What if γ = 1?
4. Rmax = 3, γ = 0.9: what is the upper bound on utility?
5. What is the difference between R(s) and U(s)?

<details><summary>Answers</summary>

1. After each random step you may be in a different state than planned, so you need an action for every state: a policy.
2. Additive: −2 − 2 + 10 = **6**. Discounted: −2 + 0.5×(−2) + 0.25×10 = −2 − 1 + 2.5 = **−0.5**.
3. γ = 0.9: 2 / 0.1 = **20**. γ = 1: **+∞** (diverges).
4. 3 / 0.1 = **30**.
5. R(s) is the immediate reward for being in s; U(s) is the expected total discounted reward from s onward.
</details>
