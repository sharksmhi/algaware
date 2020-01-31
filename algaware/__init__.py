# -*- coding: utf-8 -*-
"""
Created on 2019-11-26 16:26

@author: a002028

"""
from . import alg_plot
from . import data_core
from . import readers

import os
import sys
package_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(package_path)

name = "algaware"
