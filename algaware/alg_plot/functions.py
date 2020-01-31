# -*- coding: utf-8 -*-
"""
Created on 2019-12-04 10:42

@author: a002028

"""
import datetime
from matplotlib import ticker, dates


#TODO Functions below are meant to be initiated through the import of a yaml-file at startup
# Perhaps this way of work should be extended and therefore this py-file may be divided into multiple py-files depending
# on type of functions..


class MPLDatelocator:
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def __call__(self, ax, locator, args, kwargs):
        """
        :param ax:
        :param locator:
        :param args:
        :param kwargs:
        :return:
        """
        if self.style == 'month':
            self.func = dates.MonthLocator(*args, **kwargs)

        #FIXME hardcoded xlim...
        ax.set_xlim([datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)])
        if self.axis == 'x_axis':
            self.set_x(ax, locator)
        elif self.axis == 'y_axis':
            self.set_y(ax, locator)

    def set_x(self, ax, locator):
        """
        :param ax:
        :param locator:
        :return:
        """
        if locator == 'major_locator':
            ax.xaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.xaxis.set_minor_locator(self.func)

    def set_y(self, ax, locator):
        """
        :param ax:
        :param locator:
        :return:
        """
        if locator == 'major_locator':
            ax.yaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.yaxis.set_minor_locator(self.func)


class MPLDateformatter:
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def __call__(self, ax, formatter, args, kwargs):
        """
        :return:
        """
        if self.style == 'date':
            self.func = dates.DateFormatter(*args, **kwargs)

        if self.axis == 'x_axis':
            self.set_x(ax, formatter)
        elif self.axis == 'y_axis':
            self.set_y(ax, formatter)

    def set_x(self, ax, formatter):
        """
        :param ax:
        :param formatter:
        :return:
        """
        if formatter == 'major_formatter':
            ax.xaxis.set_major_formatter(self.func)

        elif formatter == 'minor_formatter':
            ax.xaxis.set_minor_formatter(self.func)

    def set_y(self, ax, formatter):
        """
        :param ax:
        :param formatter:
        :return:
        """
        if formatter == 'major_formatter':
            ax.yaxis.set_major_formatter(self.func)

        elif formatter == 'minor_formatter':
            ax.yaxis.set_minor_formatter(self.func)


class MPLTickerlocator:
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def __call__(self, ax, locator, args, kwargs):
        """
        :param ax:
        :param locator:
        :param args:
        :param kwargs:
        :return:
        """
        if self.style == 'fixed_ticker':
            self.func = ticker.FixedLocator(*args, **kwargs)

        if self.axis == 'x_axis':
            self.set_x(ax, locator)
        elif self.axis == 'y_axis':
            self.set_y(ax, locator)

    def set_x(self, ax, locator):
        """
        :param ax:
        :param locator:
        :return:
        """
        if locator == 'major_locator':
            ax.xaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.xaxis.set_minor_locator(self.func)

    def set_y(self, ax, locator):
        """
        :param ax:
        :param locator:
        :return:
        """
        if locator == 'major_locator':
            ax.yaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.yaxis.set_minor_locator(self.func)


class MPLAxesInheritance:
    """
    """
    @staticmethod
    def __call__(ax_child, ax_parent, init_keys):
        """
        :param ax_child:
        :param ax_parent:
        :param init_keys:
        :return:
        """
        axis_parent = None
        axis_child = None
        for key in init_keys:
            if key.endswith('axis'):
                axis_parent = getattr(ax_parent, key)
                axis_child = getattr(ax_child, key)
            elif axis_parent:
                get_attr = '_'.join(['get', key])
                set_attr = '_'.join(['set', key])
                attr = getattr(axis_parent, get_attr)
                axis_child.__getattribute__(set_attr)(attr())


class ImplementAxesKwargs:
    """
    """
    @staticmethod
    def __call__(ax, attr, args, kwargs):
        """
        :param ax:
        :param attr:
        :param args:
        :param kwargs:
        :return:
        """
        ax.__getattribute__(attr)(*args, **kwargs)


class ImplementAxisKwargs:
    """
    """
    def __init__(self, *args):
        pass

    @staticmethod
    def __call__(ax, attr, args, kwargs):
        """
        :param ax:
        :param attr:
        :param args:
        :param kwargs:
        :return:
        """
        ax.__getattribute__(attr)(*args, **kwargs)


class AxesLegend:
    """
    """
    @staticmethod
    def __call__(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        legend = ax.legend(*args, **kwargs)
        ax.add_artist(legend)


class FigureLegend:
    """
    """
    @staticmethod
    def __call__(fig, ax_keys, nr_of_handles, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        for key in ax_keys:
            legend_hl = fig.axes[key].ax.get_legend_handles_labels()
            kwargs['handles'] = legend_hl[0]
            kwargs['labels'] = legend_hl[1]
            if len(legend_hl[0]) == nr_of_handles:
                break
        fig.fig.legend(**kwargs)


class FillBetween:
    """
    """
    @staticmethod
    def __call__(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        ax.fill_between(*args, **kwargs)


class BasicPlot:
    """
    """
    @staticmethod
    def __call__(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        ax.plot(*args, **kwargs)


class UpdateAxesLabel:
    """
    """
    @staticmethod
    def __call__(ax, attr, label_input):
        """
        :param ax:
        :param attr:
        :param label_input:
        :return:
        """
        if not label_input:
            return

        if attr == 'set_ylabel':
            label = ax.yaxis.get_label_text()
            label = '\n'.join([label_input, label])
            ax.set_ylabel(label)
        if attr == 'set_xlabel':
            label = ax.xaxis.get_label_text()
            label = '\n'.join([label_input, label])
            ax.set_xlabel(label)
