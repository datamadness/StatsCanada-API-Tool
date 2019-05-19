# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:15:55 2019

@author:        DATAmadness
Github:         https://github.com/datamadness
Blog:           https://datamadness.github.io
Description:
Source: Statistics Canada, 2016 Census of Population    
"""

import requests
import pandas as pd
import json

class census_data:
    
    #Dictionary of all available topics in census data
    topics = {'0': 'All topics',
            '1': 'Aboriginal peoples',
            '2': 'Education',
            '3': 'Ethnic origin',
            '4': 'Families, households and marital status',
            '5': 'Housing',
            '6': 'Immigration and citizenship',
            '7': 'Income',
            '8': 'Journey to work',
            '9': 'Labour',
            '10': 'Language',
            '11': 'Language of work',
            '12': 'Mobility',
            '13': 'Population',
            '14': 'Visible minority'
        }
    
    #Initiate census data object by specifying one or more geo uid with topic code
    def __init__(self, geo_uids = '2016A000011124', topic = str('7')):
        
        #Census data endpoint
        self.base_url = 'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json'
        
        #API parameter specification - outputs list of parameter dictionaries for equal number of calls
        if type(geo_uids) == str:

            self.params = [{'lang': 'E',         #language
                          'dguid': geo_uids,     #geography id
                          'topic': topic,        #topic id
                          'notes': '0'}]         #Do not include notes
        
        elif type(geo_uids) == list:
           self.params =[]
           for guid in geo_uids:
               self.params.append({'lang': 'E',         #language
                          'dguid': guid,                #geography id
                          'topic': topic,               #topic id
                          'notes': '0'}
                       )
        else:
           self.params =[]
           for guid in geo_uids.geo_dataDataFrame['GEO_UID']:
               self.params.append({'lang': 'E',         #language
                          'dguid': guid,                #geography id
                          'topic': topic,               #topic id
                          'notes': '0'}
                       )
        
    #Calls API and retrieves the data -> one call per parameter set in self.params   
    def get_data(self):
        
        #Collect data from each api call into one data list + single list of column names
        appended_data = []
        for call_params in self.params:
            response = requests.get(self.base_url, call_params)
            decoded_response = json.loads(response.text[2:])
            columns = decoded_response['COLUMNS']
            data = decoded_response['DATA']
            appended_data = appended_data + data
        
        #Create pandas DataFrame from the column and data lists
        self.censusDataFrame = pd.DataFrame.from_records(appended_data, columns = columns)
        
        #Provide user feedback whether the call was successfull or not
        if response.status_code == 200:
            print('Successfully received census data')
        elif response.status_code == 404:
            print('Something went wrong during census data retrieaval')
        
        #Extract detailed description of the retrieved data fields for given census topic
        self.data_description = dict(zip(self.censusDataFrame['TEXT_ID'].loc[self.censusDataFrame['INDENT_ID'] >= 0], 
                                         self.censusDataFrame['TEXT_NAME_NOM'].loc[self.censusDataFrame['INDENT_ID'] >= 0]))
            
        return self.censusDataFrame
    
    #Function to print out filed description
    def describe_data(self):
        for field_id, description in self.data_description.items():
            print("--------------------------------------------------------------\n")
            print("Field ID: %5d \n" %field_id)
            print("Field Description: \n")
            print(description)
            print("--------------------------------------------------------------\n")
    
    #Takes field id(s) from data description and returns Pandas DF with only that information for each
    #geographical region
    def field_filter(self, field_ids=None):
        if field_ids is None:
            print('You must input desired field ID(s). Example: fieldfilter(field_ids=[12013,12014])')
 
        else:
            if type(field_ids) == int:
                field_ids = [field_ids]
            filteredDF = self.censusDataFrame.loc[self.censusDataFrame['TEXT_ID'].isin(field_ids)]
            return filteredDF
            
