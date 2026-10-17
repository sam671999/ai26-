# COSC3117 — Tutorial 9: MDPs & Value Iteration (Study Guide)

**How to use this (important):** reading solutions feels like learning but isn't. For every question:
1. Read the **Concept** section once (15 min).
2. Close the file. Attempt the question on paper.
3. Only then open the **Solution** and mark yourself. Re-do anything you got wrong *the next day* from a blank page.

`mdp_checker.py` recomputes everything. Change the numbers and check your hand-work against it.

---

## 0. The whole topic in 5 sentences

- An **MDP** is a world where actions have *random* outcomes. You pick an action; nature picks the result.
- Each state gives a **reward** R(s). Your goal is the best *total (discounted) reward over time*, not just the next step.
- The **utility** U(s) = the expected total discounted reward if you start in s and act optimally from there.
- **Value iteration** finds U(s) by repeating one update (the Bellman update) on every state until the numbers stop changing.
- A **policy** π(s) says which action to take in each state. The best policy picks, in each state, the action with the highest expected next-state utility.

## 1. Concepts you must be able to explain from memory

### 1.1 The MDP tuple
| Symbol | Meaning | In Q1 |
|---|---|---|
| S | set of states | 9 cells (r,c) |
| s₀ | start state | (3,3) |
| terminals | states where the episode ends | (1,1), (3,1), (1,3) |
| A | actions | {N, E, S, W, Stay} |
| T(s,a,s′) | P(s′ \| s, a) | the 70/30, 60/40, 80/20 rules |
| R(s) | reward for being in s | 20, −20, 5 on terminals; −1 elsewhere |

**Exam habit:** for any T(s,a,·), the probabilities must sum to 1. Check this every time.

### 1.2 Walls — the #1 place marks are lost
"If an action causes the agent to travel into a wall, it stays." So the *probability mass is not lost*, it moves onto the **current cell**.
Example, from (3,3) doing East: 60% "east" → wall → stay at (3,3); 40% "south" → wall → stay at (3,3). Total: T((3,3),East,(3,3)) = **1.0**.

### 1.3 Additive vs discounted reward
- Additive: R(s₀)+R(s₁)+…
- Discounted: R(s₀) + γR(s₁) + γ²R(s₂) + …
- Why discount? (a) Infinite sequences give −∞ or +∞ additively but a finite number discounted (geometric series: if every reward is r, total = r/(1−γ)). (b) Models "sooner is better".

### 1.4 The two equations
**Value iteration (has a `max`):**

U_{i+1}(s) = R(s) + γ · max_a Σ_{s′} T(s,a,s′) · U_i(s′)

**Policy extraction (has an `argmax`, no R, no γ):**

π*(s) = argmax_a Σ_{s′} T(s,a,s′) · U(s′)

**Policy evaluation (a fixed policy — NO max, just plug in π(s)):**

U^π_{i+1}(s) = R(s) + γ · Σ_{s′} T(s,π(s),s′) · U^π_i(s′)

