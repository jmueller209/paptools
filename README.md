# paptools

> **Write scientific calculations the way you write them on paper.**

`paptools` is a Python library for laboratory work unifying core functionality of `numpy`, `sympy`, and `unyt`. It combines measured values, uncertainties, units and symbolic mathematics into a single object. The library is specifically useful in combination with Jupyter Notebooks. Whether you're calculating the density of a material, the period of a pendulum, or the efficiency of a heat engine, `paptools` takes care of the repetitive work:

* Physical units
* Automatic uncertainty propagation
* Symbolic equations
* LaTeX generation
* Scientific constants

---

## A first calculation

Suppose you've measured the mass and volume of a sample.

```python
from paptools import *

m = Number(26.116, 0.002, symbol="m", unit="g")
V = Number(5.370, 0.005, symbol="V", unit="cm³")

rho = (m / V).round()

rho
```

Output

```text
ρ = (4.863 ± 0.005) g/cm³
```
Note that the `round()` method automatically rounds the error according to the convention where we keep the first significant digit if it is greater than or equal to 3 and keep the first two significant digits if the first significant digit is a 1 or 2. The value gets than rounded to the same accuracy.

But there is much more hidden inside the result.

---

## Inspect the equation

```python
rho.get_expr()
```

```text
m / V
```

---

## Inspect the propagated uncertainty

```python
rho.get_err_expr()
```

```text
√((∂ρ/∂m Δm)² + (∂ρ/∂V ΔV)²)
```

---

## Generate LaTeX for your report

```python
import sympy as sp

sp.latex(rho.get_expr())
```

```latex
\frac{m}{V}
```

and

```python
sp.latex(rho.get_err_expr())
```

produces the complete Gaussian error propagation formula.

No manual derivation required.

---

# Why paptools?

Most scientific calculations involve much more than numbers.

Every measured quantity has

* a value,
* an uncertainty,
* a unit,
* and often a symbolic meaning.

Traditional scientific code tends to split these concepts across several libraries. `paptools` keeps them together, allowing you to focus on the calculation instead of bookkeeping.

---

# Core ideas

Everything revolves around just two data types.

## `Number`

Represents a single measured quantity.

```python
length = Number(
    12.54,
    0.03,
    symbol="l",
    unit="cm"
)
```

A `Number` can store

* the numerical value,
* its uncertainty,
* a physical unit,
* an optional symbolic variable.

---

## `Array`

Represents a collection of measured values.

```python
times = Array(
    [4.51, 4.48, 4.52, 4.50],
    uncertainty=0.01,
    symbol="t",
    unit="s"
)
```

Arrays support element-wise operations, statistics and uncertainty-aware calculations.

---

# Designed for laboratory work

A typical workflow looks like this:

```text
Measurements
        │
        ▼
Create Number / Array objects
        │
        ▼
Perform calculations
        │
        ├── numerical result
        ├── propagated uncertainty
        ├── unit conversion
        ├── symbolic expression
        └── LaTeX output
```

---

# Learn by doing

The documentation is organised around complete workflows rather than individual modules.

* **Your First Experiment** — from raw measurements to a final result.
* **Working with Measurements** — creating `Number` and `Array` objects.
* **Units** — conversions and dimensional consistency.
* **Automatic Error Propagation** — how uncertainties are handled.
* **Symbolic Equations** — inspecting and exporting expressions.
* **Cookbook** — complete examples from real laboratory experiments.
* **API Reference** — detailed documentation of every public class and function.

Most users should only need the first two guides before becoming productive.

---

# Installation

```bash
pip install paptools
```

---

# Philosophy

`paptools` grew out of countless undergraduate physics laboratory reports.

Its goal is simple:

> Spend your time thinking about the experiment—not propagating uncertainties, converting units, or rewriting equations into LaTeX.
