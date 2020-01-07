# -*- coding: utf-8 -*-
"""
Created on 2019-12-02 16:04

@author: a002028

"""
import seaborn as sns
sns.set_style("ticks", {'axes.grid': True, 'grid.linestyle': '--'})
# sns.set_style("whitegrid")
# sns.set_style("darkgrid")
# sns.set_style("dark")
# sns.set_context("talk")
sns.set_context("paper", rc={"grid.linewidth": 0.5})
import matplotlib.pyplot as plt
from threading import Thread
import copy
import utils


def thread_process(call_function, *args, **kwargs):
    """
    :param call_function:
    :param args:
    :param kwargs:
    :return:
    """
    Thread(target=call_function, args=args, kwargs=kwargs).start()


class FigureBase(object):
    """
    """
    def __init__(self):
        super().__init__()
        self._figure = None
        self._figure_name = None

    def get_session_figure_settings(self, figure_key):
        """
        :param figure_key:
        :return:
        """
        return self.setup.get(figure_key)

    @property
    def axes_setup(self):
        return self.figure.get('axes')

    @property
    def figure_setup(self):
        return self.figure.get('setup')

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, name):
        self._figure = self.settings['figures'].get(name)

    @property
    def figure_name(self):
        return self._figure_name

    @figure_name.setter
    def figure_name(self, name):
        self._figure_name = name.replace(' ', '_')

    @property
    def default_plot_settings(self):
        return self.settings['default_plot_settings']

# class Figure():
#     """
#
#     """
#     @property
#     def _constructor(self):
#         """
#         Constructor for Figure
#         :return: Figure
#         """
#         return Figure


class Axes(object):
    """
    """
    def __init__(self, settings=None, figure_axes=None, figure_grid=None, functions=None):
        for item, value in settings.items():
            setattr(self, item, value)
        self.figure_grid = figure_grid
        self.figure_axes = figure_axes
        self.functions = functions
        self._data_key = None

        parent_ax = self.figure_axes.get(self.x_axis.get('share_with'))
        if parent_ax:
            parent_ax = parent_ax.ax

        self.ax = plt.subplot2grid(self.figure_grid,
                                   (self.row_pos, self.col_pos),
                                   rowspan=self.row_span,
                                   colspan=self.col_span,
                                   sharex=parent_ax,
                                   sharey=parent_ax)
        self._axes_settings()

    def get(self, attr):
        """
        :param attr:
        :return:
        """
        if hasattr(self, attr):
            return self.__getattribute__(attr)
        else:
            return None

    def _axes_settings(self):
        """
        :param ax:
        :param ax_setting:
        :return:
        """
        if self.x_axis.get('share_with'):
            thread_process(self._que_sharex, *(self.ax, self.x_axis))
        # elif self.x_axis.get('parent'):
        #     self._set_axis_properties(axis='x_axis')
        self._set_axis_properties(axis='x_axis')

        if self.y_axis.get('share_with'):
            thread_process(self._que_sharey, *(self.ax, self.y_axis))
        # elif self.y_axis.get('parent'):
        #     self._set_axis_properties(axis='y_axis')
        self._set_axis_properties(axis='y_axis')

        if self.get('axes_setting'):
            self._set_axes_settings(ax_setting=self.get('axes_setting'))

    def _set_axes_settings(self, ax_setting=None):
        """
        :param ax:
        :param ax_setting:
        :return:
        """
        for item, value in ax_setting.items():
            if isinstance(value, dict):
                if 'function' in value:
                    func = self.functions.get(value.get('function'))
                    func.run(self.ax, item, value['args'], value['kwargs'])

    def _set_axis_properties(self, axis=None):
        """
        :param ax:
        :param ax_setting:
        :return:
        """
        for item, value in getattr(self, axis).items():
            if isinstance(value, dict):
                print(item, value)
                if 'function' in value:
                    func = self.functions.get(value.get('function'))(axis, value['style'])
                    func.run(self.ax, item, value['args'], value['kwargs'])

    def _que_sharex(self, ax, axes_prop):
        """
        A figure might contain multiple subplots that are created at different time. We therefore need to set up a que
        that tells a specific axes to wait until the desired "parent" axes have been created and is ready to
        share axes specifications
        :return:
        """
        finished = False
        while not finished:
            if axes_prop.get('share_with') in self.figure_axes:
                ax.xaxis.set_tick_params(which='both', labelbottom=False)
                if axes_prop.get('invisible_major'):
                    ax.xaxis.set_major_formatter(plt.NullFormatter())

                """
                Example on inheritor input from plot_setup.yaml
                (Not used in recent version of algaware plot-function)
                x_axis:
                        share_with: '7'
                        inheritor:
                            init_keys:
                            - xaxis
                            - major_locator
                            - minor_locator
                            function: axes_inheritor
                """
                # parent = self.axes[axes_prop.get('share_with')]
                # ax.get_shared_x_axes().join(ax, parent)
                # ax.set_xticklabels([])
                # if axes_prop.get('inheritor'):
                #     func = self.setup['function_types'].get(axes_prop['inheritor'].get('function'))()
                #     func.run(ax, parent, axes_prop['inheritor'].get('init_keys'))
                finished = True

    def _que_sharey(self, ax, axes_prop):
        """
        A figure might contain multiple subplots that are created at different time. We therefore need to set up a que
        that tells a specific axes to wait until the desired "parent" axes have been created and is ready to
        share axes specifications
        :return:
        """
        finished = False
        while not finished:
            if axes_prop.get('share_with') in self.figure_axes:
                ax.yaxis.set_tick_params(which='both', labelbottom=True)
                # parent = self.axes[axes_prop.get('share_with')]
                # ax.get_shared_y_axes().join(ax, parent)
                # ax.set_yticklabels([])
                # if axes_prop.get('inheritor'):
                #     func = self.setup['function_types'].get(axes_prop['inheritor'].get('function'))()
                #     func.run(ax, parent, axes_prop['inheritor'].get('init_keys'))
                finished = True

    @property
    def data_key(self):
        return self._data_key

    @data_key.setter
    def data_key(self, key):
        self._data_key = key


