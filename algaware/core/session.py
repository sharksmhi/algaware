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

    def initialize_data_handler(self, ctd_directory=None):
        """
        :return:
        """
        self.data_handler = DataHandler(start_time=self.start_time,
                                        end_time=self.end_time,
                                        settings=self.settings,
                                        ctd_directory=ctd_directory)

    def initialize_figure_handler(self):
        """
        :return:
        """
        self.figure_handler = alg_plot.FigureSetup(setup=self.settings.plot_setup)

    def initialize_plot_handler(self):
        """
        :return:
        """
        self.plot_handler = alg_plot.PlotAlgaware(figure_setup=self.figure_handler,
                                                  data=self.data_handler.data_dict,
                                                  station_key_map=self.data_handler.station_key_map)

    def initialize_statistic_handler(self):
        """
        :return:
        """
        # TODO: Do we need statistics here? perhaps we could move it directly to the datahandler ?
        statistics_directory = '/'.join((self.settings.base_directory, 'etc', 'statistics',
                                         'annual_2001-2015_ctd_temp_salt_statistics_chl20m.txt'))
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

    def load_data(self):
        """
        :return:
        """
        self.data_handler.load_all_data_sources()
        self._append_statistics_to_data_handler()

    def _append_statistics_to_data_handler(self):
        """
        :return:
        """
        self.data_handler.add_annual_statistics_to_dictionary(self.statistic_handler)


if __name__ == '__main__':

    # Input from GUI (SHARKtools)
    # start_time = pd.Timestamp(2019, 11, 1)
    # end_time = pd.Timestamp(2019, 11, 30)
    start_time = pd.Timestamp(2020, 1, 1)
    end_time = pd.Timestamp(2020, 1, 31)
    year = start_time.year

    # settings = config.Settings()

    s = Session()
    # s.update_attributes(**{'start_time': '2020-01-01',
    #                        'end_time': '2020-01-31'})
    s.update_attributes(**{'start_time': '2020-02-01',
                           'end_time': '2020-02-29'})
    s.initialize_statistic_handler()
    s.initialize_data_handler()
    # s.load_data()
    #
    # s.initialize_figure_handler()

    # # fig_obj.set_figure_settings('The Skagerrak')
    # # fig_obj.set_figure_settings('The Kattegat and The Sound')
    # # fig_obj.set_figure_settings('The Southern Baltic')
    # # fig_obj.set_figure_settings('The Western Baltic')
    # fig_obj.set_figure_settings('The Eastern Baltic')
    # s.update_figure_settings('The Skagerrak')
    # s.update_figure_settings('The Kattegat and The Sound')
    # s.update_figure_settings('The Southern Baltic')
    # s.update_figure_settings('The Western Baltic')
    # s.update_figure_settings('The Eastern Baltic')
    #
    # s.initialize_plot_handler()
    # s.plot_figure()


    # statpath = 'etc\\statistics\\annual_2001-2015_ctd_temp_salt_statistics.txt'
    # statpath = 'etc\\statistics\\annual_2001-2015_ctd_temp_salt_statistics_chl20m.txt'
    # sh = data_core.StatisticsHandler(statpath=statpath)
    # dh = data_core.datahandler.DataHandler(start_time=start_time, end_time=end_time, settings=settings)
    #
    # print('session_key_list', dh.si_handler.session_key_list)
    #
    # start_timeit = time.time()
    # dh.load_all_data_sources()
    # print("Timed: --data loaded in %.3f sec" % (time.time() - start_timeit))
    # dh.add_annual_statistics_to_dictionary(sh)
    #
    # # dh.get_ctd_data()
    # # ctd_data = dh.get_ctd_data()
    # #
    # # si_data = dh.get_sharkint_data()
    # # si_data = si.get_data_in_dataframe()
    # # start_time = time.time()
    #
    # start_timeit = time.time()
    # fig_obj = plot.FigureSetup(setup=settings.plot_setup)
    # # fig_obj.set_figure_settings('The Skagerrak')
    # # fig_obj.set_figure_settings('The Kattegat and The Sound')
    # # fig_obj.set_figure_settings('The Southern Baltic')
    # # fig_obj.set_figure_settings('The Western Baltic')
    # fig_obj.set_figure_settings('The Eastern Baltic')
    # fig_obj.refresh_mpl_figure()
    # fig_obj.refresh_axes()
    # print("Timed: --%.3f sec" % (time.time() - start_timeit))
    #
    # start_timeit = time.time()
    # plt_obj = plot.PlotAlgaware(figure_setup=fig_obj,
    #                             data=dh.data_dict,
    #                             station_key_map=dh.station_key_map)
    #
    # plt_obj.plot()
    # print("Plot time: --%.3f sec" % (time.time() - start_timeit))
    # start_timeit = time.time()
    # plt_obj.update_axes()
    # plt_obj.add_legend()
    # print("update_axes time: --%.3f sec" % (time.time() - start_timeit))
    # print("Plot time: --%.3f sec" % (time.time() - start_timeit))
    # fig_obj.save(fmt=['eps', 'png'])
    # print("Save time: --%.3f sec" % (time.time() - start_timeit))
