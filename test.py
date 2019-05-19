# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:48:47 2019

@author:        DATAmadness
Github:         https://github.com/datamadness
Blog:           https://datamadness.github.io
Description:      
"""
import pandas as pd
from geo_data import region_slicer
from census_data_retriever import census_data


bc_regions = region_slicer(province = '59')
bc_regions.get_data()

income_data = census_data(bc_regions, topic = 7)
#income_data = census_data()
income_data.get_data()

x = income_data.field_filter(field_ids=12013)
x.to_csv('name.csv')
