# -*- coding: utf-8 -*-
"""
Created on 2019-08-30 15:05

@author: a002028

"""
import numpy as np


class DataBooleanBase(object):
    """

    """
    def __init__(self):
        super().__init__()
        self.data = None
        self._boolean = True

    def boolean_not_nan(self, param):
        """
        :param param:
        :return:
        """
        return self.data[param].notna()

    def add_boolean_from_list(self, parameter, value_list):
        """
        :param parameter:
        :param value_list:
        :return: Adds boolean to self.boolean. See property: self.boolean
        """
        self.boolean = self.data[parameter].isin(value_list)

    def add_boolean_month(self, month):
        """
        :param month:
        :return:
        """
        self.boolean = self.data['timestamp'].dt.month == month

    def add_boolean_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] == value

    def add_boolean_less_or_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] <= value

    def reset_boolean(self):
        """"""
        self._boolean = True

    @property
    def index(self):
        """"""
        return np.where(self.boolean)[0]

    @property
    def boolean(self):
        """"""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """"""
        self._boolean = self._boolean & add_bool


class MeanDataBooleanBase(object):
    """

    """
    def __init__(self):
        super().__init__()
        self.data = None
        self._boolean = True
        self._boolean_combo = {}

    def add_boolean_from_list(self, parameter, value_list):
        """
        :param parameter:
        :param value_list:
        :return: Adds boolean to self.boolean. See property: self.boolean
        """
        self.boolean = self.data[parameter].isin(value_list)

    def add_boolean_month(self, month):
        """
        :param month:
        :return:
        """
        self.boolean = self.data['timestamp'].dt.month == month

    def add_boolean_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] == value

    def add_boolean_less_or_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] <= value

    def add_boolean_greater_or_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] >= value

    def add_boolean_not_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] != value

    def add_boolean_not_nan(self, param):
        """
        :param param:
        :return:
        """
        self.boolean = self.data[param].notna()

    def reset_boolean(self):
        """"""
        self._boolean = True

    def reset_boolean_combo(self):
        """"""
        self._boolean_combo = {}

    def add_combo_boolean(self, key, boolean, only_true_values=False):
        """"""
        self._boolean_combo[key] = boolean
        if only_true_values:
            boolean_true = self.boolean_not_nan(key)
            self._boolean_combo[key] = self._boolean_combo[key] & boolean_true

    def remove_combo_boolean(self, key):
        """"""
        self._boolean_combo.pop(key, None)

    def boolean_not_nan(self, param):
        """
        :param param:
        :return:
        """
        return self.data[param].notna()

    @property
    def combo_boolean_all(self):
        """"""
        try:
            return np.column_stack([self._boolean_combo[key] for key in self._boolean_combo.keys()]).all(axis=1)
        except ValueError:
            return self._boolean

    @property
    def combo_boolean_any(self):
        """"""
        return np.column_stack([self._boolean_combo[key] for key in self._boolean_combo.keys()]).any(axis=1)

    @property
    def index(self):
        """"""
        return np.where(self.boolean)[0]

    @property
    def boolean(self):
        """"""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """"""
        self._boolean = self._boolean & add_bool


class StatBooleanBase(object):
    """

    """
    def __init__(self):
        super().__init__()
        self.data = None
        self._boolean = True

    def add_boolean_from_list(self, parameter, value_list):
        """
        :param parameter:
        :param value_list:
        :return: Adds boolean to self.boolean. See property: self.boolean
        """
        self.boolean = self.data[parameter].isin(value_list)

    def add_boolean_month(self, month):
        """
        :param month:
        :return:
        """
        self.boolean = self.data['timestamp'].dt.month == month

    def add_boolean_equal(self, param, value):
        """
        :param param:
        :param value:
        :return:
        """
        self.boolean = self.data[param] == value

    def add_boolean_not_nan(self, param):
        """
        :param param:
        :return:
        """
        self.boolean = self.data[param].notna()

    def reset_boolean(self):
        """"""
        self._boolean = True

    @property
    def index(self):
        """"""
        return np.where(self.boolean)[0]

    @property
    def boolean(self):
        """"""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """"""
        self._boolean = self._boolean & add_bool