class FigureSetup(FigureBase):
    """
    """
    def __init__(self, setup=None):
        super().__init__()
        self.setup = setup
        self.fig = None
        self.axes = {}
        self.main_axes_properties = {}
        self.settings = self.get_session_figure_settings('algaware')

    def set_figure_settings(self, figure_name):
        """
        :param figure_name:
        :return:
        """
        self.figure_name = figure_name
        self.figure = figure_name

    def refresh_mpl_figure(self):
        """
        :return:
        """
        self.fig = plt.figure(figsize=self.figure_setup.get('size'))

    def refresh_axes(self):
        """
        :return:
        """
        self.axes = {}
        for key, ax_settings in self.axes_setup.items():
            self.axes[key] = Axes(settings=ax_settings,
                                  figure_axes=self.axes,
                                  figure_grid=self.figure_setup.get('subplot_grid'),
                                  functions=self.setup['function_types'])

    def save(self, dpi=300):
        """
        :param dpi:
        :return:
        """
        plt.tight_layout()
        save_name = self.figure_name + '.png'
        plt.savefig(save_name, dpi=dpi)


class PlotAlgaware(object):
    """
    """
    def __init__(self, figure_setup=None, data=None, station_key_map=None):
        self.fig = figure_setup
        self.data = data
        self.station_key_map = station_key_map

        self.default_plot_settings = self.fig.settings.get('default_plot_settings')

    def get(self, attr):
        """
        :param attr:
        :return:
        """
        if hasattr(self, attr):
            return self.__getattribute__(attr)
        else:
            return None

    def plot(self):
        """
        :return:
        """
        for ax_key in self.fig.axes.keys():
            station = self.fig.axes[ax_key].get('statn_nom')
            data_key = self.station_key_map.get(station)
            self.fig.axes[ax_key].data_key = data_key
            if self.fig.axes[ax_key].get('plot'):
                for key, item in self.fig.axes[ax_key].get('plot').items():
                    plot_setting = self.default_plot_settings.get(key)
                    if 'function' in plot_setting:
                        func = self.fig.axes[ax_key].functions.get(plot_setting.get('function'))()
                        if data_key:
                            if isinstance(data_key, str):
                                kwargs = self.get_data_kwargs(plot_setting.get('kwargs'), item)
                                self.func_plot(data_key, ax_key, item, func, kwargs)
                            else:
                                for i, d_key in enumerate(data_key):
                                    if i == 1:
                                        if not item.get('secondary'):
                                            continue
                                        else:
                                            kwargs = self.get_data_kwargs(plot_setting.get('kwargs'), item, secondary=True)
                                    else:
                                        kwargs = self.get_data_kwargs(plot_setting.get('kwargs'), item)
                                    self.func_plot(d_key, ax_key, item, func, kwargs)

    def func_plot(self, key, ax_key, item, func, kwargs):
        """
        :param key:
        :param ax_key:
        :param item:
        :param func:
        :param plot_setting:
        :return:
        """
        args = self.get_data_args(key, item)
        func.run(self.fig.axes[ax_key].ax,
                 args, kwargs)

    def update_axes(self):
        """
        :param item:
        :param ax:
        :return:
        """
        for ax_key in self.fig.axes.keys():
            data_key = self.fig.axes[ax_key].data_key
            if self.fig.axes[ax_key].get('update_axes'):
                for key, item in self.fig.axes[ax_key].get('update_axes').items():
                    if 'function' in item:
                        func = self.fig.axes[ax_key].functions.get(item.get('function'))()
                        value_key = item.get('data_key')
                        value = self.get_key_data(data_key, value_key)
                        func.run(self.fig.axes[ax_key].ax, key, value)

    def get_key_data(self, data_key, header_key):
        """
        :param key:
        :param header_key:
        :return:
        """
        if isinstance(data_key, list):
            value_list = []
            symbols = [' (circles)', ' (triangles)']
            for i, d_key in enumerate(data_key):
                value_list.append(self.data[d_key].get(header_key) + symbols[i])
            value = '\n'.join(value_list)
        else:
            try:
                value = self.data[data_key].get(header_key)
            except KeyError:
                value = None

        return value

    def get_data_args(self, key, plot_setting):
        """
        :return:
        """
        if isinstance(plot_setting, dict):
            data_type = plot_setting.get('data_type')
        else:
            return []

        if data_type:
            data = self.data[key].get(data_type)
            args = [data[param] for param in plot_setting.get('data_keys')]
            return args
        elif plot_setting.get('args'):
            return plot_setting.get('args')
        else:
            return []

    @staticmethod
    def get_data_kwargs(default_kwargs, item, secondary=False):
        """
        :param default_kwargs:
        :param item:
        :param secondary:
        :return:
        """
        if isinstance(item, dict):
            if secondary:
                item_kwargs = item.get('secondary_kwargs')
            else:
                item_kwargs = item.get('kwargs')
        else:
            item_kwargs = None
        kwargs = utils.recursive_dict_update(copy.copy(default_kwargs),
                                             item_kwargs)
        return kwargs


if __name__ == '__main__':
    plt_obj = FigureSetup()
    plt_obj.set_figure_settings('The Skagerrak')
    plt_obj.refresh_mpl_figure()
    plt_obj.refresh_axes()