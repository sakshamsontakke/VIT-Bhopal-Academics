# Differential Equations — Exam-Oriented Analysis & Sample Question Paper

**Source material analyzed:**
1. *Ordinary Differential Equation — First Order and First Degree* (183 slides, VIT Bhopal, Dr. Juhi Kesarwani & Dr. Ashish Kumar Kesarwany, Aug 19 2026)
2. *Second Order Linear Differential Equations — Linear DE with Constant Coefficients* (101 slides, same authors, Aug 25 2026)

> **Important scope note (read before using this paper):** Both source files are **lecture/tutorial slide decks** — they contain definitions, worked examples, and end-of-topic practice-exercise banks. They are **not** a leaked previous-year paper, so there is no direct evidence in the source of the university's official blueprint (exact duration, total marks, or section layout). Section 4 below therefore uses an **inferred** pattern — a standard 2/4/10-mark, Part A/B/C structure common to short-cycle (CAT-style) university tests — built from the *density and structure* of the exercises themselves. Treat the mark scheme and duration as a reasonable simulation, not a confirmed fact.
>
> Also note: the lecture explicitly states that **only two P.I. methods are in the syllabus — Variation of Parameters and the Method of Undetermined Coefficients.** The classical inverse-operator ("$1/f(D)$") shortcut method is explicitly *excluded* by the instructor. This paper does not test the operator method for that reason.

---

## 1. PDF Analysis

### 1.1 Topics identified

**PDF 1 — First order, first degree ODEs** (9 ToC sections, ~44 worked examples/exercise-sets, ~230 individual practice problems across all exercise sets):
- Introduction: definition of a DE, order & degree, general vs. particular solution, initial value problems (IVP), classification by type (ODE/PDE), order, and linearity
- Survey of 8 solution techniques (separable, homogeneous, reducible-to-homogeneous, linear, reducible-to-linear, exact, non-exact, substitution)
- Separation of variables (2 exercise sets, 20 problems)
- Homogeneous differential equations, $y = vx$ substitution (2 exercise sets, 22 problems)
- Linear first-order DE, integrating factor $e^{\int P\,dx}$ (4 exercise sets, 36 problems — the single most-drilled technique)
- Equations reducible to linear / **Bernoulli's equation**, substitution $v = y^{1-n}$ (3 exercise sets, 24 problems)
- Exact differential equations: test $\partial M/\partial y = \partial N/\partial x$, **full proof** of the necessary-and-sufficient condition, plus 3 "miscellaneous" exercise sets that mix all first-order methods together (5 exercise sets total, ~57 problems)
- Applications: Newton's Law of Cooling (7 exercises, 2 fully worked examples — forensic/murder-time and pizza-cooling problems), mixing/tank problems (1 worked example, 2 exercises), growth & decay (2 worked examples, 5 exercises), falling-body/air-resistance (2 worked examples, 1 exercise), RL/RC electrical circuits (2 worked examples, 2 exercises)
- Simultaneous differential equations solved by the $D$-operator elimination method (2 worked examples, 4 exercise sets)

**PDF 2 — Second-order linear DE with constant coefficients** (5 ToC sections, ~15 worked examples, ~45 practice problems):
- Introduction: standard form $\dfrac{d^2y}{dx^2}+P_1\dfrac{dy}{dx}+P_2y=Q$, superposition theorem (with proof), Complementary Function (C.F.) / Particular Integral (P.I.) definitions and proof that C.F. + P.I. is the general solution, operator notation $D$
- Rule for the Complementary Function via the **Auxiliary Equation**: Case I (real, distinct roots), Case II (repeated roots), Case III (complex conjugate roots), Case IV (repeated complex pairs) — 1 large exercise set of **15** problems, mostly IVPs
- Particular Integral — **Method of Variation of Parameters** (full derivation via Wronskian, 4 worked examples, 1 exercise set of 6 problems)
- Particular Integral — **Method of Undetermined Coefficients** (choice table with Basic/Modification/Sum rules, 5 worked examples, 4 exercise sets including a distinctive "write down the trial P.I. only" question type)
- Applications: spring–mass SHM and RLC circuits, both modeled by the same $ay''+by'+cy=F(t)$ form (2 worked examples, 5 exercises)

