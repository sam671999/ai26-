# COSC3117 — Tutorial 9 DEEP GUIDE: Markov Decision Processes & Value Iteration

> Goal: after this guide you can (1) explain *why* every formula is what it is, (2) build an MDP from a word problem, (3) fill value-iteration tables by hand without panic, (4) extract and evaluate policies, and (5) handle the "weird" parts (walls, ties, Stay, R(s) vs R(s,a,s′)).
>
> **How to study this:** Read Parts 1–5 once, slowly (about 60–75 min). Then do Part 6 (the tutorial questions) *on paper first*, using Part 6 only to check. Then Part 8 (practice). Re-do one question cold the next day.
>
> Companion files: `STUDY-GUIDE.md` (1-page revision sheet), `mdp_checker.py` (recomputes everything — edit numbers to check your own variants).

---

# PART 1 — The problem MDPs solve (intuition first)

## 1.1 From search to uncertainty
In the earlier weeks of this course (search: BFS, A*, etc.) you assumed **actions do exactly what they say**: "move north" puts you in the north cell. The world was *deterministic* and the answer to a problem was a **fixed sequence of actions** (a plan).

Real agents (robots, game characters) live in a world where **actions can fail or slip**. A robot told to go north on a wet floor might drift west. Now a fixed plan is useless: after one step you might not be where you expected. What you need instead is a **rule that says what to do in whichever state you end up in**. That rule is called a **policy**.

> **Plan** = a list of actions ("N, N, E").
> **Policy** = a lookup table state → action ("if in (2,2) go North; if in (2,3) go North; …").

This is the single most important conceptual jump in the topic: **with randomness, the output of planning is a policy, not a path.**

## 1.2 Why "just do what looks best next step" isn't enough
You get a reward in each state you visit (e.g. −1 per step, +20 at the goal). Greedy would pick the action with the best immediate reward — but the −1 steps are all identical, so greedy has nothing to go on. What matters is the **long-run total** reward. That is why we need *utilities* (Part 4): a number for each state that summarises "how good is it to be here, considering everything that will happen afterwards?"

## 1.3 The Markov property
"Markov" means: **the future depends only on the current state (and action), not on how you got there.** T(s,a,s′) only needs s and a, never the history. That is why a table of numbers per state is enough to describe the whole problem.

---

# PART 2 — The MDP formally, and the grid conventions

## 2.1 The five ingredients
| Symbol | Name | Plain English | In Question 1 |
|---|---|---|---|
| S | states | every situation the agent can be in | 9 cells |
| s₀ | start state | where the agent begins | (3,3) |
| terminals | terminal states | once entered, the episode ends | (1,1), (3,1), (1,3) |
| A | actions | what the agent can choose | N, E, S, W, Stay |
| T(s,a,s′) | transition model | probability of landing in s′ if you do a in s | the 70/30 etc. rules |
| R(s) | reward function | the reward for being in s | 20, −20, 5, else −1 |

Formally: T : S × A × S → ℝ, (s,a,s′) ↦ P(s′ | a ∧ s). In words, T is *a probability distribution over s′ for each fixed (s,a)*. So:

> **Sanity rule #1:** for every fixed (s, a): Σ over s′ of T(s,a,s′) = 1. Check this every single time you write a transition.

Terminal states: the problem says "Remember terminal states do not get more rewards once reached." Interpretation: when the agent steps into a terminal state it collects that state's reward **once**, and then the process is over. In the value-iteration equation this is implemented by **fixing U(terminal) = R(terminal) forever** (no future beyond it).

## 2.2 Coordinates and compass — get this wrong and everything is wrong
Cells are **(row, column)**. Row 1 is the **top**.

```
                col 1   col 2   col 3
              ┌───────┬───────┬───────┐
   row 1      │  20   │  -1   │   5   │      ↑ NORTH  = row − 1
              ├───────┼───────┼───────┤      ↓ SOUTH  = row + 1
   row 2      │  -1   │  -1   │  -1   │      → EAST   = col + 1
              ├───────┼───────┼───────┤      ← WEST   = col − 1
   row 3      │ -20   │  -1   │  -1   │
              └───────┴───────┴───────┘
 (1,1) terminal +20     (1,3) terminal +5     (3,1) terminal −20     start = (3,3) bottom-right
```

Mnemonic: **north = up = smaller row number**. (In maths graphs "up" is bigger y; here it's the opposite. Don't mix them.)

## 2.3 The stochastic action rules
When the agent *chooses* an action, the *actual* movement direction is random:

| Choose | 1st outcome | 2nd outcome |
|---|---|---|
| North | 70 % north | 30 % **west** |
| East | 60 % east | 40 % **south** |
| South | 80 % south | 20 % **east** |
| West | 70 % west | 30 % **north** |
| Stay | 100 % stay | — |

Notice the pattern: each action can "slip" into a *different* direction (north slips west, east slips south, south slips east, west slips north). The slip direction is **not** "the opposite" or "sideways both ways" — read the table, don't assume.

## 2.4 The WALL rule (where most marks are lost)
"If an action causes the agent to travel into a wall, the agent will stay in their current cell."

Crucial subtlety: this applies **per outcome**, not per action. Each of the two random outcomes is checked separately, and a blocked outcome puts its probability on the **current cell**.

Worked example: at (3,3) (bottom-right corner), action **East**:
- 60 %: "go east" → col 4 doesn't exist → wall → stay at (3,3)
- 40 %: "go south" → row 4 doesn't exist → wall → stay at (3,3)
- So all 100 % lands on (3,3): **T((3,3), East, (3,3)) = 1.0**.

Worked example: at (3,3), action **North**:
- 70 %: north → (2,3) fine
- 30 %: west → (3,2) fine
- So T = 0.7 to (2,3), 0.3 to (3,2). No wall involved.

Worked example where only *one* outcome hits a wall — (1,2) (top middle), action **North**:
- 70 %: north → row 0 → wall → stay at (1,2)
- 30 %: west → (1,1)
- So T((1,2),N,(1,2)) = 0.7, T((1,2),N,(1,1)) = 0.3.

