# V2 and mean reflectance: theorem, scope, and verification

Date: 2026-11-08. Source definition inspected at commit
`cb566dddca3adeecbd8ac3b8ac352d270d7df585`.

## Ergebnis auf Deutsch

**λ*_V2 ist exakt und umkehrbar mit der ungewichteten mittleren Reflexion über
dasselbe Wellenlängenintervall verknüpft.** Es handelt sich um gleichen
Informationsgehalt nach einer linearen Umrechnung, nicht um die numerische
Gleichheit einer dimensionslosen Reflexion mit einer Wellenlänge. Die Aussage
gilt für jede integrierbare Kurve im Definitionsbereich, nicht nur für getestete
Atlasfarben. Messrauschen widerlegt die Identität nicht. Ein anderer Mittelwert,
ein anderes Intervall oder eine andere Gewichtung wäre eine andere Definition.

## 1. Exact theorem

Let $a<b$, let $R:[a,b]\rightarrow[0,1]$ be integrable, and define

$$
I_0=\int_a^bR(\lambda)\,d\lambda,\quad
m=\frac{I_0}{b-a},\quad
g(x)=\int_a^x(1-R(\lambda))\,d\lambda-\int_x^bR(\lambda)\,d\lambda.
$$

For every $x\in[a,b]$,

$$
\begin{aligned}
g(x)&=\int_a^x1\,d\lambda-\int_a^xR(\lambda)\,d\lambda-\int_x^bR(\lambda)\,d\lambda\\
&=x-a-\int_a^bR(\lambda)\,d\lambda\\
&=x-a-I_0.
\end{aligned}
$$

Thus $g(y)-g(x)=y-x$: $g$ is strictly increasing and continuous even when $R$
has discontinuities. Since $0\leq I_0\leq b-a$, its unique root is

$$
\boxed{\lambda^*_{V2}=a+I_0=a+(b-a)m.}
$$

The inverse is $m=(\lambda^*_{V2}-a)/(b-a)$. Zero reflectance gives $a$ and unit
reflectance gives $b$; endpoint roots are included. Positive area is required
for EE, not V2. Neither a local intersection, monotonicity, smoothness nor a
particular solver is needed for this theorem.

The statement is **unconditional within the explicitly defined domain**. V2 is
not identical to every quantity sometimes called “mean reflectance”.

## 2. Units, weighting, and sampling

| Quantity or operation | Relation to V2 |
|---|---|
| Unweighted integral average on 380–730 nm, R in [0,1] | Exact affine equivalence |
| Percent reflectance $P=100R$ | $V2=380\,\mathrm{nm}+3.5\,\mathrm{nm}\,\overline P$ |
| Arithmetic average of point samples | Not generally the integral average |
| Illuminant/observer-weighted average | Different quantity |
| Another wavelength interval | Another definition |
| Local crossing $R=0.5$ or $R=\sqrt2-1$ | Different quantity; may be absent or multiple |
| Evaluating $R(\lambda^*_{V2})$ | Not generally equal to $m$ |

For a piecewise-linear curve on increasing $w_i$,

$$
I_0=\sum_{i=0}^{n-2}(w_{i+1}-w_i)\frac{R_i+R_{i+1}}2.
$$

This is exact for that interpolation model, not a guarantee that it perfectly
recovers an unknown material curve. For 36 uniform samples over 380–730 nm,

$$
m=\frac{R_0/2+\sum_{i=1}^{34}R_i+R_{35}/2}{35},
$$

which generally differs from $\sum_{i=0}^{35}R_i/36$.
For samples $(380,0),(555,1),(730,0)$ the arithmetic average is $1/3$, but
the area is 175 nm and the integral average is $1/2$. V2 is 555 nm, not
496.667 nm. Also, $R(V2)=1$, not the mean of 0.5.

Subdividing straight segments preserves the integral. Resampling that discards
bends or changing the interpolant can change it. This changes the input
function; it does not refute the theorem.

## 3. Brent and measurement noise

The archived specification prescribes Brent–Dekker. That is a procedural
requirement, retained for claims of Brent procedure conformance. Direct
integration solves exactly the same equation, irrespective of that requirement.

For a perturbation $\epsilon(\lambda)$ with fixed bounds and processing,

$$
\delta\lambda^*_{V2}=\int_a^b\epsilon(\lambda)\,d\lambda=(b-a)\,\delta m.
$$

This is exact, not a first-order approximation. For discrete integration weights
$q$, the V2 variance is $q^T\Sigma q$, where $\Sigma$ is the error covariance
matrix. Expressing V2 as $m$ divides its variance by $(b-a)^2$ and does not
create a new signal-to-noise advantage. Sensitivity and uncertainty must be
compared for the same target in common units. Common offsets do not average
away. Root tolerance, quadrature error, interpolation error and measurement
uncertainty are different things.