### 1.2 Key formulas / concepts an examiner can draw on
| Method | Core formula |
|---|---|
| Separable | $\int \dfrac{dy}{g(y)} = \int f(x)\,dx + C$ |
| Homogeneous | $y=vx \Rightarrow v+x\dfrac{dv}{dx}=f(v)$ |
| Linear (1st order) | I.F. $=e^{\int P\,dx}$; $y\cdot$I.F. $=\int Q\cdot$I.F.$\,dx+C$ |
| Bernoulli | $v=y^{1-n}$ reduces $\dfrac{dy}{dx}+Py=Qy^n$ to a linear DE in $v$ |
| Exact | Solve if $\dfrac{\partial M}{\partial y}=\dfrac{\partial N}{\partial x}$; solution = (terms of $\int M\,dx$) + (remaining terms of $\int N\,dy$) $=C$ |
| 2nd-order C.F. | Roots of $m^2+P_1m+P_2=0$: real distinct → $c_1e^{m_1x}+c_2e^{m_2x}$; repeated → $(c_1+c_2x)e^{mx}$; complex $\alpha\pm i\beta$ → $e^{\alpha x}(c_1\cos\beta x+c_2\sin\beta x)$ |
| Variation of parameters | $u'=-\dfrac{Qy_2}{W}$, $v'=\dfrac{Qy_1}{W}$, $W=y_1y_2'-y_2y_1'$; $y_p=uy_1+vy_2$ |
| Undetermined coefficients | Trial function from the Basic Rule table; **multiply by $x$ (or $x^2$)** if the trial term duplicates a C.F. term (Modification Rule) |

### 1.3 Repeated / emphasized concepts (highest signal)
- **Linear first-order DE** and **Exact DE** are each drilled across 4–5 separate exercise sets — the single strongest signal in the whole corpus.
- **Newton's Law of Cooling** is the most-repeated *application*, appearing in two fully-worked examples and seven follow-up exercises with near-identical structure (find $k$ from one data point, then answer a temperature/time sub-question).
- The **Auxiliary Equation root-cases (I–III)** are drilled hard in a single 15-question block in PDF 2 — almost all of them are IVPs (general solution *and* apply initial conditions), so "solve the IVP" is clearly the expected question format for this topic, not just "find the general solution."
- **Undetermined coefficients with the Modification Rule** (resonance, i.e. when the forcing term duplicates a C.F. term) is explicitly tested as its own micro-skill via "just write down the trial $y_p$" questions — a distinctive, low-effort-but-high-signal question type worth knowing about.
- Three whole exercise sets in PDF 1 ("miscellaneous problems") give a DE **without naming its type** — the hidden skill being tested is correctly *identifying* which of the 6 first-order methods applies before solving.

### 1.4 Observed question pattern (inferred)
Based on the structure of the worked examples and exercises, an exam drawing on this material would plausibly contain:
1. Short definitional/identification questions (order & degree, exactness condition, type of C.F. case) — low mark value
2. "Solve the following differential equation" — general-solution problems, one per major technique
3. "Solve the following IVP" — same techniques but with an initial condition to apply, worth slightly more due to the extra algebra
4. "Show that the equation is exact/homogeneous/Bernoulli and hence solve it" — a hybrid identify-then-solve question
5. Word-problem applications with 2–3 sub-parts (a),(b),(c), mirroring the cooling/growth/spring examples almost exactly
6. Occasional theorem/proof questions (exactness N&S condition, superposition principle)
7. A conceptual "write down only the trial particular integral" question (undetermined coefficients)

### 1.5 Difficulty analysis
- **Easy:** order/degree identification, stating a theorem/formula, Case I/II auxiliary-equation problems with integer roots
- **Medium:** separable/homogeneous/linear/Bernoulli/exact general-solution and IVP problems, Case III (complex-root) problems, straightforward undetermined-coefficients problems (no resonance)
- **Hard:** variation-of-parameters problems involving $\tan$, $\sec$, or $\ln$ integrals; undetermined-coefficients problems *with* resonance (Modification Rule); multi-part application word problems; miscellaneous problems where the method isn't named; theorem proofs

---

## 2. Most Important Topics (ranked)

