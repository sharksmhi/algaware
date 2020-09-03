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
                file = yaml.load(fd)
                # try:
                #     file = yaml.load(fd)
                # except yaml.YAMLError:
                #     file = yaml.safe_load(fd)
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
        return os.path.splitext(os.path.basename(file_path))[0]
