# -*- coding: utf-8 -*-
"""
Created on 2019-11-26 16:40

@author: a002028

"""
import sys
import time
# sys.path.append('C:/Utveckling/ctdpy')
# sys.path.append("..")
import data_core
import plot
import config

from datetime import datetime as dt
import datetime
import matplotlib.dates as mdates
import json
import yaml
import numpy as np
import pandas as pd


import datetime


if __name__ == '__main__':

    # Input from GUI (SHARKtools)
    # start_time = pd.Timestamp(2019, 11, 1)
    # end_time = pd.Timestamp(2019, 11, 30)
    start_time = pd.Timestamp(2019, 10, 1)
    end_time = pd.Timestamp(2019, 10, 31)
    year = start_time.year

    settings = config.Settings()

    statpath = 'etc\\statistics\\annual_2001-2015_ctd_temp_salt_statistics.txt'
    sh = data_core.StatisticsHandler(statpath=statpath)
    dh = data_core.datahandler.DataHandler(start_time=start_time, end_time=end_time)

    print('session_key_list', dh.si_handler.session_key_list)

    start_time = time.time()
    dh.load_all_data_sources()
    print("Timed: --data loaded in %.3f sec" % (time.time() - start_time))
    dh.add_annual_statistics_to_dictionary(sh)

    # dh.get_ctd_data()
    # ctd_data = dh.get_ctd_data()
    #
    # si_data = dh.get_sharkint_data()
    # si_data = si.get_data_in_dataframe()
    # start_time = time.time()

    start_time = time.time()
    fig_obj = plot.FigureSetup(setup=settings.plot_setup)
    # fig_obj.set_figure_settings('The Skagerrak')
    # fig_obj.set_figure_settings('The Kattegat and The Sound')
    # fig_obj.set_figure_settings('The Southern Baltic')
    # fig_obj.set_figure_settings('The Western Baltic')
    fig_obj.set_figure_settings('The Eastern Baltic')
    fig_obj.refresh_mpl_figure()
    fig_obj.refresh_axes()
    print("Timed: --%.3f sec" % (time.time() - start_time))

    start_time = time.time()
    plt_obj = plot.PlotAlgaware(figure_setup=fig_obj,
                                data=dh.data_dict,
                                station_key_map=dh.station_key_map)

    plt_obj.plot()
    print("Plot time: --%.3f sec" % (time.time() - start_time))
    start_time = time.time()
    plt_obj.update_axes()
    print("update_axes time: --%.3f sec" % (time.time() - start_time))
    print("Plot time: --%.3f sec" % (time.time() - start_time))
    fig_obj.save()
    print("Save time: --%.3f sec" % (time.time() - start_time))
