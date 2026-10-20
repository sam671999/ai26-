# Self-check tool for Tutorial 9. Do the maths by hand FIRST, then run: python3 mdp_checker.py
# Edit R_T, OUT, or the gamma in vi(n, g) to check your own variants of the question.
from fractions import Fraction as F
R_T={(1,1):20,(3,1):-20,(1,3):5}
terminals=set(R_T)
states=[(r,c) for r in (1,2,3) for c in (1,2,3)]
def R(s): return R_T.get(s,-1)
D={'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1),'X':(0,0)}
OUT={'N':[('N',.7),('W',.3)],'E':[('E',.6),('S',.4)],'S':[('S',.8),('E',.2)],'W':[('W',.7),('N',.3)],'X':[('X',1.0)]}
def move(s,d):
    r,c=s[0]+D[d][0],s[1]+D[d][1]
    return (r,c) if 1<=r<=3 and 1<=c<=3 else s
def T(s,a):
    out={}
    for d,p in OUT[a]:
        s2=move(s,d); out[s2]=out.get(s2,0)+p
    return out
print("T((3,3),a,.):")
for a in 'NESWX': print(a,T((3,3),a))
def q(s,a,U): return sum(p*U[s2] for s2,p in T(s,a).items())
def vi(n,g=1.0):
    U={s:0.0 for s in states}; hist=[dict(U)]
    for i in range(n):
        N={}
        for s in states:
            N[s]=R(s) if s in terminals else R(s)+g*max(q(s,a,U) for a in 'NESWX')
        U=N; hist.append(dict(U))
    return hist
h=vi(3)
for i in range(1,4):
    print("U",i)
    for r in (1,2,3): print("  ",[round(h[i][(r,c)],4) for c in (1,2,3)])
U2=h[2]
print("policy from U2")
for s in states:
    if s in terminals: continue
    qs={a:round(q(s,a,U2),4) for a in 'NESWX'}
    print(s,qs,max(qs,key=qs.get))
pi={(2,1):'W',(2,2):'W',(2,3):'N',(3,2):'N',(3,3):'E',(1,2):'S'}
U={s:0.0 for s in states}
for i in (1,2):
    N={}
    for s in states:
        N[s]=R(s) if s in terminals else R(s)+q(s,pi[s],U)
    U=N
    print("policy eval iter",i)
    for r in (1,2,3): print("  ",[round(U[(r,c)],4) for c in (1,2,3)])
