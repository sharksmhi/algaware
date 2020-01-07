# -*- coding: utf-8 -*-
"""
Created on 2019-12-05 14:38

@author: a002028

"""
import numpy as np
import pandas as pd
from datetime import datetime as dt

from .boolian_base import StatBooleanBase
import readers
from .interpolate import get_interpolated_df


class StatisticsHandler(StatBooleanBase):
    """
    """
    def __init__(self, statpath=''):
        super().__init__()
        self.data = readers.load_txt(statpath, as_dtype=False, fill_nan=np.nan)
        float_columns = self.data.keys()[3:]
        self.data.loc[:, float_columns] = self.data.loc[:, float_columns].astype(float)

    @staticmethod
    def map_value(string):
        """
        #FIXME fixa en ordentlig mappning ist!
        :param string:
        :return:
        """
        if string == 'KOSTERFJORDEN':
            return 'KOSTERFJORDEN (NR16)'
        if string == 'BY20 FÅRÖDJUPET':
            return 'BY20 FÅRÖDJ'
        if string == 'BCS  III-10':
            return 'BCS III-10'
        if string == 'BY32 NORRKÖPING':
            return 'BY32 NORRKÖPINGSDJ'
        if string == 'CPHL':
            return 'CHLA'
        return string

    @staticmethod
    def get_interpolated_data(data):
        """
        :param data:
        :return:
        """
        df_stat_intp = get_interpolated_df(data, x_key='datetime', y_key='std_low')
        df_stat_intp_2 = get_interpolated_df(data, x_key='datetime', y_key='std_hi')
        df_stat_intp_3 = get_interpolated_df(data, x_key='datetime', y_key='mean')
        df_stat_intp['datetime'] = df_stat_intp['x']
        df_stat_intp['std_low'] = df_stat_intp['y']
        df_stat_intp['std_hi'] = df_stat_intp_2['y']
        df_stat_intp['mean'] = df_stat_intp_3['y']

        return df_stat_intp

    def get_value(self, station, month, param, statistic_param='mean'):
        """
        :param month:
        :param param:
        :param statistic_param:
        :return:
        """
        param = self.map_value(param)
        station = self.map_value(station)

        self.reset_boolean()
        self.add_boolean_equal('STATN', station)
        self.add_boolean_equal('MONTH', month)
        if self.index.any():
            return self.data.iloc[self.index[0]][':'.join([param, statistic_param])]
        else:
            return np.nan

    @staticmethod
    def get_point_data(data, param=''):
        """
        :param current_data:
        :return:
        """
        dictionary = {'Time': [],
                      'Date': [],
                      'Data': []}
        for i, row in data.iterrows():
            dictionary['Time'].append(row['datetime'])
            dictionary['Date'].append(row['datetime'].strftime('%Y-%m-%d'))
            dictionary['Data'].append(row[param])
        return pd.DataFrame(dictionary)

    def add_edge_data(self, data, mean_param):
        """
        :param data:
        :return:
        """
        if 1 in data['datetime'].dt.month.values and 12 in data['datetime'].dt.month.values:
            year = str(data['datetime'][0].year)
            mean_low = np.nanmean([data['std_low'].iloc[0], data['std_low'].iloc[-1]])
            mean_hi = np.nanmean([data['std_hi'].iloc[0], data['std_hi'].iloc[-1]])
            mean_mean = np.nanmean([data[mean_param].iloc[0], data[mean_param].iloc[-1]])
            df_first = pd.DataFrame({'datetime': [self.get_datetime(year, '1', '1')],
                                     'std_low': [mean_low], 'std_hi': [mean_hi], 'mean': [mean_mean]})
            df_last = pd.DataFrame({'datetime': [self.get_datetime(year, '12', '31')],
                                    'std_low': [mean_low], 'std_hi': [mean_hi], 'mean': [mean_mean]})

            return pd.concat([df_first, data, df_last]).reset_index(drop=True)

        return data

    @staticmethod
    def get_no_data_df(point_data):
        """
        Ugly solution to a plotting problem concerning axis tickmarks and ticklabels.
        :param point_data:
        :return:
        """
        no_data = {}
        no_data['Data'] = [np.nan] * len(point_data['Time'])
        no_data['Time'] = point_data['Time']
        return no_data

    @staticmethod
    def get_datetime(y, m, d):
        """
        :param y:
        :param m:
        :param d:
        :return:
        """
        return dt.strptime(''.join([y, m.zfill(2), d.zfill(2)]), "%Y%m%d")

    def get_hi_lo_std(self, station, param, current_year=''):
        """
        :param station:
        :param param:
        :param current_data:
        :return:
        """
        param_mapped = self.map_value(param)
        station = self.map_value(station)

        self.reset_boolean()
        self.add_boolean_equal('STATN', station)
        std_param = ':'.join([param_mapped, 'std'])
        mean_param = ':'.join([param_mapped, 'mean'])
        self.add_boolean_not_nan(mean_param)
        data = self.data.iloc[self.index][['MONTH', std_param, mean_param]].reset_index(drop=True)
        data['datetime'] = data['MONTH'].apply(
            lambda x: self.get_datetime(current_year, str(x).replace('.0', '').zfill(2), '15'))
        self._add_stat_data(data, mean_param, std_param)
        data = self.add_edge_data(data, mean_param)
        return data

    @staticmethod
    def _add_stat_data(data, mean_param, std_param):
        """
        :param data:
        :param mean_param:
        :param std_param:
        :return:
        """
        data['mean'] = data[mean_param]
        data['std_low'] = data[mean_param] - data[std_param]
        data['std_hi'] = data[mean_param] + data[std_param]
        data['std_low'] = data['std_low'].apply(lambda x: x if x > 0 else 0)
