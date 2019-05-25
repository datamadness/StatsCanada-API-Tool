# StatsCanada-API-Tool
A Python tool to access to wide range of 2016 Census socioeconomic data through Statistics Canada API.

## Features
To make the access to the data easier, this python tool automates the gory details on your behalf. It allows you to call the Statistics Canada API and retrieve any data for any region in just couple lines of code. Moreover, you can receive combined data from arbitrary number of regions at once. To top it off, the data is returned in pandas DataFrame format for an easy post-processing.

## More detailed documentation and example is available here:
https://datamadness.github.io/StatsCanada-Tool-Census

## region_slicer class
The census data is mapped to the country's regions and geographical locations. The region_slicer class serves for fetching the geo location data that will later allow you to retrieve the actual census data for the regions of your interest. 

*region_slicer(geo_level = str, province = str)*

**geo_level**: *str, default = 'POPCNTR'*. This parameter defines how to subdivide the province/territory or the country. This can be bases on population centers, voting regions, economic regions and many other.

*regions_slicer.geo_levels* 

lists all available geo_level values with description

**province**: *str, default = '00'*. This parameter defines which province or territory data to fetch. Default '00' is for all of Canada.

*regions_slicer.provincial_codes* 

lists all available province codes with description

*region_slicer.get_data()*

Object method that calls the API and receives the geo data per the parameters stored in the region_slicer object.
Returns: pandas DataFrame 


## census_data class

This class takes an region_slicer object and returns the actual census data for all regions included in the region_slicer as one pandas DataFrame. DataFrames from region_slicer and census_data can be joined 'GEO_ID' primary key.

*census_data(geo_uids = region_slicer, topic = int)*

**geo_uids**: *region_slicer object or str or list of str, default = '2016A000011124'*. Value that specifies all geo_uids for which to fetch the census data

**topic**: *int, default = 7*. Specifies census topic of interest. For example Education, Labour, Income, Housing and so on.

*census_data.topics* 

lists all available census topic values with description

*census_data.get_data()*

Object method that calls the API and receives the geo data per the parameters stored in the census_data object.
Returns: pandas DataFrame

*census_data.data_description* 

stores the description of all fetched data and their field_ids under given census topic

*census_data.describe_data()*

Object method that prints the description of all unique data fields stored in the census_data object and corresponding field_id

*census_data.field_filter(field_ids=None)*

**field_ids**: *str or list of str, default = None*. Filters census data for specific field ID(s). Returns pandas DataFrame containing only the data defined by the field_ids. For example, it can filter out Average income per region from income census data.
Returns: pandas DataFrame
