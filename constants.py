import requests
import numpy as np



def get_counties():
    base_url = f'https://api.census.gov/data/{year}/acs/acs5'
    params = {
        'get': 'NAME',
        'for': 'county:*',
        'in' : f'state:{state_fips}',
        'key': key
    }

    counties = np.array(
        requests.get(base_url, params=params).json()[1:]
    )

    return counties[:, 2], counties[:, 0]


# important params
state_fips      = 39
for_param       = 'block group:*'
year            = 2018
group_name_desc = {
    'B11016': 'HOUSEHOLD TYPE BY HOUSEHOLD SIZE',
    'B15003': 'EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER',
    'B23025': 'EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER'
}


# data extractor params
key     = '184fc9798e379fa4bb145284a3c6f3f8e5ff7fb2'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
}

get_in_param = lambda state, county: f'state:{state} county:{county}'

counties_fips, county_names = get_counties()

all_variables_link  = f'https://api.census.gov/data/{year}/acs/acs5/variables.json'
groups_link         = f'https://api.census.gov/data/{year}/acs/acs5/groups.json'
get_group_vars_link = lambda group: f'https://api.census.gov/data/{year}/acs/acs5/groups/{group}.json'
raw_data_base_link  = f'https://api.census.gov/data/{year}/acs/acs5'

# sql params
sql_file = 'generated/create.sql'
schema_name = 'etl_ankit'
table_name = 'schools_external_factors'
db_config_path = 'db_config.json'

