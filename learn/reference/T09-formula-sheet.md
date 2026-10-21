# Tutorial 9 formula sheet (MDPs, value iteration, policies)

## 0. Set-up (Q1 "build the MDP")
MDP = (S, s0, terminals, A, T, R)
- S: all squares (row, column). s0: start. Terminals: the exits. A: {north, east, south, west, stay}.
- Directions: north = row-1, south = row+1, east = col+1, west = col-1.
- T(s,a,s') = probability of landing on s' after action a on s.
  1. List each random outcome (intended + slip) with its probability.
  2. Find the landing square; a wall means stay on the current square.
  3. If two outcomes land on the same square, ADD their probabilities. Total must be 1.
- R(s): reward for being on square s (terminals have their own reward).

## 1. Adding up rewards over time
- Additive:   R0 + R1 + R2 + ...
- Discounted: R0 + g*R1 + g^2*R2 + ...   (g = gamma, 0 <= g <= 1; R0 has weight 1)
- Same reward r forever:  S = r / (1 - g)      (trick: S = r + g*S)
- Utility bound: U <= Rmax / (1 - g)
- Bigger g = future matters MORE. Additive sum of endless -1s = -infinity (write the sign).

## 2. Expected utility of one move
EU(s,a) = SUM over s' of  T(s,a,s') * U(s')        (probability x value, then add)
MEU principle: choose the action with the highest EU.

## 3. Value iteration (Q2a)
- U0(s) = 0 for all s.   U1(s) = R(s).
- U_{i+1}(s) = R(s) + g * max over a of [ SUM over s' of T(s,a,s') * U_i(s') ]
- Terminals: U(s) = R(s) always (no max, no future).
- Use ONLY the old table U_i on the right-hand side. Write "using U_i" above each block.
- Compute all FIVE actions per square (include Stay). Add R(s) once, outside the max.

## 4. Best move per square = policy extraction (Q2b)
pi(s) = argmax over a of [ SUM over s' of T(s,a,s') * U(s') ]
- No R(s), no gamma. Answer is the MOVE, not the value. Say "tie" if there is one.
- Use the table the question names (e.g. U2).

## 5. Judging a given policy = policy evaluation (Q2c)
U^pi_0 = 0,  U^pi_1(s) = R(s)
U^pi_{i+1}(s) = R(s) + g * SUM over s' of T(s, pi(s), s') * U^pi_i(s')
- No max: use only the move the policy gives. Terminals fixed at R.

## 6. Concept answers
- Can "stay" be optimal (Q2d)? Yes. Stay forever is worth R/(1-g). Stay beats leaving when
  R/(1-g) > R + g*(value of what leaving gives). Needs a POSITIVE reward per turn and a high enough g.
  Example: cafe pays +2/turn, exit pays +10 once, g = 0.9: stay = 20, go = 2 + 0.9*10 = 11 -> stay.
  With g = 0.5: stay = 4, go = 7 -> go. With -1 per turn staying only loses points.
- Policy vs plan: random outcomes mean you need an action for EVERY square (a policy), not a fixed list.
- Why discount: sooner is better, and endless sums stay finite.

## 7. R(s,a,s') -> R(s) (Q3)
For each square s':
- If every move that ARRIVES at s' has the same reward: keep s' with that reward.
- Otherwise make a copy of s' for each different arriving reward (name it s'_{from,action}), reward = that move's reward.
- Each copy keeps ALL the outgoing moves of s'; moves now lead to the right copy.
- A start square nothing arrives at: reward 0.
- Check: total reward along any route must match before and after.

## 8. Exam habits
- Re-add each final line; sanity-check signs and size.
- Round i reads from round i-1 only. Include Stay. Exits keep their reward.
- Show one line of working per cell.
