import requests
import numpy as np

key = '184fc9798e379fa4bb145284a3c6f3f8e5ff7fb2'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
}
state_fips = 39

def get_counties():
    base_url = 'https://api.census.gov/data/2018/acs/acs5'
    params = {
        'get': 'NAME',
        'for': 'county:*',
        'key': key
    }

    counties = np.array(
                    requests.get(base_url, params=params).json()[0:]
                )

    return  counties[:, 1], counties[:, 0]

counties_fips, county_names = get_counties()
