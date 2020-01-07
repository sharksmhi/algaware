# -*- coding: utf-8 -*-
"""
Created on Thu Jul 05 10:29:30 2018

@author: a002028
"""
import os
import utils
import numpy as np
import yaml


class YAMLreader(dict):
    """
    """
    def __init__(self):
        super().__init__()

        self.config = {}

    def load_yaml(self, config_files, file_names_as_key=False, return_config=False):
        """

        :param config_files: Preferably list of file paths
        :param file_names_as_key: False | True
        :param return_config: False | True
        :return: Dictionary with loaded files specifications
        """
        for config_file in config_files:
            with open(config_file, encoding='utf8') as fd:
                try:
                    file = yaml.load(fd)
                except yaml.YAMLError:
                    file = yaml.safe_load(fd)
                if file_names_as_key:
                    file_name = self.get_file_name(config_file)
                    self.config[file_name] = file
                else:
                    self.config = utils.recursive_dict_update(self.config, file)

        if return_config:
            return self.config

    @staticmethod
    def get_file_name(file_path):
        """
        :param file_path: str, complete path to file
        :return: filename without extension
        """
        filename = os.path.basename(file_path)
        return os.path.splitext(filename)[0]

    """
    #   USE WITH CTDPY YAMLWRITER   warning!!  do not use .safe_dump!! use .dump!
    """
    # yw = YAMLwriter()
    #
    # j_path = 'C:/Utveckling/algaware/etc/plot_setup.json'
    # with open(j_path, 'r') as fd:
    #     setup = json.load(fd)
    #
    # setup['function_types'] = {'date_locator': plot.functions.MPLDatelocator,
    #                            'date_formatter': plot.functions.MPLDateformatter}
    #
    # setup['algaware']['figures']['The Skagerrak']['axes']['7']['x_axis']['major_locator'] = {'style': 'month',
    #                                                                                          'args': [],
    #                                                                                          'kwargs': {},
    #                                                                                          'function': 'date_locator'}
    #
    # setup['algaware']['figures']['The Skagerrak']['axes']['7']['x_axis']['major_formatter'] = {'style': 'date',
    #                                                                                            'args': [''],
    #                                                                                            'kwargs': {},
    #                                                                                            'function': 'date_formatter'}
    #
    # setup['algaware']['figures']['The Skagerrak']['axes']['7']['x_axis']['minor_locator'] = {'style': 'month',
    #                                                                                          'args': [],
    #                                                                                          'kwargs': {
    #                                                                                              'bymonthday': 15},
    #                                                                                          'function': 'date_locator'}
    #
    # setup['algaware']['figures']['The Skagerrak']['axes']['7']['x_axis']['minor_formatter'] = {'style': 'date',
    #                                                                                            'args': ['%b'],
    #                                                                                            'kwargs': {},
    #                                                                                            'function': 'date_formatter'}
    #
    # yw.write_yaml(setup, out_path=j_path.replace('.json', '.yaml'))