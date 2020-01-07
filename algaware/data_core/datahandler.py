# -*- coding: utf-8 -*-
"""
Created on 2019-11-26 16:35

@author: a002028

"""

import pandas as pd
import numpy as np
import sys
sys.path.append('C:/Utveckling/ctdpy')
import ctdpy
sys.path.remove('C:/Utveckling/ctdpy')

import data_core
from .boolian_base import MeanDataBooleanBase


class CTDDataHandler(object):
    """

    """
    def __init__(self, base_directory=None):
        if not base_directory:
            # ONLY FOR TESTING
            # base_directory = '//winfs-proj/proj/havgem/EXPRAPP/Exprap2019/Aranda v45-46 November/CTD/CNV/'
            base_directory = '//winfs-proj/proj/havgem/EXPRAPP/Exprap2019/Aranda v42 okt/ctd/cnv/'
        files = ctdpy.core.utils.generate_filepaths(base_directory,
                                                    endswith='.cnv',
                                                    )
        self.ctd_session = ctdpy.core.session.Session(reader='smhi',
                                                      filepaths=files)
        self.fid_mapping = {}

    def load_data(self):
        """
        :return:
        """
        self.data = self.read_data()

        self.set_ctd_keys()

    def get_key_data(self, key):
        """
        :param key:
        :return:
        """
        selected_columns = ['PRES_CTD', 'DEPH', 'CHLFLUO_CTD']
        #TODO do we want to include certain columns?
        fid = self.fid_mapping.get(key)
        if fid:
            df = self.data[self.fid_mapping.get(key)]['hires_data']
            df = df.loc[:, selected_columns].astype(float)
            boolean = df['DEPH'] <= 50.0
            df = df.loc[boolean, :]
        else:
            df = None
        return df

    def read_data(self):
        """
        :return:
        """
        datasets = self.ctd_session.read()
        return datasets[0]

    def set_ctd_keys(self):
        """
        :param data:
        :return:
        """
        for fid in self.data.keys():
            myear = str(ctdpy.core.utils.get_timestamp(self.data[fid]['metadata'].get('SDATE')).year)
            shipc = self.ctd_session.settings.smap.map_shipc(self.data[fid]['metadata'].get('SHIPC'))
            serno = self.data[fid]['metadata'].get('SERNO')
            key = '_'.join([myear, shipc, serno])
            self.data[fid]['metadata']['key'] = key
            self.fid_mapping.setdefault(key, fid)


