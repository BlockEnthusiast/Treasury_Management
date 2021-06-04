import matplotlib.pyplot as plt
import numpy as np


class Plotter():
    def __init__(self):
        self.plt = plt
        self.fig = self.plt.figure(figsize=(10,10))
        self.current_plot = None
        self.current_plot_index = 111
        self.subplots = []
        # self.plt.legend()
        self.fig.subplots_adjust(hspace=.5,wspace=0.5)

    def iterate_plot(self):
        new_plot = self.fig.add_subplot(self.current_plot_index)
        self.current_plot_index += 1
        self.subplots.append(new_plot)


    def plot(self, _x, _y, _extras):
        self.subplots[-1].plot(_x, _y,
                    label       = self.raw_input(_extras, 'label'),
                    color       = self.raw_input(_extras, 'color'),
                    linestyle   = self.raw_input(_extras, 'linestyle'),
                    linewidth   = self.raw_input(_extras, 'linewidth'),
                    marker      = self.raw_input(_extras, 'marker'),
                    markerfacecolor = self.raw_input(_extras, 'markerfacecolor'),
                    markersize  = self.raw_input(_extras, 'markersize'),
                    )

    def set_axis(self, _x_label, _y_label):
        self.subplots[-1].set_xlabel(_x_label)
        self.subplots[-1].set_ylabel(_y_label)

    def set_title(self, _title):
        self.subplots[-1].set_title(_title)

    def set_limits(self, _x_min, _x_max, _y_min, _y_max):
        self.subplots[-1].set_ylim([_y_min, _y_max])
        self.subplots[-1].set_xlim([_x_min, _x_max])

    def raw_input(self, a, b):
        if b in a:
            return a[b]
        else:
            return None

    def show(self):
        self.plt.legend()
        self.plt.show()
