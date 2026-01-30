from paptools.plotting.plot import LinePlot, PlotGrid
from paptools.core.array import Array
import numpy as np
import random


x = np.linspace(0, 17, 19)
x_error = 0.2 + 0.2 * np.sqrt(x)

y = np.cos(x) + np.random.normal(0, 0.1, size=x.shape)
y_error = 0.2 + 0.2 * np.sqrt(np.abs(y))

x_arr = Array(x, x_error, unit="s", symbol="t")
y_arr = Array(y, y_error, unit="m/s", symbol="v")

def sin_func(x, a, b, c):
    return a * np.sin(b * x + c)

plot = LinePlot(x_arr, y_arr, label="Measured Data")
plot.add_regression(sin_func, label="Fitted Sine Function", show_fit_params_in_label=True)

plot.show()