> **Technique:** For every (cell, action), write the two target cells first (the "intended" and the "slip"), cross out any that hit a wall and replace with the cell itself, THEN add the probabilities (if both outcomes land on the same cell, add them).

## 2.5 Neighbour lookup table (make this once, saves enormous time)
Where each *direction of movement* sends you from each non-terminal cell (a wall means "stays put" — written as the cell itself):

| Cell | N (row−1) | E (col+1) | S (row+1) | W (col−1) |
|---|---|---|---|---|
| (1,2) | (1,2) wall | (1,3) | (2,2) | (1,1) |
| (2,1) | (1,1) | (2,2) | (3,1) | (2,1) wall |
| (2,2) | (1,2) | (2,3) | (3,2) | (2,1) |
| (2,3) | (1,3) | (2,3) wall | (3,3) | (2,2) |
| (3,2) | (2,2) | (3,3) | (3,2) wall | (3,1) |
| (3,3) | (2,3) | (3,3) wall | (3,3) wall | (3,2) |

Then an *action* is a mix of two columns of this table:
- Action North = 0.7·N-column + 0.3·W-column
- Action East = 0.6·E-column + 0.4·S-column
- Action South = 0.8·S-column + 0.2·E-column
- Action West = 0.7·W-column + 0.3·N-column
- Action Stay = 1.0·(the cell itself)

## 2.6 Complete transition table for every non-terminal cell
(Generated from the neighbour table and verified by code. Only non-zero entries shown; everything else is 0.)

| State | North | East | South | West | Stay |
|---|---|---|---|---|---|
| (1,2) | (1,2):0.7, (1,1):0.3 | (1,3):0.6, (2,2):0.4 | (2,2):0.8, (1,3):0.2 | (1,1):0.7, (1,2):0.3 | (1,2):1 |
| (2,1) | (1,1):0.7, (2,1):0.3 | (2,2):0.6, (3,1):0.4 | (3,1):0.8, (2,2):0.2 | (2,1):0.7, (1,1):0.3 | (2,1):1 |
| (2,2) | (1,2):0.7, (2,1):0.3 | (2,3):0.6, (3,2):0.4 | (3,2):0.8, (2,3):0.2 | (2,1):0.7, (1,2):0.3 | (2,2):1 |
| (2,3) | (1,3):0.7, (2,2):0.3 | (2,3):0.6, (3,3):0.4 | (3,3):0.8, (2,3):0.2 | (2,2):0.7, (1,3):0.3 | (2,3):1 |
| (3,2) | (2,2):0.7, (3,1):0.3 | (3,3):0.6, (3,2):0.4 | (3,2):0.8, (3,3):0.2 | (3,1):0.7, (2,2):0.3 | (3,2):1 |
| (3,3) | (2,3):0.7, (3,2):0.3 | (3,3):1.0 | (3,3):1.0 | (3,2):0.7, (2,3):0.3 | (3,3):1 |

Check one by hand: (2,1) West. West: 0.7·W-col → (2,1) (wall) ; 0.3·N-col → (1,1). Table says (2,1):0.7, (1,1):0.3 ✓.

---

# PART 3 — Rewards, returns, and discounting

## 3.1 Reward vs utility — two different things
- **Reward R(s)**: a number you receive *immediately* for being in a state. Local, short-term.
- **Utility U(s)**: the *expected total (discounted) reward* from s onwards if you behave optimally. Global, long-term.

Analogy: R is your salary this month; U is your expected lifetime earnings from this job. A state with a bad R (−1) can have a great U if it's right next to the +20 cell.

## 3.2 Additive vs discounted return
For a sequence of states s₀, s₁, …, s_t:

- **Additive:** R(s₀) + R(s₁) + … + R(s_t)
- **Discounted** (decay factor γ, 0 ≤ γ ≤ 1): R(s₀) + γR(s₁) + γ²R(s₂) + … + γᵗR(s_t)

The tutorial convention: s₀ **is rewarded** (no discount on step 0), because with R(s) there's no "previous state" to attach a reward to.

**Why discount?**
1. *Sooner is better* (a dollar today beats a dollar tomorrow; also the future is uncertain).
2. *Mathematics:* a never-ending sequence of −1 rewards adds up to −∞ additively. Discounted it is a convergent geometric series, so comparisons are meaningful.

## 3.3 The geometric series (know this one)
If every reward is the same number r, forever:

total = r + γr + γ²r + … = r · (1 + γ + γ² + …) = **r / (1 − γ)**  (valid for 0 ≤ γ < 1)

For r = −1, γ = 0.5: −1 / 0.5 = **−2**. This is the answer to Question 1(b)(b).

## 3.4 What γ means as a personality
- γ = 1: "I care about the far future exactly as much as now" (additive). Only safe when episodes end (terminal states) — Q2 uses γ=1 for that reason.
- γ close to 0: very short-sighted.
- γ = 0.5: a reward 3 steps away is worth 1/8 of one right now.

---

# PART 4 — Utility, the Bellman equation, and value iteration (the heart)

## 4.1 Defining utility
For a policy π (a rule for choosing actions):

U^π(s) = E[ R(s₀) + γR(s₁) + γ²R(s₂) + … | s₀ = s, follow π ]

(The E means "average over all the random ways the future could unfold".)
The **optimal** utility U(s) is the best you can do over all policies.

## 4.2 The key insight: utility is recursive
Split the sum into "now" and "everything after":

U^π(s) = R(s) + γ · E[ R(s₁) + γR(s₂) + … ] = R(s) + γ · E[ U^π(s₁) ]

In words: **the value of a state = its own reward + γ × (the average value of wherever you land next).** The "wherever you land next" is random, and its probabilities come from T. This gives:

### Policy-evaluation equation (a policy is fixed — no choice)
U^π(s) = R(s) + γ Σ_{s′} T(s, π(s), s′) U^π(s′)

### Bellman optimality equation (you get to choose the best action)
U(s) = R(s) + γ · **max_a** Σ_{s′} T(s,a,s′) U(s′)

## 4.3 Dissecting the sum — the "Q-value"
For a fixed state s and action a, define