class SHARKintDataHandler(MeanDataBooleanBase):
    """

    """
    def __init__(self, ship_mapper=None, start_time=None, end_time=None):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.smap = ship_mapper
        self.si_session = data_core.SHARKintData('prod',
                                                 # start_date=start_time.strftime('%Y%m%d'), end_date=end_time.strftime('%Y%m%d'),
                                                 year=self.start_time.year)
        self._key_list = None

    def get_key_data(self, key):
        """
        :param key:
        :return:
        """
        self.reset_boolean()
        self.add_boolean_equal('key', key)
        return self.data.loc[self.boolean, :].reset_index(drop=True)

    def get_station_data(self, station):
        """
        :param station:
        :return:
        """
        self.reset_boolean()
        self.add_boolean_equal('STATN', station)
        self.add_boolean_less_or_equal('DEPH', 20.0)
        data = self.data.loc[self.boolean, ['timestamp', 'datetime', 'CHLA']]
        return data.groupby(['timestamp', 'datetime'], as_index=False).mean()

    def load_data(self):
        """
        :return:
        """
        self.reset_boolean()
        self.data = self.si_session.get_data_in_dataframe()
        self.add_boolean_not_nan('CHLA')
        self.add_boolean_not_equal('Q_CHLA', 'B')
        self.data = self.data.loc[self.boolean, :].reset_index(drop=True)
        self.set_timestamp('SDATE')
        self.set_datetime_str_format('MYEAR', fmt='%Y')
        self.set_datetime_format('datetime')
        self.map_ship()
        self.set_key()

    def map_ship(self):
        """
        :return:
        """
        self.data['SHIPC'] = self.data['SHIPC'].apply(self.smap)

    def set_datetime_format(self, key):
        """
        :param data:
        :param key:
        :param fmt:
        :return:
        """
        self.data[key] = self.data['timestamp'].apply(pd.to_datetime)

    def set_datetime_str_format(self, key, fmt='%Y'):
        """
        :param data:
        :param key:
        :param fmt:
        :return:
        """
        self.data[key] = self.data['timestamp'].dt.strftime(fmt)

    def set_key(self, keys=None):
        """
        :param keys:
        :param data:
        :return:
        """
        if keys is None:
            keys = ['MYEAR', 'SHIPC', 'SERNO']
        self.data['key'] = self.data[keys].apply(lambda x: '_'.join(x), axis=1)

        self.reset_boolean()
        self.add_boolean_greater_or_equal('timestamp', self.start_time)
        self.add_boolean_less_or_equal('timestamp', self.end_time)

        self.session_key_list = self.data.loc[self.boolean, 'key']

    def set_timestamp(self, key, fmt='%Y'):
        """
        :param data:
        :param key:
        :param fmt:
        :return:
        """
        self.data['timestamp'] = self.data[key].apply(pd.Timestamp)

    @property
    def session_key_list(self):
        """
        :return:
        """
        return self._key_list

    @session_key_list.setter
    def session_key_list(self, x):
        """
        :return:
        """
        self._key_list = x.unique()


class DataHandler(object):
    """
    """
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

        #TODO use some sort of settings object to get data sources
        self.ctd_handler = CTDDataHandler()

        #TODO change location of ship_mapper.. sharkpylib?
        self.si_handler = SHARKintDataHandler(ship_mapper=self.ctd_handler.ctd_session.settings.smap.map_shipc,
                                              start_time=start_time,
                                              end_time=end_time)

        self.data_dict = {}
        self._station_key_map = None

    def load_all_data_sources(self):
        """
        :return:
        """
        self.ctd_handler.load_data()
        self.si_handler.load_data()

        self.update_data_dictionary()

    def update_data_dictionary(self):
        """
        :return:
        """
        for key in self.si_handler.session_key_list:
            key_dict = {}
            key_dict['sharkint_profile'] = self.si_handler.get_key_data(key)
            key_dict['station'] = key_dict['sharkint_profile']['STATN'].iloc[0]
            key_dict['datetime'] = key_dict['sharkint_profile']['datetime'].iloc[0]
            key_dict['sdate'] = key_dict['datetime'].strftime('%Y-%m-%d')
            key_dict['sharkint_surface'] = self.si_handler.get_station_data(key_dict['station'])
            key_dict['ctd'] = self.ctd_handler.get_key_data(key)

            self.data_dict[key] = key_dict

        self.station_key_map = sorted(self.data_dict.keys(), reverse=True)

    def add_annual_statistics_to_dictionary(self, stat_obj):
        """
        :param stat_obj:
        :return:
        """
        print('Adding annual statistics to data source..')
        for key in self.data_dict:
            stat_data = stat_obj.get_hi_lo_std(self.data_dict[key].get('station'),
                                               'CHLA',
                                               current_year=str(self.data_dict[key]['datetime'].year))
            self.data_dict[key]['statistics'] = stat_obj.get_interpolated_data(stat_data)
        print('statistics added to data source')

    @property
    def station_key_map(self):
        """
        :return:
        """
        return self._station_key_map

    @station_key_map.setter
    def station_key_map(self, key_list):
        """
        :return:
        """
        self._station_key_map = {}
        for key in key_list:
            statn = self.data_dict[key].get('station')
            if statn not in self._station_key_map:
                self._station_key_map[statn] = key
            elif isinstance(self._station_key_map[statn], str):
                self._station_key_map[statn] = [self._station_key_map[statn], key]
