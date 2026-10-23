# Tutorial 10 sheet: Reinforcement Learning (AIMA ch.23: 23.1-23.3, plus 23.4 lightly)

RL = an MDP where the agent does NOT know T(s,a,s') or R. It must learn from experience (trials/episodes).
- Passive RL: the policy is FIXED; learn how good it is (utilities U^pi).
- Active RL: no fixed policy; learn what to do (Q-values / a policy).
- Model-based: learn T (and R) then compute. Model-free: learn values directly, no T.

## Passive RL (23.2)
Direct utility estimation: U(s) = average of the observed total future reward from s. Simple, but slow and ignores the link between neighbouring states.
ADP (adaptive dynamic programming, model-based):
  N(s,a) = how many times action a was taken in s
  N(s,a,s') = how many times that led to s'
  T_hat(s,a,s') = N(s,a,s') / N(s,a)
  then evaluate the policy with the learned model (policy evaluation from T9).
TD (temporal difference, model-free), after EACH observed step s -> s':
  U(s) <- U(s) + alpha * [ R(s) + gamma*U(s') - U(s) ]
  sample = R(s) + gamma*U(s'); error = sample - U(s). alpha = learning rate.
  Update in the order observed; U(s') is its CURRENT value.
  Convention to confirm with the solution PDF: when a terminal state is first reached, its utility is set to its reward.

## Active RL (23.3)
Q-learning (model-free, off-policy), after each step (s, a, s'):
  Q(s,a) <- Q(s,a) + alpha * [ R(s) + gamma * max over a' of Q(s',a') - Q(s,a) ]
  Terminal states: no updates; when s' is terminal set all its Q-values to its reward (the "exit" action).
SARSA (on-policy) uses Q(s',a') for the action a' actually taken, instead of the max.
Exploration vs exploitation:
  "occasionally random": with probability 1/t take a random action, otherwise the greedy action.
  Exploration function f(u,n) = R+ if n < N_e else u  (optimism: untried actions look great until tried N_e times).

## Generalisation (23.4)
Too many states for a table: approximate U or Q with features:  U_theta(s) = theta_1*f_1(s) + ... + theta_n*f_n(s)
Update each weight:  theta_i <- theta_i + alpha*[R + gamma*U_theta(s') - U_theta(s)] * f_i(s)
Good features are cheap, informative about winning (e.g. chess: material count, mobility, king safety).

## Modelling an RL problem (tutorial Q2b)
State = what the agent needs to know; actions = what it can do; reward = when/what signal (sparse at the end vs frequent); episodic or continuing; discount.

## Successor-state axioms (tutorial Q3e)
F_t <=> (an action at t-1 made F true) OR (F_{t-1} AND no action at t-1 made F false)
Ask: how can F become true? How can it stay true? Check each case against the world's rules (walls, locked gate, key).
