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

    def add_linear_regression(self, overwrite_param_names = None, index=-1, marker=None, line_style=None, label=None, color=None, show_fit_params_in_label=True, x_range=None):
        x_unit = self.data_set[index]['x'].get_unit()
        y_unit = self.data_set[index]['y'].get_unit()
        def linear_func(x, a, b):
            return a * x + b
        
        popt, pcov = self.add_regression(linear_func, overwrite_param_names=overwrite_param_names, index=index, marker=marker, line_style=line_style, label=label, color=color, show_fit_params_in_label=show_fit_params_in_label, x_range=x_range)

        a = popt[0]
        b = popt[1]
        var_a = pcov[0, 0]  # Varianz von a
        var_b = pcov[1, 1]  # Varianz von b
        cov_ab = pcov[0, 1] # Kovarianz von a und b

        # Calculate x-axis intercept and its error
        if x_unit is not None:
            x_unit_str = f" {x_unit}"
        else:
            x_unit_str = ""

        if y_unit is not None:
            y_unit_str = f" {y_unit}"
        else:               
            y_unit_str = ""

        # Exakte Fehlerberechnung für x_intercept = -b/a
        x_int_val = -b / a
        # Formel nach Gauß mit Korrelationsterm
        x_int_err = np.sqrt(
            ( (1/a)**2 * var_b ) + 
            ( (b/a**2)**2 * var_a ) - 
            ( 2 * (b/a**3) * cov_ab )
        )

        # Jetzt erst das Number-Objekt erstellen
        x_intercept = Number(x_int_val, x_int_err, symbol=r'x_{intercept}', unit=x_unit_str)
        return popt, pcov, x_intercept, Number(b, np.sqrt(var_b), symbol='b', unit=y_unit_str)

    def add_gaussian_regression(self, overwrite_param_names = None, index=-1, marker=None, line_style=None, label=None, color=None, show_fit_params_in_label=True, x_range=None, enable_y_offset=False):
        A_guess = max(self.data_set[index]['y']._value)
        mu_guess = self.data_set[index]['x']._value[np.argmax(self.data_set[index]['y']._value)]
        sigma_guess = (max(self.data_set[index]['x']._value) - min(self.data_set[index]['x']._value)) / 4
        p0 = [A_guess, mu_guess, sigma_guess]
        if enable_y_offset:
            def gaussian_func(x, A, mu, sigma, d):
                return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + d
            p0.append(min(self.data_set[index]['y']._value))
        else:
            def gaussian_func(x, A, mu, sigma):
                return A * np.exp(-(x - mu)**2 / (2 * sigma**2))
        popt, pcov = self.add_regression(gaussian_func, overwrite_param_names=overwrite_param_names, index=index, marker=marker, line_style=line_style, label=label, color=color, show_fit_params_in_label=show_fit_params_in_label, x_range=x_range, p0=p0)
        return popt, pcov

    def add_regression(self, func, overwrite_param_names = None, index=-1, marker=None, line_style=None, label=None, color=None, show_fit_params_in_label=True, x_range=None, p0=None):
        x = self.data_set[index]['x']
        y = self.data_set[index]['y']
        x_data = np.array(x._value)
        y_data = np.array(y._value)
        y_error = np.array(y._error) if y._error is not None else None

        if y_error is None:
            if p0 is None:
                popt, pcov = curve_fit(func, x_data, y_data)
            else:
                popt, pcov = curve_fit(func, x_data, y_data, p0=p0)
        else:
            if p0 is None:
                popt, pcov = curve_fit(func, x_data, y_data, sigma=y_error, absolute_sigma=True) 
            else:
                popt, pcov = curve_fit(func, x_data, y_data, sigma=y_error, absolute_sigma=True, p0=p0)

       
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
        if x_range is None:
            x_fit_val = np.linspace(min(x_data), max(x_data), 100)
        else:
            x_fit_val = np.linspace(x_range[0], x_range[1], 100)
        # Generate fitted y values for plotting
        y_fit_val = func(x_fit_val, *popt)

        if color is None and self.settings.regression.use_matching_series_color:
            color = self.data_set[index]['color']

        x_fit = Array(x_fit_val)
        y_fit = Array(y_fit_val)

        self.add_series(y=y_fit, x=x_fit, marker=marker, line_style=line_style, label=label_str, color=color, kind="regression")

        return popt, pcov
        
    def add_vertical_line(self, x, color='red', label='', line_style='--'):
        self.ax.axvline(x=x, color=color, linestyle=line_style, label=label)

    def render(self):
        for i, entry in enumerate(self.data_set):
            x_val = entry['x']._value
            y_val = entry['y']._value
            x_err = entry['x']._error
            y_err = entry['y']._error
            self.ax.errorbar(x_val, y_val, xerr=x_err, yerr=y_err, marker=entry['marker'], linestyle=entry['line_style'], label=entry['label'], color=entry['color'], capsize=entry['capsize'])

