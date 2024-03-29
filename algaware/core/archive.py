#!/usr/bin/env python
# Copyright (c) 2022 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2022-05-23 15:20

@author: johannes
"""
from pathlib import Path
import pandas as pd
import datetime
import numpy as np


def floater(v):
    """"""
    return float(v) if v else np.nan


class SHARKarchive:
    """Class to extract data from SHARK archives."""

    def __init__(self, archive_path=None, year=None, stations=None):
        if not year:
            year = str(datetime.date.today().year)
        else:
            year = str(year)

        self.stations = stations or []
        #self.archive_path = archive_path or fr'C:\Arbetsmapp\datasets\PhysicalChemical\{year}\SHARK_PhysicalChemical_{year}_BAS_SMHI\processed_data\data.txt'
        self.archive_path = archive_path or fr'C:\PhysicalChemical\{year}\SHARK_PhysicalChemical_{year}_BAS_SMHI\processed_data\data.txt'
        self._clear_selection()

        _df = pd.read_csv(
            Path(__file__).parent.parent.joinpath('etc', 'station_mapper.txt'),
            sep='\t',
            header=0,
            encoding='cp1252',
            dtype=str,
            keep_default_na=False,
        )
        self.statn_mapper = {syno: statn for syno, statn in _df.values}

    def _clear_selection(self):
        self.select_list = []
        self.in_dict = {}
        self.between = {}
        self.more_than = {}
        self.less_than = {}
        self.equal_to = {}
        self.like = {}

        self.item_list = []

    def add_select(self, item):
        if type(item) == list:
            self.select_list.extend(item)
        else:
            self.select_list.append(item)

    def add_in_dict(self, item_dict):
        self.in_dict.update(item_dict)

    def add_between(self, item_dict):
        self.between.update(item_dict)

    def add_more_than(self, item_dict):
        self.more_than.update(item_dict)

    def add_less_than(self, item_dict):
        self.less_than.update(item_dict)

    def add_equal_to(self, item_dict):
        self.equal_to.update(item_dict)

    def add_like(self, item_dict):
        self.like.update(item_dict)

    def get_data_in_dataframe(self):
        """"""
        df = pd.read_csv(
            self.archive_path,
            sep='\t',
            header=0,
            encoding='cp1252',
            dtype=str,
            keep_default_na=False,
        )
        columns = ['SHIPC', 'STATN', 'SDATE', 'SERNO',
                   'DEPH', 'CHLA', 'Q_CHLA', 'CTDCPHL']
        parameter_mapping = {
            'CPHL': 'CHLA', 'Q_CPHL': 'Q_CHLA', 'FLUO_CTD': 'CTDCPHL'
        }
        df = df.rename(parameter_mapping, axis=1)
        df['STATN'] = df['STATN'].apply(self._mapper)
        df = df.loc[df['STATN'].isin(self.stations), :].reset_index(drop=True)
        for col in ('DEPH', 'CHLA', 'CTDCPHL'):
            df[col] = df[col].apply(floater)
        print('SHARK-archive load completed!')

        return df[columns]

    def _mapper(self, v):
        """Map synonym name to nominell station name."""
        return self.statn_mapper.get(v, v)


if __name__ == '__main__':
    sa = SHARKarchive(stations=[
        "Å13", "Å15", "Å17", "SLÄGGÖ", "P2", "FLADEN", "ANHOLT E",
        "N14 FALKENBERG", "W LANDSKRONA",
        "BY1", "BY2 ARKONA", "BY4 CHRISTIANSÖ", "BY5 BORNHOLMSDJ", "REF M1V1",
        "BY32 NORRKÖPINGSDJ", "BY38 KARLSÖDJ", "BY10", "BY15 GOTLANDSDJ",
        "BY20 FÅRÖDJ", "BCS III-10"
    ])
    df = sa.get_data_in_dataframe()
