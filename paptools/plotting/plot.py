from ..core.array import Array
from ..core.number import Number
from ..settings import SETTINGS
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from scipy.optimize import curve_fit
import inspect



class PlotGrid:
    def __init__(self, rows=2, cols=5, plots=[]):
        self.plots = plots
        self.fig, self.axes = plt.subplots(rows, cols)
        self.axes_flat = np.array(self.axes).flatten()

    def add_plot(self, plot):
        self.plots.append(plot)

    def show(self):
        for i, plot_obj in enumerate(self.plots):
            # Assign the grid's axis to the plot object
            plot_obj.ax = self.axes_flat[i]
            plot_obj.render()
            plot_obj.ax.set_title(plot_obj.title)
            
        plt.tight_layout()
        plt.show()

class BasePlot(ABC):
    def __init__(self, title="", style=None):
        self.fig, self.ax = None, None
        self.title = title
        if style is None:
            style = SETTINGS.plotting.general.style
        plt.style.use(style)

    @abstractmethod
    def render(self):
        """Each plot type must implement how it draws itself."""
        pass

    @abstractmethod
    def finalize(self):
        """Each plot type must implement any final adjustments after rendering."""
        pass

    def show(self):
        # If it's not part of a grid, create a new window now
        if self.ax is None:
            self.fig, self.ax = plt.subplots()
            
        self.render()
        self.finalize()
        plt.show()

# Subclass for things like Scatter and Line
class BivariatePlot(BasePlot, ABC):
    def __init__(self, x, y, x_scale, y_scale, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.data_set = [{'x': x, 'y': y}]
        self.x_scale = x_scale
        self.y_scale = y_scale

        self.x_label = str(x._expr) + (f" [{x.get_unit()}]" if x.get_unit() is not None else "")
        self.y_label = str(y._expr) + (f" [{y.get_unit()}]" if y.get_unit() is not None else "")

    def add_series(self, y, x=None):
        if x is None:
            x = self.x
        self.data_set.append({'x': x, 'y': y})

    def finalize(self):
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.legend()
        self.ax.set_title(self.title)
        self.ax.set_xscale(self.x_scale)
        self.ax.set_yscale(self.y_scale)


# Subclass for things like Histograms
class UnivariatePlot(BasePlot, ABC):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data


class LinePlot(BivariatePlot):
    def __init__(self, x, y, x_scale="linear", y_scale="linear", marker=None, line_style=None, label=None, color=None, **kwargs):
        super().__init__(x, y, x_scale, y_scale, **kwargs)
        self.settings = SETTINGS.plotting.line_plot
        self._add_meta_data_to_dataset_entry(marker, line_style, label, color)

    def _add_meta_data_to_dataset_entry(self, marker=None, line_style=None, label=None, color=None, capsize=None, kind="plot"):
        if marker is None:
            if kind == "plot":
                self.data_set[-1]['marker'] = self.settings.plot.default_marker
            elif kind == "regression":
                self.data_set[-1]['marker'] = self.settings.regression.default_marker
            else:
                raise ValueError(f"Unknown kind '{kind}' for meta data.")
        else:
            self.data_set[-1]['marker'] = marker
        
        if line_style is None:
            if kind == "plot":
                self.data_set[-1]['line_style'] = self.settings.plot.default_line_style
            elif kind == "regression":
                self.data_set[-1]['line_style'] = self.settings.regression.default_line_style
            else:
                raise ValueError(f"Unknown kind '{kind}' for meta data.")
        else:
            self.data_set[-1]['line_style'] = line_style
        
        if label is None:
            if kind == "plot":
                self.data_set[-1]['label'] = f"Series {len(self.data_set)}"
            elif kind == "regression":
                self.data_set[-1]['label'] = f"Regression {len(self.data_set)}"
            else:
                raise ValueError(f"Unknown kind '{kind}' for meta data.")
        else:
            self.data_set[-1]['label'] = label
        
        if color is None:
            if kind == "plot":
                self.data_set[-1]['color'] = self.settings.plot.default_color_cycle[(len(self.data_set)-1) % len(self.settings.plot.default_color_cycle)]
            elif kind == "regression":
                self.data_set[-1]['color'] = self.settings.regression.default_color_cycle[(len(self.data_set)-1) % len(self.settings.regression.default_color_cycle)]
            else:                
                raise ValueError(f"Unknown kind '{kind}' for meta data.")
        else:
            self.data_set[-1]['color'] = color

        if capsize is not None:
            self.data_set[-1]['capsize'] = capsize
        else:
            self.data_set[-1]['capsize'] = self.settings.plot.error_bars.cap_size

    def add_series(self, y, x=None, marker=None, line_style=None, label=None, color=None, capsize=None, kind="plot"):
        super().add_series(y, x)
        self._add_meta_data_to_dataset_entry(marker, line_style, label, color, kind=kind)

    def add_regression(self, func, overwrite_param_names = None, index=-1, marker=None, line_style=None, label=None, color=None, show_fit_params_in_label=True):
        x = self.data_set[index]['x']
        y = self.data_set[index]['y']
        x_data = np.array(x._value)
        y_data = np.array(y._value)
        y_error = np.array(y._error) if y._error is not None else None

        popt, pcov = curve_fit(func, x_data, y_data)

       
        if overwrite_param_names is not None:
            names = overwrite_param_names
        else:
            # Extract names from function signature, skipping the first arg (x)
            names = list(inspect.signature(func).parameters.keys())[1:]

        values = popt
        errors = np.sqrt(np.diag(pcov))

        if not label is None:
            label_str = f"{label}"
        else:
            absolute_index = index if index >= 0 else len(self.data_set) + index
            label_str = f"Regression {absolute_index + 1}"

        if show_fit_params_in_label:
            for i in range(len(values)):
                val_err_pair = Number(values[i], errors[i], symbol=names[i], unit="")
                val_err_pair = val_err_pair.round()
                label_str += f"\n {val_err_pair.get_expr()}={str(val_err_pair)}"

        # Genearate x values for the fitted line
        x_fit_val = np.linspace(min(x_data), max(x_data), 100)
        # Generate fitted y values for plotting
        y_fit_val = func(x_fit_val, *popt)

        if color is None and self.settings.regression.use_matching_series_color:
            color = self.data_set[index]['color']

        x_fit = Array(x_fit_val)
        y_fit = Array(y_fit_val)

        self.add_series(y=y_fit, x=x_fit, marker=marker, line_style=line_style, label=label_str, color=color, kind="regression")

        return popt, pcov
        

    def render(self):
        for i, entry in enumerate(self.data_set):
            x_val = entry['x']._value
            y_val = entry['y']._value
            x_err = entry['x']._error
            y_err = entry['y']._error
            self.ax.errorbar(x_val, y_val, xerr=x_err, yerr=y_err, marker=entry['marker'], linestyle=entry['line_style'], label=entry['label'], color=entry['color'], capsize=entry['capsize'])