**Q(s,a) = Σ_{s′} T(s,a,s′) · U(s′)** = *expected utility of the state you'll land in, if you choose a.*

Read it as a weighted average: for each possible landing cell, (probability) × (that cell's utility), then add up. That's all it is. Then:

> **U_new(s) = R(s) + γ · max_a Q(s,a)**
> **π(s) = argmax_a Q(s,a)**

`max` returns the **value** of the best action. `argmax` returns **which action** it was. (The tutorial's video link is about exactly this distinction.)

## 4.4 Value iteration — what it does and why it works
The Bellman optimality equation is a system of equations with `max` inside, so it can't be solved by simple algebra. Value iteration solves it by **iterating**:

1. Start with U₀(s) = 0 for every state (a blank guess).
2. For every state, compute U_{i+1}(s) = R(s) + γ max_a Σ T(s,a,s′) U_i(s′), **using only the old table U_i** on the right-hand side.
3. Repeat. The numbers converge to the true utilities.

### The best way to understand what U_i actually is
**U_i(s) = the best expected total reward you can collect if you only get to experience i states (counting s itself).**
- U₁(s) = R(s): you only get to experience s. So U₁ is just the rewards.
- U₂(s) = R(s) + best expected R of the next state.
- U₃(s) = R(s) + best expected (R of next + best expected R of the one after) …

That makes the tables *predictable*. In the grid, value "**leaks outward from the big reward one step per iteration**": after 2 iterations only cells within 1 step of the +20 corner have caught the 20; after 3 iterations cells within 2 steps; and so on. If your table has a high value far from any big reward early on, you've made an error.

### Two free sanity checks (use these in the exam!)
1. **Floor check.** With R = −1, γ = 1 and Stay available, U_i(s) ≥ −i for non-terminal cells (you could just Stay and collect −1 each time). So U₂ ≥ −2 and U₃ ≥ −3 for every non-terminal cell. If you write −5 at U₂, you're wrong.
2. **Ceiling check.** No cell can exceed the best terminal reward (20) with γ=1 here. Non-terminal cells next to the 20 should be a bit below 20.

## 4.5 Terminal states in the iteration
For a terminal state, **U_i(s) = R(s) for every i ≥ 1** (U₀ = 0 for everything, as given). Don't apply the max formula to terminals; there's no future.

## 4.6 One state, one iteration — the exact recipe
Memorise this loop; every exam cell is this:

1. Pick a state s.
2. For each action a: list (landing cell, probability) → multiply each probability by **that landing cell's value in the OLD table** → add. That's Q(s,a).
3. Choose the largest Q.
4. U_new(s) = R(s) + γ × (largest Q). *(R(s) is added once, outside the max.)*
5. Write it in the **NEW** table. Don't read from it until the whole table is finished.

**Error that costs the most marks:** using a value you've just computed in the new table (mixing iterations). Keep two tables on the page.

---

# PART 5 — Policies: extraction vs evaluation

| | **Policy extraction** (Q2b) | **Policy evaluation** (Q2c) |
|---|---|---|
| You are given | a utility table U | a policy π |
| You produce | a policy | a utility table |
| Formula | π(s) = argmax_a Σ T·U(s′) | U^π_{i+1}(s) = R(s) + γ Σ T(s,π(s),s′) U^π_i(s′) |
| Has R? γ? | **No** (R and γ don't change which action wins) | **Yes** |
| Has max? | argmax over all 5 actions | **None** — only the given action |

Why does extraction ignore R(s) and γ? Because R(s) and γ are the same for every action in state s; multiplying by γ>0 and adding R(s) doesn't change which action has the largest Q.

**Ties.** If two actions have the same Q, either is a valid optimal action. In an exam, write "North or West (tie)" — don't pretend there's a unique answer.

**Maximum Expected Utility (MEU) principle** (named in Q2b): a rational agent picks the action that maximises expected utility. That is exactly argmax_a Q(s,a).

---

# PART 6 — The tutorial questions, fully worked

## Question 1(a): Build the MDP

**i. States.** S = {(r,c) : r,c ∈ {1,2,3}} — 9 states.

**ii. Start & terminals.** s₀ = (3,3). Terminals = {(1,1), (3,1), (1,3)}.

**iii. Actions.** A = {North, East, South, West, Stay}. (It's fine to say "Stay is the same for terminals but irrelevant because the episode ends there".)

**iv. T from (3,3).** Using §2.4:

| Action | Outcomes |
|---|---|
| North | 0.7 → (2,3); 0.3 (west) → (3,2) |
| East | 0.6 (east, wall) → (3,3); 0.4 (south, wall) → (3,3). **Total T((3,3),E,(3,3)) = 1.0** |
| South | 0.8 (south, wall) → (3,3); 0.2 (east, wall) → (3,3). **Total = 1.0** |
| West | 0.7 → (3,2); 0.3 (north) → (2,3) |
| Stay | 1.0 → (3,3) |

Everything else is 0. Each action's row sums to 1 ✓.
**Common wrong answer:** writing T((3,3),East,(3,3)) = 0.6 and forgetting the south-slip also hits a wall.

**v. Reward function.**
R(1,1) = 20, R(3,1) = −20, R(1,3) = 5, R(s) = −1 for the other six cells.

## Question 1(b): Additive vs discounted reward

**Sequence (a): (3,3), (2,3), (2,2), (2,1), (1,1)**
Rewards in order: −1, −1, −1, −1, +20.
- *Additive:* −1−1−1−1+20 = **16**.
- *Discounted γ=0.5:* −1 + 0.5(−1) + 0.25(−1) + 0.125(−1) + 0.0625(20)
  = −1 − 0.5 − 0.25 − 0.125 + 1.25 = **−0.625**.

**Sequence (b): (3,3), (3,2), (2,2), (2,3), …repeat forever**
Every state is a non-terminal: reward −1 every step.
- *Additive:* −1−1−1−… = **−∞**.
- *Discounted:* −1/(1−0.5) = **−2**.

**What the question is teaching.** Additive: (b) is catastrophic (−∞) vs (a) = 16 — fine, but additive sums can be infinite and can't be compared when two sequences are both infinite. Discounted: everything stays finite (so an agent can compare infinite behaviours), and *distant* rewards matter less: the +20 in (a) is worth only 1.25 because it arrives 4 steps away. That's why (a) drops from 16 to −0.625.

---

## Question 2(a): Value iteration, γ = 1

Rewards: terminals 20 / −20 / 5; others −1. Since γ = 1 the factor disappears.

### Iteration 1 (U₀ = 0 everywhere)
For a non-terminal s: U₁(s) = −1 + max_a Σ T · 0 = **−1**. Terminals: their reward.

```
U1:   20    -1     5
      -1    -1    -1
     -20    -1    -1
```

### Iteration 2 — every Q-value, every cell (using the U₁ table)
Format: Q(s,a) = Σ probability × old value.

**(1,2)**, R = −1
- North: 0.3·U₁(1,1) + 0.7·U₁(1,2) = 0.3·20 + 0.7·(−1) = 6 − 0.7 = **5.3**
- East: 0.6·U₁(1,3) + 0.4·U₁(2,2) = 0.6·5 + 0.4·(−1) = 3 − 0.4 = **2.6**
- South: 0.2·U₁(1,3) + 0.8·U₁(2,2) = 1 − 0.8 = **0.2**
- **West:** 0.7·U₁(1,1) + 0.3·U₁(1,2) = 14 − 0.3 = **13.7** ← best
- Stay: −1
- U₂(1,2) = −1 + 13.7 = **12.7**

**(2,1)**, R = −1
- **North:** 0.7·U₁(1,1) + 0.3·U₁(2,1) = 14 − 0.3 = **13.7** ← best
- East: 0.6·U₁(2,2) + 0.4·U₁(3,1) = −0.6 − 8 = −8.6
- South: 0.2·(−1) + 0.8·(−20) = −16.2
- West: 0.3·U₁(1,1) + 0.7·U₁(2,1) = 6 − 0.7 = 5.3
- Stay: −1
- U₂(2,1) = **12.7**

**(2,2)**, R = −1 — every neighbour currently has value −1 (no terminal adjacent), so every action gives −1
- N, E, S, W, Stay all = −1
- U₂(2,2) = −1 + (−1) = **−2**

**(2,3)**, R = −1
- **North:** 0.7·U₁(1,3) + 0.3·U₁(2,2) = 3.5 − 0.3 = **3.2** ← best
- East: 0.6·(−1) + 0.4·(−1) = −1
- South: −1
- West: 0.3·U₁(1,3) + 0.7·U₁(2,2) = 1.5 − 0.7 = 0.8
- Stay: −1
- U₂(2,3) = −1 + 3.2 = **2.2**

**(3,2)**, R = −1
- North: 0.7·U₁(2,2) + 0.3·U₁(3,1) = −0.7 − 6 = −6.7
- East: 0.6·U₁(3,3) + 0.4·U₁(3,2) = −1
- South: 0.8·U₁(3,2) + 0.2·U₁(3,3) = −1
- West: 0.3·U₁(2,2) + 0.7·U₁(3,1) = −0.3 − 14 = −14.3
- Stay: −1
- Best = −1 (E, S or Stay tie) → U₂(3,2) = **−2**. *(North and West are bad because of the slip/move into the −20 cell.)*

**(3,3)**, R = −1
- Every action → neighbours with value −1 → Q = −1 for all.
- U₂(3,3) = **−2**

```
U2:   20    12.7     5
     12.7    -2     2.2
      -20    -2     -2
```

**Why these numbers make sense (U_i = best total of i rewards):** U₂(1,2)=12.7: step on (1,2) gets −1; then 70% chance of stepping onto the 20 cell (+20) and 30% chance of a −1 → expected −1 + 14 − 0.3 = 12.7 ✓. Cells not adjacent to a terminal can only collect −1 −1 = −2 ✓.

### 2(a)(ii) — Iteration 3 (using the U₂ table)
Now it's the same recipe, but the old table is U₂.

**(1,2)**
- North: 0.3·20 + 0.7·12.7 = 6 + 8.89 = 14.89
- East: 0.6·5 + 0.4·(−2) = 3 − 0.8 = 2.2
- South: 0.2·5 + 0.8·(−2) = 1 − 1.6 = −0.6
- **West:** 0.7·20 + 0.3·12.7 = 14 + 3.81 = **17.81**
- Stay: 12.7
- U₃(1,2) = −1 + 17.81 = **16.81**

**(2,1)**
- **North:** 0.7·20 + 0.3·12.7 = **17.81**
- East: 0.6·(−2) + 0.4·(−20) = −9.2
- South: 0.2·(−2) + 0.8·(−20) = −16.4
- West: 0.3·20 + 0.7·12.7 = 6 + 8.89 = 14.89
- Stay: 12.7
- U₃(2,1) = **16.81**

**(2,2)**
- North: 0.7·U₂(1,2) + 0.3·U₂(2,1) = 0.7·12.7 + 0.3·12.7 = **12.7**
- East: 0.6·U₂(2,3) + 0.4·U₂(3,2) = 1.32 − 0.8 = 0.52
- South: 0.2·2.2 + 0.8·(−2) = 0.44 − 1.6 = −1.16
- West: 0.3·U₂(1,2) + 0.7·U₂(2,1) = **12.7** (tie with North)
- Stay: −2
- U₃(2,2) = −1 + 12.7 = **11.7**

**(2,3)**
- **North:** 0.7·5 + 0.3·(−2) = 3.5 − 0.6 = **2.9**
- East: 0.6·2.2 + 0.4·(−2) = 1.32 − 0.8 = 0.52
- South: 0.2·2.2 + 0.8·(−2) = −1.16
- West: 0.3·5 + 0.7·(−2) = 1.5 − 1.4 = 0.1
- Stay: 2.2
- U₃(2,3) = −1 + 2.9 = **1.9**
*(Interesting: Stay (2.2) is the runner-up; North wins because 70% chance of +5 beats sitting still.)*

**(3,2)**
- North: 0.7·(−2) + 0.3·(−20) = −1.4 − 6 = −7.4
- East: 0.6·(−2) + 0.4·(−2) = −2
- South: −2
- West: 0.3·(−2) + 0.7·(−20) = −14.6
- Stay: −2
- Best −2 (E/S/Stay tie) → U₃(3,2) = −1 + (−2) = **−3**
*(−3 = the floor: three states each with −1. So "can't see anything good within 3 steps" ✓.)*

**(3,3)**
- **North:** 0.7·U₂(2,3) + 0.3·U₂(3,2) = 1.54 − 0.6 = **0.94**
- East/South/Stay: −2 (the wall keeps you at (3,3), U₂ = −2)
- West: 0.3·2.2 + 0.7·(−2) = 0.66 − 1.4 = −0.74
- U₃(3,3) = −1 + 0.94 = **−0.06**

```
U3:   20     16.81      5
     16.81   11.7      1.9
      -20     -3      -0.06
```

**Watch how value leaks:** after iteration 2 only cells touching a terminal had good values; after iteration 3 the centre (2,2) got 11.7 and the start (3,3) finally rose above −2 because it can now "see" the 2.2 cell. Iterating more would raise everything further (since γ=1 and terminals are reachable, values converge).

---

## Question 2(b): Best policy from the U₂ table
Use the **U₂** table (not U₃) and compute Q(s,a) = Σ T·U₂(s′) for every action, then argmax. (No R, no γ.)

These Q-values are the same numbers you computed above in the "iteration 3" step (because iteration 3 *uses* U₂):

| State | N | E | S | W | Stay | **π(s)** |
|---|---|---|---|---|---|---|
| (1,2) | 14.89 | 2.2 | −0.6 | **17.81** | 12.7 | **West** |
| (2,1) | **17.81** | −9.2 | −16.4 | 14.89 | 12.7 | **North** |
| (2,2) | **12.7** | 0.52 | −1.16 | **12.7** | −2 | **North or West (tie)** |
| (2,3) | **2.9** | 0.52 | −1.16 | 0.1 | 2.2 | **North** |
| (3,2) | −7.4 | **−2** | **−2** | −14.6 | **−2** | **East / South / Stay (three-way tie)** — just *not* North or West |
| (3,3) | **0.94** | −2 | −2 | −0.74 | −2 | **North** |

Terminals have no action to choose. Intuition for each:
- (1,2): head West to the +20 (70%); slipping north does nothing (wall).
- (2,1): head North to the +20 (70%); slipping west does nothing (wall). Notice **don't** go South, the −20 is right there!
- (2,3): North to the +5 cell.
- (3,3): North towards the good stuff.
- (3,2): this state is *next to the −20*. North slips west into −20 with 30%; West goes into it 70%. With only two iterations of information there's nothing good to head toward, so the safe options tie.

**Why "after 2 iterations" matters (verified by running value iteration further):** the policy you extract depends on how far the values have spread. Policy read from U₂ vs later tables:
- (3,2): from U₂ a tie (E/S/Stay); from U₃, U₄, U₅ it is **North** (once (2,2) has a high value, the 70% chance of reaching it is worth the 30% slip into −20); at convergence (≈50 iterations) it is **East** (go via (3,3) instead and avoid the −20 risk).
- (2,3): North from U₂, but **West** at convergence (the route toward the +20 beats the +5).
- All other cells keep the same action.
The question tells you to use U₂ on purpose, so you practise the argmax procedure on the table you are given, without waiting for convergence. In the exam, always use the table the question names.

---

## Question 2(c): Evaluate the given policy (γ = 1)
π: (2,1)→W, (2,2)→W, (2,3)→N, (3,2)→N, (3,3)→E, (1,2)→S.
**No max here** — the action in each cell is dictated.

**Iteration 1 (U₀=0):** U₁(s) = R(s) + 0 = −1 for non-terminals; terminals = reward. (Same table as before.)

**Iteration 2 (use U₁):**
- **(2,1), West:** 0.7 → wall → stays (2,1): U₁ = −1; 0.3 (north slip) → (1,1): 20. Σ = −0.7 + 6 = 5.3. U₂ = −1 + 5.3 = **4.3**
- **(2,2), West:** 0.7 → (2,1) = −1; 0.3 (north) → (1,2) = −1. Σ = −1. U₂ = **−2**
- **(2,3), North:** 0.7 → (1,3)=5; 0.3 (west) → (2,2)=−1. Σ = 3.5 − 0.3 = 3.2. U₂ = **2.2**
- **(3,2), North:** 0.7 → (2,2) = −1; 0.3 (west) → (3,1) = −20. Σ = −0.7 − 6 = −6.7. U₂ = **−7.7**
- **(3,3), East:** 1.0 → stays → −1. U₂ = **−2**
- **(1,2), South:** 0.8 → (2,2) = −1; 0.2 (east slip) → (1,3) = 5. Σ = −0.8 + 1 = 0.2. U₂ = −1 + 0.2 = **−0.8**

```
U1:   20    -1    5            U2^π:  20    -0.8    5
      -1    -1   -1                   4.3    -2     2.2
     -20    -1   -1                  -20    -7.7    -2
```

**What it shows:** Policy π is *not optimal* — look at (3,2): its value (−7.7) is much worse than the −2 achievable by the optimal choice, because the policy sends it North, risking the −20. Policy evaluation tells you how good a given rule is; it doesn't improve it.

---

## Question 2(d): Can "Stay" ever be part of an optimal policy?
**Yes.** The hint: look at the reward for non-terminal cells.

Intuition: Stay makes sense whenever *being where you are is more rewarding than anything reachable* — i.e. **R(s) > 0** for a non-terminal cell. Then each step you stay you *collect* a positive reward again.

**Concrete grid.** Two cells in a row: A (non-terminal, R(A) = +1) and B (terminal, R(B) = 0). Discount γ = 0.9, actions {move toward B, Stay}, deterministic.
- Moving to B: U = R(A) + γ·U(B) = 1 + 0.9·0 = **1**.
- Staying forever: U(A) = 1 + 0.9·U(A) ⇒ U(A) = 1/(1−0.9) = **10**.
- 10 > 1 ⇒ **Stay is the optimal action in A.**

*(Why γ < 1: with γ = 1 staying forever would give +∞; the optimum would still be "Stay" but the numbers diverge. Using γ<1 keeps everything finite and the proof clean.)*

**And in Q1's grid?** All non-terminal cells are −1, so staying only loses reward and never helps; if a terminal is reachable, it's better to move. That's why Stay never appears in the optimal policy above.

**General rule:** Stay can be optimal iff the cell's per-step reward is positive enough that collecting it again beats every option involving leaving (and risk). If all non-terminal rewards ≤ 0 and some positive terminal is reachable, Stay is never strictly optimal.

---

## Question 3: R(s,a,s′) ⇄ R(s)

### Background
Two conventions for where rewards live:
- **R(s)**: reward for *being in* a state. (Used in the textbook and this question's grid.)
- **R(s,a,s′)**: reward for *a transition* — "taking action a in state s and landing in s′." (Used by David Silver, most ML literature.)

They're equally expressive; you can convert between them, but you may need extra states.

### Why a conversion needs *extra states*
If the reward depends on **how you got somewhere** (which action, which previous state), then a single state can't carry one fixed R(s) — the same destination would need different rewards depending on the path. Example from the diagram: arriving at s2 via **Study** (from s0) costs −2, but arriving at s2 via **Pub** (from s3) pays +1. A single node "s2" with R(s) can't be both −2 and +1.

### The recipe: make each *kind of arrival* its own state
Turn each *transition* (or each distinct (destination, reward) arrival) into a **new state** whose R(s) equals that transition's reward. Entering the new state pays the reward. From the new state, the outgoing choices and probabilities are exactly those of the original destination.

### The student MDP's transitions
| From | Action | Reward | To |
|---|---|---|---|
| s0 | Study | −2 | s2 |
| s0 | Facebook | −1 | s1 |
| s1 | Facebook | −1 | s1 |
| s1 | Quit | 0 | s0 |
| s2 | Study | −2 | s3 |
| s2 | Sleep | 0 | s4 |
| s3 | Study | +10 | s4 |
| s3 | Pub | +1 | s0 (0.2), s2 (0.4), s3 (0.4) |

### Method A — general (always works): states = transitions
One new state per row (and a start state) — e.g. state "(s0,Study,s2)" with R = −2; its outgoing actions are those of s2. Correct but large.

### Method B — the neat reduction for this MDP
Notice the reward is determined purely by **(destination, action used to arrive)**, with no dependence on the origin state:
- arrive at s1 via Facebook: always −1
- arrive at s0 via Quit: 0; via Pub: +1
- arrive at s2 via Study: −2; via Pub: +1
- arrive at s3 via Study: −2; via Pub: +1
- arrive at s4 via Sleep: 0; via Study: +10

So define states as **(destination, arrival action)**:

| New state | R(s) | Notes |
|---|---|---|
| s0 (initial) | 0 | the start; no arrival |
| (s0, Quit) | 0 | behaves like s0 |
| (s0, Pub) | +1 | behaves like s0 |
| (s1, Facebook) | −1 | behaves like s1 |
| (s2, Study) | −2 | behaves like s2 |
| (s2, Pub) | +1 | behaves like s2 |
| (s3, Study) | −2 | behaves like s3 |
| (s3, Pub) | +1 | behaves like s3 |
| (s4, Sleep) | 0 | terminal |
| (s4, Study) | +10 | terminal |

**Transitions copy the original ones, redirected to the right copy:**
- from any copy of s0: Study → (s2,Study) w.p. 1; Facebook → (s1,Facebook) w.p. 1.
- from (s1,Facebook): Facebook → (s1,Facebook); Quit → (s0,Quit).
- from any copy of s2: Study → (s3,Study); Sleep → (s4,Sleep).
- from any copy of s3: Study → (s4,Study); Pub → (s0,Pub) 0.2, (s2,Pub) 0.4, (s3,Pub) 0.4.

**Caveats you can mention for extra marks:**
1. Rewards are now collected on **arrival** instead of on departure — a one-step shift in time (matters if γ<1; the start state has reward 0).
2. The new MDP has more states, but identical optimal behaviour (same decisions, same expected returns up to that timing shift).
3. The reverse conversion is trivial: R(s) = R(s,a,s′) with the reward ignoring a and s′, i.e. "R(s) is a special case of R(s,a,s′) that doesn't depend on the action or successor."

---

# PART 7 — The mistake catalogue (how each one looks, and the cure)

| # | Mistake | How it shows up | Cure |
|---|---|---|---|
| 1 | Wall rule applied to the action, not each outcome | T((3,3),East) = 0.6 stay + 0.4 south-cell | Check each outcome separately; add blocked ones onto the current cell |
| 2 | Mixing old and new table | A U₂ value changes while you compute another U₂ cell | Two tables; fill the new one only from the old one |
| 3 | Forgetting terminal rule | Computing "max" for (1,1) | Terminals: U = R, always |
| 4 | Adding R inside the max, or per action | U = max_a (R + Σ…) with differing R | R(s) is the same for all actions → add it once outside |
| 5 | Using γ or R in the argmax | Extra clutter, still right mostly | Extraction = just Σ T·U |
| 6 | Mixing up north/south | Moving "up" increases the row | North = row − 1 |
| 7 | Using the wrong slip direction | North slips east | Re-read the table: N→W, E→S, S→E, W→N |
| 8 | Applying `max` in policy evaluation | Evaluating a given policy but choosing the best action | Plug in π(s) only |
| 9 | Not discounting R(s₀) correctly | Dropping the first reward or discounting it | R(s₀) is counted at weight 1 |
| 10 | Arithmetic slips (0.7×(−1)) | Wrong signs | Write each product explicitly (as above) |
| 11 | Claiming a unique policy when there's a tie | "(3,2): East" only | Write "East/South/Stay tie" |
| 12 | Decimals everywhere | Slow, error-prone | Use tenths: 0.7·20 = 14, 0.3·12.7 = 3.81; keep a calculator habit |

---

# PART 8 — Practice with answers (do them cold!)

## P1 — Transition modelling (10 min)
(a) From (2,2), write T((2,2),a,·) for all 5 actions.
(b) From (1,2), action East: both outcomes?
(c) From (3,2), action South: both outcomes?

<details><summary>Answers</summary>

(a) North → (1,2) 0.7, (2,1) 0.3. East → (2,3) 0.6, (3,2) 0.4. South → (3,2) 0.8, (2,3) 0.2. West → (2,1) 0.7, (1,2) 0.3. Stay → (2,2) 1.
(b) East: 0.6 east → (1,3); 0.4 south → (2,2).
(c) South: 0.8 south → wall → stay (3,2); 0.2 east → (3,3). So T = (3,2): 0.8, (3,3): 0.2.
</details>

## P2 — Discounted returns (5 min)
Sequence: (3,3), (2,3), (1,3). γ = 0.9. Compute additive and discounted rewards. Then: with γ = 0.9 what is an endless sequence of +2's worth?

<details><summary>Answers</summary>

Rewards −1, −1, +5.
Additive: 3. Discounted: −1 + 0.9(−1) + 0.81(5) = −1 − 0.9 + 4.05 = **2.15**.
Endless +2: 2/(1−0.9) = **20**.
</details>

## P3 — Variation of Q2: change γ and the step cost (20 min)
Same grid, but non-terminal reward is **−0.04** and **γ = 0.9**. Compute U₁ and U₂ for every cell. (Terminals still 20, −20, 5.)

<details><summary>Answers (verified)</summary>

U₁: non-terminals = −0.04 (terminals as given).
U₂:
```
 20       12.5492     5
 12.5492  -0.076    3.0992
 -20      -0.076   -0.076
```
Worked cell (1,2): best action West: Σ = 0.7·20 + 0.3·(−0.04) = 14 − 0.012 = 13.988; U₂ = −0.04 + 0.9·13.988 = −0.04 + 12.5892 = **12.5492**.
Worked cell (2,3): North: Σ = 0.7·5 + 0.3·(−0.04) = 3.488; U₂ = −0.04 + 0.9·3.488 = **3.0992**.
Worked cell (2,2): all neighbours −0.04 so any action Σ = −0.04; U₂ = −0.04 + 0.9(−0.04) = **−0.076**.
(2,1) mirrors (1,2) by symmetry: **12.5492**.
U₃ for reference: (1,2)=(2,1)=15.9483, (2,2)=11.2543, (2,3)=3.0895, (3,2)=−0.1084, (3,3)=1.892.

Key insight: with γ<1 each step "leaks" a factor of 0.9, so values are slightly smaller than in the γ=1 version, and the small step penalty (−0.04) makes wandering cheap, so (3,3) rises faster. 
</details>

## P4 — Policy extraction from your P3 table (10 min)
Using the U₂ table from P3, find the best action at (2,3) and (3,3).

<details><summary>Answers</summary>

(2,3): N: 0.7·5+0.3·(−0.076) = 3.4772; Stay: 3.0992 (U₂(2,3)); W: 0.3·5+0.7·(−0.076)=1.447; E: 0.6·3.0992+0.4·(−0.076)=1.829; S: 0.2·3.0992+0.8·(−0.076)=0.559. **North** (3.477).
(3,3): N: 0.7·3.0992+0.3·(−0.076) = 2.147; W: 0.3·3.0992+0.7·(−0.076)=0.877; E/S/Stay: −0.076. **North**.
</details>

## P5 — Design question (10 min)
Design a 1×3 gridworld with deterministic moves (left/right/stay) in which "Stay" is optimal at the middle cell but *not* at the left cell.

<details><summary>Answer idea</summary>

Cells L, M, G (G = terminal, reward 10). R(L) = −1, R(M) = +3, γ = 0.9.
- At M: Stay forever = 3/(1−0.9) = 30; going right gets 3 + 0.9·10 = 12 → Stay wins.
- At L: Staying forever = −1/(0.1) = −10, moving right to M gets −1 + 0.9·30 = 26 → move wins.
So Stay is optimal at M but not at L. (Any positive R(M) large enough works.)
</details>

## P6 — Explain it (teach-back; the most important one)
Without notes, explain aloud (or write 5 sentences): (1) why a policy rather than a plan, (2) what U(s) means, (3) why value iteration starts from zeros and still reaches the truth, (4) the difference between max and argmax, (5) what changes between value iteration and policy evaluation.
If you can't, re-read Part 4 and Part 5. *If you can explain it to someone else, you can solve exam variants.*

---

# PART 9 — Exam technique for this topic

1. **Write the rules down first** (compass, slip table, wall rule) — 60 seconds, prevents every systematic error.
2. **Make the neighbour table** (§2.5) before any iteration. It replaces thinking with lookup.
3. **Two tables side by side.** Draw the old grid on the left, the new on the right.
4. **Show one line per cell**, e.g. "U₂(1,2) = −1 + max(5.3, 2.6, 0.2, 13.7, −1) = 12.7". Marks are usually for the method, and a single arithmetic slip doesn't ruin a cell if the working is visible.
5. **Prune with the sanity checks:** the Stay action equals the old value of the cell itself — compare quickly; actions that put 30%+ on a terminal with a big negative reward are almost never best; actions leading toward the biggest positive terminal usually win.
6. **Use symmetry** (e.g. (1,2) and (2,1) came out the same at U₂ and U₃) to avoid recomputing — but only after confirming the geometry really mirrors.
7. **Check each result against the floor:** with R = −1, γ = 1, U_i ≥ −i.
8. **Policy questions:** state the tie when there is one. Don't recompute U; use the table given.
9. **Time check:** a 6-cell iteration should take ~5 minutes once practised.

# PART 10 — What the exam will likely ask (given the tutorials)
- Build an MDP (S, s₀, terminals, A, T, R) for a new gridworld or small graph with different slip probabilities.
- Compute additive/discounted returns for given state sequences; spot a geometric series.
- Do 1–3 iterations of value iteration on a small grid (maybe different γ, different R).
- Extract a policy from a utility table / evaluate a given policy for 1–2 iterations.
- Conceptual: stay optimal? effect of γ? R(s) vs R(s,a,s′) conversion? why discount?
- The same *calculation pattern* with different numbers — which is why the practice in Part 8 (changed γ and reward) is the most valuable thing you can do.

# PART 11 — One-page recap to memorise
```
MDP = (S, s0, terminals, A, T, R)         T(s,a,·) sums to 1; blocked move => stay put
Return = R(s0) + γR(s1) + γ²R(s2) + ...      constant r forever = r/(1−γ)
Q(s,a)  = Σ_s' T(s,a,s') · U_old(s')
U_new(s)= R(s) + γ · max_a Q(s,a)            terminals: U = R
π(s)    = argmax_a Q(s,a)                    (no R, no γ)
Policy evaluation: same as U_new but plug in π(s) instead of max
Sanity: U_i ≥ −i for R=−1, γ=1; value leaks outward 1 step per iteration
```

---

# PART 12 — Checked against the OFFICIAL solution (tute-09-SOL.pdf)

**Result: every number in this guide matches the official solutions.** U₁, U₂, U₃ tables, the policy at (1,2), the policy-evaluation table, 1(b) values (16, −0.625, −∞, −2) all agree. Details worth knowing:

1. **−0.06 vs −0.059.** The official U₃(3,3) is printed as −0.059. The exact value is −1 + (0.7·2.2 + 0.3·(−2)) = −0.06. The −0.059 is a floating-point artefact of their calculator. Write −0.06 (or −0.059); both will be accepted.
2. **Marking style = show the formula with T terms.** The official working for one cell looks like this — copy this format in the exam:
   - U₁((1,2)) = −1 + γ[T((1,2),west,(1,1))·U₀(1,1) + T((1,2),west,(1,2))·U₀(1,2)] = −1 + 1×[0.7×0 + 0.3×0] = −1
   - U₁((1,1)) = 20 + γ[T((1,1),stay,(1,1))·U₀(1,1)] = 20   *(terminal: its only action is "stay", and it keeps U = R)*
   - U₂((1,2)) = −1 + 1×[0.7×20 + 0.3×(−1)] = **12.7**
   - U₃((1,2)) = −1 + 1×[0.7×20 + 0.3×12.7] = **16.81**
   - Official statement to quote: "moving west is the best action (in general you'd compute the term for every action and keep the max)."
3. **Policy question (2b):** the official answer only requires π((1,2)) = west (shown for one cell). Doing all cells (as in Part 6) is more than required, but ties must be stated.
4. **Policy evaluation (2c):** the official table matches (4.3, −2, 2.2, −7.7, −2, −0.8). They stress: "we do not take the max because at every state we know what to do, namely π(s)".
5. **Q2(d) official answer:** "If the reward is positive and large in magnitude for non-terminal states, and γ is small, then it is possible for an agent to choose to stay." Our example (R(A)=+1, terminal reward 0, γ=0.9) is a valid concrete grid. The exact condition: Stay beats leaving to a terminal with reward R_T when R/(1−γ) > R + γ·R_T. Quote the official phrase *and* give a numeric example.
6. **Q3 official method (use these exact words in the exam):** for each state s′ in the original MDP:
   - If **all** transitions arriving at s′ have the **same** reward, keep s′ and give it that reward.
   - Otherwise make a **copy s′_{s,a}** for every incoming transition (s,a,s′) and set R(s′_{s,a}) = R(s,a,s′). Every copy keeps **all outgoing transitions** of s′.

   Applied to the student MDP:

   | Original state | Incoming rewards | New state(s) and R |
   |---|---|---|
   | s1 | Facebook from s0: −1; Facebook from s1: −1 (same) | keep s1, R = **−1** (no copy) |
   | s0 | Quit from s1: 0; Pub from s3: +1 | s0_{s1,quit}: **0**; s0_{s3,pub}: **+1** |
   | s2 | Study from s0: −2; Pub from s3: +1 | s2_{s0,study}: **−2**; s2_{s3,pub}: **+1** |
   | s3 | Study from s2: −2; Pub from s3: +1 | s3_{s2,study}: **−2**; s3_{s3,pub}: **+1** |
   | s4 | Sleep from s2: 0; Study from s3: +10 | s4_{s2,sleep}: **0**; s4_{s3,study}: **+10** |

   Transitions: both copies of s0 go to s1 with probability 1 under Facebook, and to s2_{s0,study} under Study. A copy of s2 goes under Study to s3_{s2,study}; under Sleep to s4_{s2,sleep}. A copy of s3 goes under Study to s4_{s3,study}; under Pub to s0_{s3,pub} (0.2), s2_{s3,pub} (0.4), s3_{s3,pub} (0.4). This is the same MDP as "Method B" in Part 6, with the official naming.

# PART 13 — Where this sits in the textbook (AIMA 4th ed., Russell & Norvig)
This week's reading (chapters 15–16, highlighted sections only):
| Section | What it gives you | Maps to this tutorial |
|---|---|---|
| 15.1 Combining Beliefs and Desires under Uncertainty | The Maximum Expected Utility (MEU) principle: pick the action with the highest expected utility | Q2(b) "using the MEU principle" = argmax of Σ T·U |
| 15.2 The Basis of Utility Theory | Why preferences can be turned into numbers (utility) | Why "utility" is a sensible thing to maximise |
| 15.3 Utility Functions | What utility numbers mean (e.g. utility of money, risk) | Concept only; low exam weight |
| 16.1 Sequential Decision Problems | The MDP definition, rewards over time, additive vs discounted utility, optimal policy | Q1 (all), 1(b) |
| 16.2 Algorithms for MDPs | The Bellman equation, **value iteration**, **policy iteration** | Q2 (a)(b)(c) |

Note the book writes the reward as R(s,a,s′) and the Bellman equation as U(s) = max_a Σ P(s′|s,a)[R(s,a,s′) + γU(s′)]; the tutorial uses R(s) (Q3 is exactly about converting between them). Policy iteration (also in 16.2) = alternate "evaluate the policy" (Q2c) and "improve the policy by argmax" (Q2b) until nothing changes — you already know both halves.
