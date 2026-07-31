# paptools

> **Scientific computing with uncertainties, units, symbolic mathematics, and statistics—all in one coherent API.**

`paptools` is a Python library for scientific computing, laboratory data analysis, and engineering calculations. It combines numerical computation, symbolic mathematics, automatic uncertainty propagation, physical units, statistical analysis, and scientific utilities into a single, consistent interface.

Instead of combining several independent libraries and manually converting between data types, `paptools` allows you to work with values, uncertainties, units, and symbolic expressions as first-class objects throughout your calculations.

Built on top of the excellent scientific Python ecosystem—including **SymPy**, **NumPy**, and **unyt**—`paptools` provides a higher-level API designed for students, researchers, educators, and engineers.

---

## Why paptools?

Scientific calculations rarely involve plain numbers.

Real-world measurements have

* uncertainties,
* physical units,
* symbolic relationships,
* statistical significance,
* derived quantities,
* and mathematical transformations.

Managing these aspects separately often leads to verbose code, duplicated logic, and subtle mistakes.

`paptools` keeps everything together.

A single object can represent

* a numerical value,
* its uncertainty,
* its physical unit,
* and, when appropriate, its symbolic representation.

This enables calculations that remain readable while automatically preserving the information needed for proper scientific analysis.

---

## Features

### 📐 Automatic uncertainty propagation

Perform calculations while uncertainties are propagated automatically according to Gaussian error propagation.

```python
from paptools import Number

length = Number(2.51, uncertainty=0.03)
width = Number(1.20, uncertainty=0.02)

area = length * width

print(area)
```

---

### 📏 Physical units

Work with quantities that carry units throughout calculations.

```python
from paptools import Number

distance = Number(12, unit="m")
time = Number(3, unit="s")

velocity = distance / time
```

---

### ∑ Symbolic mathematics

Create symbolic expressions and evaluate or manipulate them using the power of SymPy.

```python
from paptools import Symbol

x = Symbol("x")

expression = x**2 + 2*x + 1
```

---

### 📊 Statistics

Includes utilities for common statistical analysis, significance testing, and experimental data evaluation.

---

### 🔢 Mathematical functions

Most mathematical functions seamlessly support plain numbers, symbolic expressions, and `paptools` objects.

```python
from paptools import sin

result = sin(angle)
```

---

### ⚛ Physical and mathematical constants

Frequently used scientific constants are included and ready to use.

```python
from paptools.constants import c, h
```

---

## Installation

Install the latest release from PyPI.

```bash
pip install paptools
```

Or install the newest development version directly from GitHub.

```bash
git clone https://github.com/jmueller209/paptools.git

cd paptools

pip install -e .
```

---

## A Quick Example

```python
from paptools import Number, sqrt

mass = Number(2.35, uncertainty=0.02, unit="kg")
volume = Number(0.84, uncertainty=0.01, unit="m^3")

density = mass / volume

print(density)
```

Measurements, uncertainties, and units remain attached to the result automatically, reducing boilerplate code and helping prevent common mistakes.

---

## Who is paptools for?

`paptools` is designed for anyone performing scientific or technical calculations, including

* students in laboratory courses,
* physics, chemistry, and engineering education,
* researchers,
* data analysis workflows,
* scientific scripting,
* reproducible computational notebooks,
* symbolic derivations,
* uncertainty analysis.

---

## Philosophy

The design of `paptools` is guided by a few simple principles.

### Expressive

Scientific code should resemble the equations found in textbooks.

### Correct

Units and uncertainties should not be an afterthought.

### Consistent

The same objects should work naturally across arithmetic, symbolic manipulation, statistics, and mathematical functions.

### Pythonic

`paptools` builds upon the existing scientific Python ecosystem instead of replacing it.

---

## Documentation

The documentation is organized into several sections.

* **Getting Started** – installation and first calculations
* **User Guide** – core concepts and workflows
* **API Reference** – complete documentation of all public classes and functions
* **Mathematical Functions** – reference for wrapped mathematical functions
* **Constants** – physical and mathematical constants
* **Cookbook** – practical scientific examples
* **Examples** – runnable scripts demonstrating common workflows

---

## Project Structure

```text
paptools/
├── core/
├── math/
├── constants/
├── statistics/
├── settings/
└── ...
```

---

## Examples

The `examples/` directory contains complete runnable examples covering

* uncertainty propagation,
* symbolic mathematics,
* unit-aware calculations,
* statistical analysis,
* physics problems,
* laboratory data analysis,
* engineering calculations.

---

## Contributing

Contributions of all kinds are welcome.

Bug reports, feature requests, documentation improvements, examples, and pull requests help make the project better for everyone.

---

## License

`paptools` is released under the MIT License.

See the `LICENSE` file for details.