> max/min gives a **number**; argmax/argmin gives the **action that achieves it**. (That's what the video link in the tutorial is about.)

### 1.5 Terminal states
Terminal states are never updated: **U(terminal) = R(terminal)** at every iteration (from iteration 1 on). U₀ is 0 for everything, including terminals.

### 1.6 The recipe for one state in one iteration (memorise this loop)
1. For each action a, list the outcomes (s′, probability).
2. Look up U_i(s′) for each outcome *from the previous table* (never from the one you're filling in).
3. Q(s,a) = Σ probability × U_i(s′).
4. Take the best Q. U_{i+1}(s) = R(s) + γ × that best Q.

Always fill the whole new table from the **old** table. Mixing them is the second most common error.

---

## 2. Question 1 — Build the MDP

Grid (row, col). North = row−1, South = row+1, East = col+1, West = col−1.

```
        col1  col2  col3
row1     20    -1     5      <- (1,1) and (1,3) terminal
row2     -1    -1    -1
row3    -20    -1    -1      <- (3,1) terminal, start = (3,3)
```

### 1(a) Solution
- **i. States:** all 9 cells (1,1)…(3,3).
- **ii. Start:** (3,3). **Terminals:** (1,1), (3,1), (1,3).
- **iii. Actions:** North, East, South, West, Stay.
- **iv. T from (3,3):**

| Action | Outcome s′ | P |
|---|---|---|
| North | (2,3) | 0.7 |
| North | (3,2) (the 30% "west") | 0.3 |
| East | (3,3) (wall either way) | 1.0 |
| South | (3,3) (wall either way) | 1.0 |
| West | (3,2) | 0.7 |
| West | (2,3) (the 30% "north") | 0.3 |
| Stay | (3,3) | 1.0 |

All other T((3,3),a,s′) = 0.
- **v. R(s):** R(1,1)=20, R(3,1)=−20, R(1,3)=5, R(s)=−1 for the other 6 cells.

### 1(b) Solution
**(a)** (3,3),(2,3),(2,2),(2,1),(1,1) → rewards −1, −1, −1, −1, +20
- Additive: −4 + 20 = **16**
- Discounted γ=0.5: −1 − 0.5 − 0.25 − 0.125 + 20(0.5⁴) = −1.875 + 1.25 = **−0.625**

**(b)** (3,3),(3,2),(2,2),(2,3), repeat → every reward is −1, forever
- Additive: **−∞**
- Discounted: −1/(1−0.5) = **−2**

*Lesson:* additive says (a) is great and (b) is a disaster; discounted still prefers (a) but (b) is now a finite number. The first reward R(s₀) is included (no discount on step 0).

---

## 3. Question 2 — Value Iteration (γ = 1)

### 2(a)(i) Solution — two iterations
**U₁:** terminals = their reward; every other cell = −1 + max(0) = **−1**.

```
U1:   20   -1    5
      -1   -1   -1
     -20   -1   -1
```

**U₂** — worked examples (use the U₁ table):
- (1,2): best action West: 0.7·U₁(1,1) + 0.3·U₁(1,2) [north = wall → stay] = 14 + (−0.3) = 13.7 → U₂ = −1 + 13.7 = **12.7**
- (2,1): best action North: 0.7·20 + 0.3·U₁(2,1) [west = wall → stay] = 13.7 → **12.7**
- (2,3): best action North: 0.7·5 + 0.3·U₁(2,2) = 3.5 − 0.3 = 3.2 → **2.2**
- (2,2): every action gives −1 at best → **−2**
- (3,3): North: 0.7(−1)+0.3(−1) = −1 → **−2**
- (3,2): North is terrible (30% into −20: 0.7(−1)+0.3(−20) = −6.7). East/South/Stay give −1 → **−2**

```
U2:   20   12.7    5
     12.7   -2    2.2
      -20   -2    -2
```

### 2(a)(ii) Solution — third iteration
```
U3:   20   16.81    5
     16.81  11.7   1.9
      -20   -3    -0.06
```
Spot checks:
- (1,2): −1 + (0.7·20 + 0.3·12.7) = −1 + 17.81 = **16.81**
- (2,2): −1 + (0.7·12.7 + 0.3·12.7) = **11.7** (north or west; both lead toward 12.7 cells)
- (2,3): −1 + (0.7·5 + 0.3·(−2)) = −1 + 2.9 = **1.9**
- (3,3): −1 + (0.7·2.2 + 0.3·(−2)) = −1 + 0.94 = **−0.06**
- (3,2): stay/east/south give −2 → **−3**

*Watch the story in the numbers:* value "leaks outward" from the +20 corner one step per iteration. That's why value iteration works.

### 2(b) Solution — policy from U₂ (argmax of Σ T·U₂)
| State | Best action | Q-values (N / E / S / W / Stay) |
|---|---|---|
| (1,2) | **West** | 14.89 / 2.2 / −0.6 / **17.81** / 12.7 |
| (2,1) | **North** | **17.81** / −9.2 / −16.4 / 14.89 / 12.7 |
| (2,2) | **North or West** (tie) | **12.7** / 0.52 / −1.16 / **12.7** / −2 |
| (2,3) | **North** | **2.9** / 0.52 / −1.16 / 0.1 / 2.2 |
| (3,2) | East / South / Stay (tie at −2) — anything but N or W | −7.4 / −2 / −2 / −14.6 / −2 |
| (3,3) | **North** | **0.94** / −2 / −2 / −0.74 / −2 |

Notes: with only two iterations, (3,2) can't "see" any good thing yet — ties are normal and acceptable; **state the tie** in the exam. Notice (3,2) avoids North and West because of the 30% slip into the −20 cell.

### 2(c) Solution — evaluate the given policy
π: (2,1)→W, (2,2)→W, (2,3)→N, (3,2)→N, (3,3)→E, (1,2)→S. **No max** — just plug in the given action.

**U₁:** same as before (−1 for non-terminals, terminals = reward).

**U₂** (use U₁):
- (2,1), W: 0.7 → wall → stay (−1); 0.3 → north (1,1) = 20 → −0.7 + 6 = 5.3 → −1 + 5.3 = **4.3**
- (2,2), W: 0.7·U₁(2,1) + 0.3·U₁(1,2) = −1 → **−2**
- (2,3), N: 0.7·5 + 0.3·(−1) = 3.2 → **2.2**
- (3,2), N: 0.7·U₁(2,2) + 0.3·U₁(3,1) = −0.7 − 6 = −6.7 → **−7.7**
- (3,3), E: wall → stay → **−2**
- (1,2), S: 0.8·U₁(2,2) + 0.2·U₁(1,3) = −0.8 + 1.0 = 0.2 → **−0.8**

```
U2^π: 20   -0.8    5
      4.3   -2    2.2
      -20  -7.7   -2
```
*(3,2) = −7.7 shows this is a bad policy there — walking north risks the −20 cell.*

### 2(d) Solution — can "stay" ever be optimal?
**Yes.** Positive reward on non-terminal cells and γ < 1.
Example: two cells, A (non-terminal, R(A)=+1) and a terminal B (R(B)=0), γ=0.9.
- Leave to B: gets 1 + 0.9·0 = 1.
- Stay forever: U(A) = 1 + 0.9·U(A) → U(A) = 1/(1−0.9) = **10**.
10 > 1, so Stay is optimal. (If every non-terminal reward is ≤ 0 and a terminal is reachable, staying only bleeds reward, so it's never strictly better — that's why Stay isn't optimal in Q1.)

---

## 4. Question 3 — R(s,a,s′) ⇄ R(s)

**Idea:** you can't hang a reward on an *edge* if rewards only live on *nodes*, so **turn each edge you care about into a node.** Entering that node pays the edge's reward.

Student MDP rewards (action, from→to):
- s0: Study −2 → s2; Facebook −1 → s1
- s1: Facebook −1 → s1; Quit 0 → s0
- s2: Study −2 → s3; Sleep 0 → s4
- s3: Study +10 → s4; Pub +1 → s0 (0.2) / s2 (0.4) / s3 (0.4)

**General method (always works):** new state = the transition (s,a,s′). R(new state) = R(s,a,s′). Transitions out of a new state are those of s′.

**Neat shortcut here:** the reward depends only on *(destination, action used to get there)*, so define states as "(destination, how I arrived)":

| New state | R(s) |
|---|---|
| s0 (start) | 0 |
| (s0,Quit) | 0 |
| (s0,Pub) | +1 |
| (s1,Facebook) | −1 |
| (s2,Study) | −2 |
| (s2,Pub) | +1 |
| (s3,Study) | −2 |
| (s3,Pub) | +1 |
| (s4,Sleep) | 0 (terminal) |
| (s4,Study) | +10 (terminal) |

Transitions copy the original: e.g. from (s2,Study) the action Study goes to (s3,Study) with prob 1; from any "s3" copy, action Pub goes to (s0,Pub) 0.2 / (s2,Pub) 0.4 / (s3,Pub) 0.4.
**Caveat to mention:** rewards are now received on *arrival*, so there's a one-step timing shift; the start state's own reward is 0.

---

## 5. Self-test (do these cold, no notes, then check with `mdp_checker.py`)

1. From (2,2), write T((2,2), a, ·) for all five actions. (Hint: no walls to worry about.)
2. Same grid but R(non-terminal) = −0.04 and γ = 0.9. Compute U₁ and U₂ for (1,2), (2,1), (2,3). Does (2,3)'s best action change?
3. In 2(a), why is U₂(3,2) = −2 and not −7.7?
4. Explain in two sentences why discounting makes an infinite loop of −1 rewards worth −2 at γ = 0.5.
5. Given U₂, what is the *only* thing you must change in the update equation to evaluate a fixed policy instead of finding the best one?
6. Make up a 1×3 grid where Stay is optimal at one cell and not at another.

## 6. Exam traps checklist
- [ ] Wall → agent stays on the **current** cell (probabilities still sum to 1)
- [ ] Terminal U = R, constant
- [ ] Fill the new table from the old table only
- [ ] Policy evaluation: no `max`; policy extraction: no `R`, no `γ`
- [ ] Say "tie" when there is one
- [ ] Include R(s₀) in the cumulative reward, undiscounted
- [ ] Write one line of workings per cell (partial marks!)
