# -*- coding: utf-8 -*-
"""
Created on 2019-12-04 10:42

@author: a002028

"""
import datetime
import matplotlib as mpl


#TODO Functions below are meant to be initiated through the import of a yaml-file at startup
# Perhaps this way of work should be extended and therefore this py-file may be divided into multiple py-files depending
# on type of functions..


class MPLDatelocator(object):
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def run(self, ax, locator, args, kwargs):
        """
        :return:
        """
        if self.style == 'month':
            self.func = mpl.dates.MonthLocator(*args, **kwargs)

        #FIXME hardcoded xlim...
        ax.set_xlim([datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)])
        if self.axis == 'x_axis':
            self.set_x(ax, locator)
        elif self.axis == 'y_axis':
            self.set_y(ax, locator)

    def set_x(self, ax, locator):
        """
        :param func:
        :return:
        """
        if locator == 'major_locator':
            ax.xaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.xaxis.set_minor_locator(self.func)

    def set_y(self, ax, locator):
        """
        :param func:
        :return:
        """
        if locator == 'major_locator':
            ax.yaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.yaxis.set_minor_locator(self.func)


class MPLDateformatter(object):
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def run(self, ax, formatter, args, kwargs):
        """
        :return:
        """
        if self.style == 'date':
            self.func = mpl.dates.DateFormatter(*args, **kwargs)

        if self.axis == 'x_axis':
            self.set_x(ax, formatter)
        elif self.axis == 'y_axis':
            self.set_y(ax, formatter)

    def set_x(self, ax, formatter):
        """
        :param func:
        :return:
        """
        if formatter == 'major_formatter':
            ax.xaxis.set_major_formatter(self.func)

        elif formatter == 'minor_formatter':
            ax.xaxis.set_minor_formatter(self.func)

    def set_y(self, ax, formatter):
        """
        :param func:
        :return:
        """
        if formatter == 'major_formatter':
            ax.yaxis.set_major_formatter(self.func)

        elif formatter == 'minor_formatter':
            ax.yaxis.set_minor_formatter(self.func)


class MPLTickerlocator(object):
    """
    """
    def __init__(self, axis, style):
        self.func = None
        self.axis = axis
        self.style = style

    def run(self, ax, locator, args, kwargs):
        """
        :return:
        """
        if self.style == 'fixed_ticker':
            self.func = mpl.ticker.FixedLocator(*args, **kwargs)

        if self.axis == 'x_axis':
            self.set_x(ax, locator)
        elif self.axis == 'y_axis':
            self.set_y(ax, locator)

    def set_x(self, ax, locator):
        """
        :param func:
        :return:
        """
        if locator == 'major_locator':
            ax.xaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.xaxis.set_minor_locator(self.func)

    def set_y(self, ax, locator):
        """
        :param func:
        :return:
        """
        if locator == 'major_locator':
            ax.yaxis.set_major_locator(self.func)

        elif locator == 'minor_locator':
            ax.yaxis.set_minor_locator(self.func)


class MPLAxesInheritance(object):
    """
    """
    @staticmethod
    def run(ax_child, ax_parent, init_keys):
        """
        :return:
        """
        axis_parent = None
        for key in init_keys:
            if key.endswith('axis'):
                axis_parent = getattr(ax_parent, key)
                axis_child = getattr(ax_child, key)
            elif axis_parent:
                get_attr = '_'.join(['get', key])
                set_attr = '_'.join(['set', key])
                attr = getattr(axis_parent, get_attr)
                axis_child.__getattribute__(set_attr)(attr())


class ImplementAxesKwargs(object):
    """
    """
    @staticmethod
    def run(ax, attr, args, kwargs):
        """
        :param ax:
        :param attr:
        :param args:
        :param kwargs:
        :return:
        """
        ax.__getattribute__(attr)(*args, **kwargs)


class ImplementAxisKwargs(object):
    """
    """
    def __init__(self, dummy, dummy2):
        pass

    @staticmethod
    def run(ax, attr, args, kwargs):
        """
        :param ax:
        :param attr:
        :param args:
        :param kwargs:
        :return:
        """
        ax.__getattribute__(attr)(*args, **kwargs)


class AxesLegend(object):
    """
    """
    @staticmethod
    def run(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        legend = ax.legend(*args, **kwargs)
        ax.add_artist(legend)


class FillBetween(object):
    """
    """
    @staticmethod
    def run(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        ax.fill_between(*args, **kwargs)


class BasicPlot(object):
    """
    """
    @staticmethod
    def run(ax, args, kwargs):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        ax.plot(*args, **kwargs)


class UpdateAxesLabel(object):
    """
    """
    @staticmethod
    def run(ax, attr, input):
        """
        :param ax:
        :param args:
        :param kwargs:
        :return:
        """
        if not input:
            return

        if attr == 'set_ylabel':
            label = ax.yaxis.get_label_text()
            label = '\n'.join([input, label])
            ax.set_ylabel(label)
        if attr == 'set_xlabel':
            label = ax.xaxis.get_label_text()
            label = '\n'.join([input, label])
            ax.set_xlabel(label)
