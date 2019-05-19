# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:11:03 2019

@author:        DATAmadness
Github:         https://github.com/datamadness
Blog:           https://datamadness.github.io
Description:      
Source: Statistics Canada, 2016 Census of Population
"""

import requests
import pandas as pd
import json

class region_slicer:
    
    #Dictionary of all possible ways to slice Canada into regions
    geo_levels = {'CD' : 'Census divisions',
                'CMACA' : 'Census metropolitan areas and census agglomerations',
                'CSD' : 'Census subdivisions (municipalities)',
                'CT' : 'Census tracts',
                'DPL' : 'Designated places',
                'ER' : 'Economic regions',
                'FED' : 'Federal electoral districts (2013 Representation Order)',
                'FSA' : 'Forward sortation areas',
                'HR' : 'Health regions (including LHINs and PHUs)',
                'POPCNTR' : 'Population centres',
                'PR' : 'Canada, provinces and territories'}
    
    #Dictionary of codes defining for which province / territory weto receive granular geo data
    provincial_codes = {'00': 'All provinces and territories',
                        '10': 'Newfoundland and Labrador',
                        '11': 'Prince Edward Island',
                        '12': 'Nova Scotia',
                        '13': 'New Brunswick',
                        '24': 'Quebec',
                        '35': 'Ontario',
                        '46': 'Manitoba',
                        '47': 'Saskatchewan',
                        '48': 'Alberta',
                        '59': 'British Columbia',
                        '60': 'Yukon',
                        '61': 'Northwest Territories',
                        '62': 'Nunavut'}

    #Initiate the geo object with API acll parameters
    def __init__(self, geo_level = 'POPCNTR', province = '00'):

        self.base_url = 'https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json'
        self.params = {'lang': 'E',         #language
                       'geos': geo_level,   #region type e.g.economic vs census
                       'cpt': province}     #province / territory code 00->all
    #Call statscan and receive the desired geo data
    def get_data(self):
        response = requests.get(self.base_url, self.params)
        decoded_response = json.loads(response.text[2:])
        
        #Split API answer into list of columns and list of teh geo data
        columns = decoded_response['COLUMNS']
        data = decoded_response['DATA']
        
        #Create a pandas DataFrame from the columns names and data records
        self.geo_dataDataFrame = pd.DataFrame.from_records(data, columns = columns)
        self.columns = columns
        
        #Provide user feedback whether the call was successfull or not
        if response.status_code == 200:
            print('Successfully received geo data')
        elif response.status_code == 404:
            print('Something went wrong during geo data retrieaval')
        
        return self.geo_dataDataFrame
