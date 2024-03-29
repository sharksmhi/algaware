# -*- coding: utf-8 -*-
"""
Created on 2019-11-26 16:40

@author: a002028

"""
import os
import time
import pandas as pd

from algaware.core.datahandler import DataHandler
from algaware.core.statistics import StatisticsHandler
from algaware.core.config import Settings

from algaware.plot import plot as alg_plot


class BaseSession(object):
    """
    """
    year = int(time.strftime('%Y'))

    def __init__(self):
        super().__init__()
        self._start_time = None
        self._end_time = None

    def update_attributes(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for item, value in kwargs.items():
            setattr(self, item, value)

    @classmethod
    def update_year(cls, value):
        cls.year = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, time_string):
        self._start_time = pd.Timestamp(time_string)

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, time_string):
        self._end_time = pd.Timestamp(time_string)


class Session(BaseSession):
    """
    """
    def __init__(self):
        super().__init__()
        self.statistic_handler = None
        self.data_handler = None
        self.figure_handler = None

        self.settings = Settings()

    def get_xlist(self):
        """
        :return:
        """
        return self.data_handler.get_station_data_information()

    def initialize_data_handler(self, ctd_directory=None, lims_path=None, archive_root_dir=None):
        """
        :return:
        """
        self.data_handler = DataHandler(
            start_time=self.start_time,
            end_time=self.end_time,
            settings=self.settings,
            ctd_directory=ctd_directory,
            lims_path=lims_path,
            archive_root_dir=archive_root_dir
        )

    def initialize_figure_handler(self):
        """
        :return:
        """
        self.figure_handler = alg_plot.FigureSetup(setup=self.settings.plot_setup)

    def update_figure_settings(self, settings_key):
        """
        :param settings_key: For Algaware figures this key can be either of the following:
                             - 'The Skagerrak'
                             - 'The Kattegat and The Sound'
                             - 'The Southern Baltic'
                             - 'The Western Baltic'
                             - 'The Eastern Baltic'
        :return:
        """
        self.figure_handler.set_figure_settings(settings_key)
        self.figure_handler.refresh_mpl_figure()
        self.figure_handler.refresh_axes()

    def initialize_plot_handler(self):
        """
        :return:
        """
        self.plot_handler = alg_plot.PlotAlgaware(
            figure_setup=self.figure_handler,
            data=self.data_handler.data_dict,
            station_key_map=self.data_handler.station_key_map
        )

    def initialize_statistic_handler(self):
        """
        :return:
        """
        # TODO: Do we need statistics here? perhaps we could move it directly to the datahandler ?
        statistics_directory = '/'.join((self.settings.base_directory, 'etc', 'statistics',
                                         'annual_1991-2020_statistics_chl20m.txt'))
        self.statistic_handler = StatisticsHandler(statpath=statistics_directory)

    def plot_figure(self, save_as_format=['eps', 'png']):
        """
        :param save_as_format:
        :return:
        """
        # start_timeit = time.time()
        self.plot_handler.plot()
        # print("Plot time: --%.3f sec" % (time.time() - start_timeit))
        # start_timeit = time.time()
        self.plot_handler.update_axes()
        self.plot_handler.add_legend()
        # print("update_axes time: --%.3f sec" % (time.time() - start_timeit))
        # print("Plot time: --%.3f sec" % (time.time() - start_timeit))
        self.figure_handler.save(fmt=save_as_format)

    def load_data(self):
        """
        :return:
        """
        self.data_handler.load_all_data_sources()
        self.data_handler.store_station_max_values()
        self._append_statistics_to_data_handler()

        self._update_axes_range_settings()

    def _append_statistics_to_data_handler(self):
        """
        :return:
        """
        self.data_handler.add_annual_statistics_to_dictionary(self.statistic_handler)

    def _update_axes_range_settings(self):
        #TODO Preliminary solution to update axes / ticks based on max value data
        range_tick_mapper = {
            10: {'range': [[0, 10]], 'ticks': [[0,2,4,6,8,10]]},
            15: {'range': [[0, 15]], 'ticks': [[0,3,6,9,12,15]]},
            20: {'range': [[0, 20]], 'ticks': [[0,4,8,12,16,20]]},
            25: {'range': [[0, 25]], 'ticks': [[0,5,10,15,20,25]]},
            30: {'range': [[0, 30]], 'ticks': [[0,6,12,18,24,30]]},
        }
        def get_max_value(current_value, statn):
            if self.data_handler.profile_max_values.get(statn, current_value-1) > current_value:
                return int(self.data_handler.profile_max_values[statn]) + 1
            else:
                return current_value

        def get_ranges_and_ticks(value):
            for check_value in sorted(range_tick_mapper):
                if value <= check_value:
                    return range_tick_mapper.get(check_value)

        basin_maximums = {}
        for basin, item in self.settings.basin_station_mapping.items():
            basin_maximums[basin] = 0
            for statn in item:
                basin_maximums[basin] = get_max_value(basin_maximums[basin], statn)

        for basin, basin_item in self.settings.plot_setup['algaware']['figures'].items():
            for axes_key, axes_item in basin_item['axes'].items():
                statn = axes_item.get('statn_nom')
                if int(axes_key)%2 == 0 and axes_item['x_axis'].get('parent'):
                    std_max = int(axes_item['x_axis']['set_xlim']['args'][0][1])
                    if basin_maximums[basin] > std_max:
                        ranges_and_ticks = get_ranges_and_ticks(basin_maximums[basin])
                        axes_item['x_axis']['set_xlim']['args'] = ranges_and_ticks['range']
                        axes_item['x_axis']['major_locator']['args'] = ranges_and_ticks['ticks']

                elif int(axes_key)%2 != 0 and axes_item['y_axis'].get('parent'):
                    std_max = int(axes_item['y_axis']['set_ylim']['args'][0][1])
                    if basin_maximums[basin] > std_max:
                        ranges_and_ticks = get_ranges_and_ticks(basin_maximums[basin])
                        axes_item['y_axis']['set_ylim']['args'] = ranges_and_ticks['range']
                        axes_item['y_axis']['set_yticks']['args'] = ranges_and_ticks['ticks']
                else:
                    pass