| Rank | Topic | Ranking rationale |
|---|---|---|
| 🔥 Very High | **Linear first-order DE (integrating factor)** | 4 exercise sets, 36 problems, 6 fully worked examples — most-repeated technique in either PDF |
| 🔥 Very High | **Exact differential equations** (test + solve) | 5 exercise sets (~57 problems) + a full theorem proof — second most-repeated technique, and the only one with an accompanying proof |
| 🔥 Very High | **2nd-order C.F. — all three root cases** | Single 15-question exercise block, almost entirely IVPs; foundational to everything else in PDF 2 |
| 🔥 Very High | **Homogeneous DE ($y=vx$)** | 2 exercise sets, 22 problems, 5 worked examples including 2 IVPs |
| 🔥 Very High | **Bernoulli's equation** | 3 exercise sets, 24 problems, 4 worked examples |
| 🔥 Very High | **Newton's Law of Cooling** | Most-repeated *application*: 2 worked examples + 7 near-identical exercises |
| 🟠 High | **Undetermined coefficients (incl. Modification Rule)** | Full choice-table + 5 examples + 4 exercise sets; the dedicated "guess the trial $y_p$" exercise signals it's tested as a distinct skill |
| 🟠 High | **Variation of parameters** | 4 fully worked examples (including one full IVP) + 1 exercise set; guaranteed at least one long-answer question given the method's prominence |
| 🟠 High | **Order and degree** | Small in volume (1 dedicated 4-question set) but a natural, easy-marks opening question |
| 🟠 High | **Simultaneous DE (D-operator elimination)** | 2 worked examples + 4 exercise sets; connects directly back to the 2nd-order auxiliary-equation skill |
| 🟡 Medium | **Growth & Decay (population/radioactive)** | 2 worked examples + 5 exercises, but less repeated than cooling |
| 🟡 Medium | **Mixing / tank problems** | 1 worked example + 2 exercises |
| 🟡 Medium | **Spring–mass SHM / RLC 2nd-order applications** | 2 worked examples + 5 exercises; direct analog table given (mechanical ↔ electrical) |
| 🟡 Medium | **"Miscellaneous" mixed-method problems** | 3 large unlabelled exercise sets — high volume but low certainty on which specific problem an examiner would pick |
| 🟡 Medium | **Exactness / superposition theorem proofs** | Each appears exactly once, but full proofs given prominent slide-time — plausible for a "state and prove" question |
| ⚪ Low | **Falling body with air resistance** | Only 2 worked examples + 1 exercise |
| ⚪ Low | **RL/RC first-order circuits** | Only 2 worked examples + 2 exercises |
| ⚪ Low | **Homogeneous-function degree checking (standalone)** | Normally just a stepping-stone into the homogeneous-DE method, not tested alone |
| ⚪ Low | **Case IV (repeated complex-pair roots, 4th-order AE)** | Appears exactly once, and is a higher-order edge case unlikely at introductory level |
| ⚪ Low | **Non-constant-coefficient "twist" (variable P₁,P₂)** | One outlier exercise (Ex. 2 #3 in PDF 2) with a variable-coefficient DE where the C.F. is *given* — atypical of the rest of the syllabus |

---

## 3. High-Probability Question Bank

### 🔥 Very High Probability

| # | Question (paraphrased/modified from source pattern) | Topic | Marks | Difficulty | Reason it's likely | Source |
|---|---|---|---|---|---|---|
| 1 | Solve $\dfrac{dy}{dx}+\dfrac{3}{x}y = x^2$ | Linear DE | 4–5 | Medium | Most-repeated technique overall | PDF1 Ex.5–8 pattern |
| 2 | Solve the IVP $\dfrac{dy}{dx}-y\tan x=\sin x,\ y(0)=0$ | Linear DE (IVP) | 5 | Medium | Directly mirrors a fully worked example | PDF1 example, p.68 |
| 3 | Test for exactness and solve $(3x^2y+2y)dx+(x^3+2x+3y^2)dy=0$ | Exact DE | 5 | Medium | 2nd most-repeated technique | PDF1 Ex.13 pattern |
| 4 | State and prove the necessary and sufficient condition for $Mdx+Ndy=0$ to be exact | Exact DE (theory) | 5–10 | Medium–Hard | Only fully-proved theorem in PDF1 | PDF1 pp.100–103 |
| 5 | Solve $x(x-y)\,dy+y^2\,dx=0$ | Homogeneous DE | 5 | Medium | Directly mirrors a fully worked example | PDF1 example, p.41 |
| 6 | Solve the IVP $\dfrac{dy}{dx}=\dfrac{x+y}{x-y},\ y(1)=0$ | Homogeneous DE (IVP) | 5 | Medium–Hard | Homogeneous + IVP is the recurring combo | PDF1 example, p.49 |
| 7 | Solve $\dfrac{dy}{dx}+\dfrac{2}{x}y=x^3y^2$ | Bernoulli's equation | 5 | Medium | 3rd most-repeated technique | PDF1 Ex.9–11 pattern |
| 8 | Solve the IVP $y''-5y'+6y=0,\ y(0)=1, y'(0)=1$ | 2nd order C.F. (real distinct roots) | 4–5 | Easy–Medium | Case I is the most basic and most-drilled 2nd-order skill | PDF2 Ex.1 pattern |
| 9 | Solve $y''-6y'+9y=0$ | 2nd order C.F. (repeated roots) | 4 | Easy | Case II, directly mirrors worked example | PDF2 p.28 |
| 10 | Solve the IVP $y''-4y'+13y=0,\ y(0)=2, y'(0)=1$ | 2nd order C.F. (complex roots) | 5 | Medium | Case III, directly mirrors worked example | PDF2 p.37 |
| 11 | A liquid heated to $95^\circ$C is left in a room at $20^\circ$C; after 5 min it cools to $80^\circ$C. Find its temperature after 15 min, and the time to reach $30^\circ$C. | Newton's Law of Cooling | 10 | Medium | Most-repeated application, always 2-part | PDF1 examples + Ex.17–24 |

### 🟠 High Probability

| # | Question | Topic | Marks | Difficulty | Reason | Source |
|---|---|---|---|---|---|---|
| 12 | Write down (do not solve) the trial particular integral for $y''-8y'+16y=3e^{4x}+2x$ | Undetermined coefficients | 3–4 | Medium | Distinctive "guess only" question type explicitly modeled | PDF2 Ex.3 pattern |
| 13 | Find the general solution of $y''-4y'-12y=x e^{4x}$ | Undetermined coeff. (no resonance) | 5 | Medium | Directly mirrors worked example | PDF2 Ex.4 |
| 14 | Solve $y''-5y'+6y=3e^{2x}+x^2$ (resonance case) | Undetermined coeff. (Sum + Modification rule) | 10 | Hard | Combines two rules — tests deeper understanding | Modeled on PDF2 pp.85–87 |
| 15 | Using variation of parameters, solve $y''+y=\csc x$ | Variation of parameters | 10 | Hard | Same technique/difficulty as the fully-worked $\sec x$ IVP example | PDF2 p.68–70 |
| 16 | Define order and degree; find them for $\left(\dfrac{d^2y}{dx^2}\right)^3+5\left(\dfrac{dy}{dx}\right)^2+7y=0$ | Order & Degree | 2 | Easy | Cheap, guaranteed opening question | PDF1 p.6 pattern |
| 17 | Solve the elimination-method system $\dfrac{dx}{dt}+3y=t,\ \dfrac{dy}{dt}-3x=1$ | Simultaneous DE | 7–10 | Hard | Ties directly to 2nd-order auxiliary-equation skill | PDF1 Ex.36–39 pattern |
| 18 | A population grows at a rate proportional to its size. If it doubles in 6 years, find the time to triple. | Growth & Decay | 5 | Medium | 2nd most-repeated application after cooling | PDF1 example, p.144 |

### 🟡 Medium Probability

| # | Question | Topic | Marks | Difficulty | Reason | Source |
|---|---|---|---|---|---|---|
| 19 | A tank has 50 L of brine with 2 kg salt; brine of $0.3$ kg/L enters at 4 L/min and drains at the same rate. Find the salt content at time $t$. | Mixing problem | 7 | Medium | 1 worked example + 2 exercises | PDF1 p.138 |
| 20 | A body attached to a spring executes SHM: $y''+36y=0$, $y(0)=1$, $y'(0)=0$. Find $y(t)$. | 2nd-order application (SHM) | 5 | Medium | Direct mechanical–electrical analogy table given | PDF2 p.93–95 |
| 21 | State (with proof) the superposition principle for a 2nd-order linear homogeneous DE. | Theory / proof | 5 | Medium | Fully proved once in the source; plausible theory Q | PDF2 pp.9–11 |
| 22 | Solve the "unlabelled" equation $(x^2+y^2)dx-2xy\,dy=0$ (identify the method first) | Mixed/miscellaneous | 7 | Hard | Explicit "identify-then-solve" skill drilled 3× in the source | PDF1 Ex.14–16 pattern |
| 23 | An RL circuit has emf $30\sin 10t$, resistance $6\,\Omega$, inductance $0.3\,$H, zero initial current. Find $i(t)$. | RL circuit (1st order) | 7 | Medium | 2 worked examples + 2 exercises | PDF1 p.166–168 |

### ⚪ Low Probability

| # | Question | Topic | Marks | Difficulty | Reason | Source |
|---|---|---|---|---|---|---|
| 24 | An object falls with resistance proportional to velocity; set up and solve for terminal velocity in terms of $m,k,g$. | Falling body / air resistance | 5 | Medium | Only 1 exercise (formula-recall style) beyond 2 examples | PDF1 Ex.33 |
| 25 | Verify that $f(x,y)=x^3y\tan\!\left(\dfrac{x^2+y^2}{x^2-y^2}\right)$ is homogeneous and state its degree. | Homogeneous function (standalone) | 3 | Easy | Normally only a stepping-stone, rarely asked alone | PDF1 p.37 |
| 26 | Solve $m^4+4=0$-type 4th-order DE $y''''+64y=0$ | Case IV (repeated complex pairs) | 5 | Hard | Appears exactly once; unlikely at intro level | PDF2 p.43 |

---

## 4. SAMPLE QUESTION PAPER

**Course/Subject (inferred):** Ordinary Differential Equations — First Order & Second Order Linear Equations (Engineering Mathematics)
**Duration (inferred):** 90 minutes
**Maximum Marks (inferred):** 50

*Instructions: Attempt all questions in Part A and Part B. In Part C, attempt any ONE part (a) or (b) from each question.*

### PART A — Short Answer (2 marks each) — 5 × 2 = 10

**A1.** Define the *order* and *degree* of a differential equation. Hence find the order and degree of
$$\left(\frac{d^2y}{dx^2}\right)^3+5\left(\frac{dy}{dx}\right)^2+7y=0.$$

**A2.** Distinguish between the *general solution* and a *particular solution* of a differential equation, giving one example of each.

**A3.** State the necessary and sufficient condition for $M(x,y)\,dx+N(x,y)\,dy=0$ to be an exact differential equation.

**A4.** Write the standard form of Bernoulli's equation, and state the substitution used to reduce it to a linear differential equation.

**A5.** Write down the auxiliary equation of $\dfrac{d^2y}{dx^2}-5\dfrac{dy}{dx}+6y=0$ and state the nature of its roots.

### PART B — Solve the following (4 marks each) — 5 × 4 = 20

**B1.** Solve: $\dfrac{dy}{dx}=\dfrac{x^2+2}{y^2+3}$

**B2.** Solve: $\dfrac{dy}{dx}=\dfrac{x^2+3xy+y^2}{x^2}$

**B3.** Solve: $\dfrac{dy}{dx}+\dfrac{2}{x}y=x^3$

**B4.** Solve: $\dfrac{dy}{dx}+\dfrac{y}{x}=x^2y^2$

**B5.** Test whether the following equation is exact, and hence solve it:
$$(2xy+3x^2)\,dx+(x^2+2y)\,dy=0$$

### PART C — Long Answer (10 marks each, attempt ONE part from each question) — 2 × 10 = 20

**C1. (a)** A body of mass 1 kg attached to a spring executes simple harmonic motion described by
$$\frac{d^2y}{dt^2}+25y=0,\qquad y(0)=2,\ \ y'(0)=0.$$
Find the displacement $y(t)$, and state its amplitude and angular frequency.

*OR*

**C1. (b)** A metal rod heated to $90^\circ$C is left to cool in a room maintained at $25^\circ$C. After 5 minutes its temperature drops to $70^\circ$C.
(i) Find the temperature of the rod after 10 minutes.
(ii) Find the time taken for the rod to cool to $40^\circ$C.

**C2. (a)** Using the method of variation of parameters, solve:
$$y''+y=\csc x$$

*OR*

**C2. (b)** Using the method of undetermined coefficients, find the general solution of:
$$y''-5y'+6y=3e^{2x}+x^2$$

---

## 5. ANSWER KEY

| Q | Final Answer |
|---|---|
| A1 | Order 2, Degree 3 |
| A2 | General: contains arbitrary constant(s), e.g. $y=Ce^{-x}$; Particular: fixed value of the constant, e.g. $y=e^{-x}$ |
| A3 | $\dfrac{\partial M}{\partial y}=\dfrac{\partial N}{\partial x}$ |
| A4 | $\dfrac{dy}{dx}+Py=Qy^n$; substitution $v=y^{1-n}$ |
| A5 | $m^2-5m+6=0\Rightarrow m=2,3$ (real and distinct) |
| B1 | $\dfrac{y^3}{3}+3y=\dfrac{x^3}{3}+2x+C$ |
| B2 | $\dfrac{x}{x+y}+\ln|x|=C$ |
| B3 | $y=\dfrac{x^4}{6}+\dfrac{C}{x^2}$ |
| B4 | $\dfrac{1}{y}=Cx-\dfrac{x^3}{2}$ |
| B5 | Exact; $x^2y+x^3+y^2=C$ |
| C1(a) | $y(t)=2\cos5t$; amplitude $=2$, $\omega=5\text{ rad/s}$ |
| C1(b) | $T(10)\approx56.2^\circ$C; $t\approx19.9$ min to reach $40^\circ$C |
| C2(a) | $y=c_1\cos x+c_2\sin x-x\cos x+\sin x\ln|\sin x|$ |
| C2(b) | $y=c_1e^{2x}+c_2e^{3x}-3xe^{2x}+\dfrac{x^2}{6}+\dfrac{5x}{18}+\dfrac{19}{108}$ |

---

## 6. DETAILED SOLUTIONS

### Part A

**A1.** The highest derivative is $\dfrac{d^2y}{dx^2}$, so the **order = 2**. The equation is a polynomial in the derivatives (free of radicals/fractions), and the highest-order derivative is raised to the power 3, so the **degree = 3**.

**A2.** A *general solution* contains as many independent arbitrary constants as the order of the DE — e.g. for $\dfrac{dy}{dx}=-y$, the general solution is $y=Ce^{-x}$. A *particular solution* is obtained by assigning a specific value to the constant (usually via an initial condition) — e.g. $y=e^{-x}$ (the case $C=1$).

**A3.** If $M\,dx+N\,dy=0$ is exact, there exists $u(x,y)$ with $du=M\,dx+N\,dy$, so $M=\partial u/\partial x$ and $N=\partial u/\partial y$. Since mixed partials are equal, $\partial M/\partial y=\partial N/\partial x$. This condition is also sufficient (converse proved by constructing $u=\int M\,dx$ and matching against $N$).

**A4.** Standard Bernoulli form: $\dfrac{dy}{dx}+Py=Qy^n$ ($P,Q$ functions of $x$). Substituting $v=y^{1-n}$ converts it to the linear equation $\dfrac{dv}{dx}+(1-n)Pv=(1-n)Q$.

**A5.** Auxiliary equation: $m^2-5m+6=0\Rightarrow (m-2)(m-3)=0\Rightarrow m=2,\,3$. Since the roots are real and distinct (Case I), the general solution would be $y=c_1e^{2x}+c_2e^{3x}$.

### Part B

**B1.** Separate variables:
$$(y^2+3)\,dy=(x^2+2)\,dx$$
Integrating both sides:
$$\frac{y^3}{3}+3y=\frac{x^3}{3}+2x+C$$

**B2.** This is homogeneous (degree 0 after dividing by $x^2$). Put $y=vx$, so $\dfrac{dy}{dx}=v+x\dfrac{dv}{dx}$:
$$v+x\frac{dv}{dx}=\frac{x^2+3vx^2+v^2x^2}{x^2}=1+3v+v^2$$
$$x\frac{dv}{dx}=1+2v+v^2=(1+v)^2$$
Separating variables:
$$\frac{dv}{(1+v)^2}=\frac{dx}{x}\ \Longrightarrow\ -\frac{1}{1+v}=\ln|x|+C_1$$
Substitute $v=y/x$, so $1+v=(x+y)/x$:
$$-\frac{x}{x+y}=\ln|x|+C_1\ \Longrightarrow\ \frac{x}{x+y}=-\ln|x|-C_1$$
Renaming the constant, the general solution is
$$\boxed{\frac{x}{x+y}+\ln|x|=C}$$

**B3.** Linear DE with $P=2/x$, $Q=x^3$. Integrating factor:
$$\text{I.F.}=e^{\int (2/x)\,dx}=e^{2\ln x}=x^2$$
$$\frac{d}{dx}(x^2y)=x^2\cdot x^3=x^5$$
Integrating:
$$x^2y=\frac{x^6}{6}+C\ \Longrightarrow\ y=\frac{x^4}{6}+\frac{C}{x^2}$$

**B4.** Bernoulli's equation with $n=2$. Divide by $y^2$:
$$y^{-2}\frac{dy}{dx}+\frac{1}{x}y^{-1}=x^2$$
Put $v=y^{-1}$, so $\dfrac{dv}{dx}=-y^{-2}\dfrac{dy}{dx}$:
$$-\frac{dv}{dx}+\frac{v}{x}=x^2\ \Longrightarrow\ \frac{dv}{dx}-\frac{v}{x}=-x^2$$
Linear in $v$: I.F. $=e^{-\int dx/x}=e^{-\ln x}=1/x$.
$$\frac{d}{dx}\left(\frac{v}{x}\right)=\frac{-x^2}{x}=-x$$
Integrating:
$$\frac{v}{x}=-\frac{x^2}{2}+C\ \Longrightarrow\ v=Cx-\frac{x^3}{2}$$
Since $v=1/y$:
$$\boxed{\frac{1}{y}=Cx-\frac{x^3}{2}}$$

**B5.** Here $M=2xy+3x^2$, $N=x^2+2y$.
$$\frac{\partial M}{\partial y}=2x,\qquad \frac{\partial N}{\partial x}=2x$$
Since these are equal, the equation **is exact**. Now,
$$\int M\,dx = x^2y+x^3\ (\text{treating }y\text{ as constant}),\qquad \int N\,dy=x^2y+y^2\ (\text{treating }x\text{ as constant})$$
The common term is $x^2y$; combining common + remaining terms:
$$\boxed{x^2y+x^3+y^2=C}$$

### Part C

**C1(a).** Auxiliary equation: $m^2+25=0\Rightarrow m=\pm5i$ (Case III with $\alpha=0,\ \beta=5$). General solution:
$$y=c_1\cos5t+c_2\sin5t$$
Apply $y(0)=2$: $c_1=2$. Differentiate: $y'=-5c_1\sin5t+5c_2\cos5t$. Apply $y'(0)=0$: $5c_2=0\Rightarrow c_2=0$. Hence
$$\boxed{y(t)=2\cos5t}$$
This represents SHM with **amplitude 2** and **angular frequency $\omega=5$ rad/s** (period $=2\pi/5$ s).

**C1(b).** Let $T(t)$ be the rod's temperature, $T_s=25$. By Newton's Law of Cooling, $\dfrac{dT}{dt}=k(T-25)$, giving $T-25=Ce^{kt}$.

At $t=0$: $90-25=65=C$, so $T(t)=25+65e^{kt}$.

At $t=5$: $70-25=45=65e^{5k}\Rightarrow e^{5k}=\dfrac{9}{13}\Rightarrow k=\dfrac{1}{5}\ln\dfrac{9}{13}\approx-0.0735$ per minute.

**(i)** At $t=10$: $e^{10k}=(e^{5k})^2=\left(\dfrac{9}{13}\right)^2\approx0.4793$.
$$T(10)=25+65(0.4793)\approx25+31.16\approx\boxed{56.2^\circ\text{C}}$$

**(ii)** Set $T=40$: $40-25=15=65e^{kt}\Rightarrow e^{kt}=\dfrac{15}{65}=0.2308$.
$$kt=\ln(0.2308)=-1.4663\ \Longrightarrow\ t=\frac{-1.4663}{-0.0735}\approx\boxed{19.9\text{ minutes}}$$

**C2(a).** Auxiliary equation: $m^2+1=0\Rightarrow m=\pm i$. Complementary function: $y_c=c_1\cos x+c_2\sin x$, so $y_1=\cos x,\ y_2=\sin x$.

Wronskian: $W=y_1y_2'-y_2y_1'=\cos^2x+\sin^2x=1$.

Here $Q(x)=\csc x=1/\sin x$.
$$u'=-\frac{y_2Q}{W}=-\sin x\cdot\frac{1}{\sin x}=-1\ \Longrightarrow\ u=-x$$
$$v'=\frac{y_1Q}{W}=\cos x\cdot\frac{1}{\sin x}=\cot x\ \Longrightarrow\ v=\ln|\sin x|$$
Particular integral:
$$y_p=uy_1+vy_2=-x\cos x+\sin x\ln|\sin x|$$
General solution:
$$\boxed{y=c_1\cos x+c_2\sin x-x\cos x+\sin x\ln|\sin x|}$$

**C2(b).** Auxiliary equation: $m^2-5m+6=0\Rightarrow (m-2)(m-3)=0\Rightarrow m=2,3$. So $y_c=c_1e^{2x}+c_2e^{3x}$.

The forcing function has two parts: $3e^{2x}$ and $x^2$.

*Exponential part:* since $m=2$ **is** a root of the auxiliary equation (Modification Rule), the trial term is $Axe^{2x}$ (not $Ae^{2x}$).

*Polynomial part:* since $0$ is **not** a root, the trial term is $Bx^2+Cx+D$ (Sum Rule combines both trial terms into one $y_p$).
$$y_p=Axe^{2x}+Bx^2+Cx+D$$

Differentiating the exponential part twice and substituting into $y_p''-5y_p'+6y_p$ leaves only the coefficient of $e^{2x}$ (the $xe^{2x}$ coefficient cancels automatically, confirming resonance):
$$-Ae^{2x}=3e^{2x}\ \Longrightarrow\ A=-3$$

Substituting the polynomial part into $y_p''-5y_p'+6y_p=x^2$:
$$6Bx^2+(6C-10B)x+(2B-5C+6D)=x^2$$
Comparing coefficients:
$$6B=1\Rightarrow B=\frac{1}{6},\qquad 6C-10B=0\Rightarrow C=\frac{5}{18},\qquad 2B-5C+6D=0\Rightarrow D=\frac{19}{108}$$

Hence $y_p=-3xe^{2x}+\dfrac{x^2}{6}+\dfrac{5x}{18}+\dfrac{19}{108}$, and the general solution is:
$$\boxed{y=c_1e^{2x}+c_2e^{3x}-3xe^{2x}+\frac{x^2}{6}+\frac{5x}{18}+\frac{19}{108}}$$

---

## 7. MOST EXPECTED QUESTIONS

### 🔥 TOP 10 MOST EXPECTED QUESTIONS (for limited-time prep)

1. **Solve a first-order linear DE (general solution or IVP) using the integrating factor.** — The single most-repeated technique in the entire corpus (4 exercise sets, 36 problems).
2. **Test for exactness and solve an exact DE.** — Second most-repeated technique, and the *only* topic with an accompanying proof, making a theory question equally likely.
3. **Solve a homogeneous DE via $y=vx$**, possibly as an IVP. — 22 practice problems across 2 exercise sets; the IVP variant is explicitly favored in the worked examples.
4. **Solve a Bernoulli's equation.** — Third most-repeated first-order technique (24 problems); always reduces to a linear DE in $v=y^{1-n}$.
5. **Solve a 2nd-order homogeneous DE (find C.F.) — likely as an IVP, likely testing at least two of the three root cases across the paper.** — Backed by a single, very dense 15-question exercise block.
6. **Solve a resonance-type undetermined-coefficients problem, or "write down the trial $y_p$" for one.** — The dedicated "guess only" exercise set signals this exact skill is separately examined.
7. **Solve a full variation-of-parameters problem (possibly as an IVP).** — 4 worked examples including one complete IVP; guaranteed at least one long-answer slot.
8. **Solve a Newton's Law of Cooling word problem with 2 sub-parts.** — By far the most-repeated application (2 worked examples + 7 exercises, nearly all with the same two-step structure: find $k$, then answer a follow-up).
9. **Define/identify order and degree of a given DE.** — Cheap, guaranteed opening marks; explicitly drilled with tricky "no degree" cases (radicals/fractions in the derivative).
10. **State and prove a theorem** — either the exactness necessary-and-sufficient condition or the superposition principle for 2nd-order linear DEs. — Both are the *only* fully-proved results in their respective PDFs, making a "state and prove" question a natural higher-mark item.

---

*All numerical constants in Sections 3, 4, and 6 have been changed from the source examples; the underlying techniques, difficulty level, and question phrasing are modeled directly on the two uploaded PDFs. No topic outside the two PDFs has been introduced.*
