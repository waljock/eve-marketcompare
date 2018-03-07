# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 18:39:23 2018

@author: HMA03468
"""

import yaml
import os

path = os.getcwd()

file1 = "typeIDs.yaml"

with open(file1, 'r', encoding="utf8") as fp:
    read_data = yaml.load(fp)