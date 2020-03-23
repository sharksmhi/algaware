# -*- coding: utf-8 -*-
"""
Created on 2019-12-05 14:25

@author: a002028

"""
import pandas as pd
import numpy as np
from scipy import interpolate


def get_interpolated_df(df, x_key, y_key):
    """
    :param df:
    :param x_key:
    :param y_key:
    :return:
    """
    if x_key == 'timestamp':
        x = df[x_key].apply(pd.to_datetime).astype(np.int64)
    elif x_key == 'datetime':
        x = df[x_key].astype(np.int64)
    else:
        x = df[x_key]
    i_x, i_y = interpolate_array(x.values, df[y_key].astype(np.float).values)
    out_df = pd.DataFrame({'x': i_x, 'y': i_y})
    if x_key == 'timestamp':
        out_df['x'] = out_df['x'].astype(np.int64).apply(pd.Timestamp)
    elif x_key == 'datetime':
        out_df['x'] = out_df['x'].astype(np.int64).apply(pd.to_datetime)
    return out_df


def interpolate_array(x, y, smooth_rate=500):
    """
    :param x:
    :param y:
    :return:
    """
    interp_obj = interpolate.PchipInterpolator(x, y)
    new_x = np.linspace(x[0], x[-1], smooth_rate)
    new_y = interp_obj(new_x)
    return new_x, new_y