Sources: [SciPy brentq](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html),
[NIST TN 1297 Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty).

## 4. Physical interpretation

The equation contains no source spectrum or observer weighting. Its integral
has wavelength units, not radiant-energy units. Using $1-R$ as absorptance
requires compatible energy accounting, negligible transmission and the relevant
reflection collection geometry. A reflectance-factor or fluorescent measurement
cannot automatically be substituted into an opaque, non-luminescent energy
partition. These qualifications do not alter the mathematical identity.

If a positive source weighting $E(\lambda)$ were inserted in both integrals,

$$
g_E(x)=\int_a^xE(\lambda)\,d\lambda-\int_a^bE(\lambda)R(\lambda)\,d\lambda.
$$

Its root would require inversion of the cumulative integral of $E$ and is not
generally $a+(b-a)m$. This is a different definition, not a counterexample.
Changing from wavelength to frequency without transforming the measure also
changes the descriptor.

Sources: [IUPAC reflectance](https://goldbook.iupac.org/terms/view/R05235),
[IUPAC spectroscopy glossary, §§112,146](https://doi.org/10.1515/pac-2019-0203).

## 5. Δλ* and the seven fields

Let $c=\int\lambda R/\int R$. For the current sign,

$$
D=\Delta\lambda^*=a+(b-a)m-c.
$$

With $t=(\lambda-a)/(b-a)$ and $M_k=\int_0^1t^kR(a+(b-a)t)\,dt$,

$$
\frac{D}{b-a}=M_0-\frac{M_1}{M_0},\qquad M_0>0.
$$

This dimensionless form identifies the combination searched for in the novelty
review. It remains tied to the chosen interval and reflectance scale.

| Synthetic spectrum | Mean | V2 (nm) | EE (nm) | D (nm) |
|---|---:|---:|---:|---:|
| Constant 0.2 | 0.2 | 450 | 555 | −105 |
| Constant 0.3 | 0.3 | 485 | 555 | −70 |
| Linear 0.12 → 0.48 | 0.3 | 485 | 590 | −105 |

The first two rows prove that EE alone does not determine D. The first and
third prove that D alone does not determine EE. Together, mean and EE determine
D exactly. A constant positive curve has a symmetric normalized distribution
and zero third central moment, yet generally nonzero D. D is therefore **not a
pure asymmetry/skewness measure**.

The four quantities $(m,c,\mu_2,\mu_3)$ determine all seven fields. Conversely,
V2, EE, μ₂ and μ₃ recover these four. Redundant fields can aid interpretation
or a restricted model but do not add independent information.

Even all seven do not identify a spectrum uniquely. On $t\in[0,1]$ take
$R_0(t)=0.5$ and $R_1(t)=0.5+0.2P_4(2t-1)$, where
$P_4(x)=(35x^4-30x^2+3)/8$. Orthogonality gives equal raw moments of orders
0–3 and hence equal seven fields although the curves differ. Both remain in
[0,1]. This rules out universal spectrum/material identification from the
seven values, without making a claim about a specific classifier's accuracy.

## 6. Reproduce the verification

The [script](../../scripts/verify_v2_identity.py) uses two numerical paths:

1. Brent on the original two integrals, using adaptive quadrature with every
   piecewise-linear breakpoint supplied.
2. Independent NumPy trapezoidal evaluation of the full area.

Fixed seed 20261108; 544 synthetic cases: 20 constants, 8 ramps, 4 oscillating
curves, 384 random curves and 128 bounded perturbations. Grids: 1, 5, 10 nm and
irregular. No clipping, material dataset or master field is used.

Maximum root difference: **2.2737367544323206e-13 nm**. Maximum residual in the
original balance equation: **4.831690603168681e-13 nm**. Comparison tolerance:
1e-8 nm. These are numerical differences, not instrument precision.

The 28-test suite includes the unchanged historical threshold test. New tests
have analytic expectations and negative examples: sample versus integral mean,
local versus global balance, weighted versus unweighted balance, zero area,
discontinuity, irregular grids and invalid inputs. The proof, not the finite
case count, establishes the general result.

```bash
python -m pip install -r requirements-audit.txt
python -m pytest -q
python scripts/verify_v2_identity.py --output /tmp/v2_identity.json
```

The [recorded JSON](../../results/v2_identity_2026-11-08.json) includes versions,
tolerances and the script SHA-256. Separate numerical paths are internal checks,
not external laboratory replication or scientific peer review.

## 7. Scientific consequence

The identity is settled for this definition. V2 is an affine encoding of mean
reflectance, not an additional independent physical observable. Its usefulness
as a coordinate, and the utility of D, can be studied separately. Neither this
proof nor a GitHub publication establishes historical priority, improved
metamerism prediction, fraud detection, aging detection or industrial acceptance.
