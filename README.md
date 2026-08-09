# paptools

> **Write scientific calculations the way you write them on paper.**

`paptools` is a Python library for laboratory work unifying core functionality of `numpy`, `sympy`, and `unyt`. It combines measured values, uncertainties, units and symbolic mathematics into a single object. The library is specifically useful in combination with Jupyter Notebooks. Whether you're calculating the density of a material, the period of a pendulum, or the efficiency of a heat engine, `paptools` takes care of the repetitive work:

* Physical units
* Automatic uncertainty propagation
* Symbolic equations
* LaTeX generation
* Scientific constants

---

## Example

Suppose you've measured the mass and volume of a sample.

```python
from paptools import *

m = Number(26.116, 0.002, symbol="m", unit="g")
V = Number(5.370, 0.005, symbol="V", unit="cm³")

rho = (m / V).round()

rho
```
