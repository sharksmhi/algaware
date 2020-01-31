# -*- coding: utf-8 -*-
"""
Created on 2019-11-29 14:18

@author: a002028

"""
try:
    from .datahandler import DataHandler
    from .boolean_base import DataBooleanBase, MeanDataBooleanBase, StatBooleanBase
    from .interpolate import get_interpolated_df
    from .statistics import StatisticsHandler
    from .session import Session
    from .algaware_config import Settings
except:
    from . import datahandler
    from . import boolean_base
    from . import interpolate
    from . import statistics
    from . import session
    from . import algaware_config
