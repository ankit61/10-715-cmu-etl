import requests
import constants


def get_group_variables(group_name_desc: dict):
    general_link = 'https://api.census.gov/data/2018/acs/acs5/groups.json'

    groups = requests.get(general_link).json()['groups']

    group_vars = {}
    for d in groups:
        if d['name'] in group_name_desc:
            # verify that group_name and group_desc match
            assert \
                d['description'].lower() == group_name_desc[d['name']].lower(),\
                f'{d["name"]} and {group_name_desc[d["name"]]} do not match'

            group_link = f'https://api.census.gov/data/2018/acs/acs5/groups/{d["name"]}.json'
            fields = requests.get(group_link).json()['variables']

            estimate_fields = {}
            for f in fields:
                if f.endswith('E'): # if field is an "estimate"
                    estimate_fields[f] = fields[f]['label']

            group_vars[d['name']] = estimate_fields
    
    return group_vars

def get_raw_data(columns):
    base_url = 'https://api.census.gov/data/2018/acs/acs5'
    data = None
    for c in constants.counties_fips:
        parameters = {
            'for': 'block group:*',
            'in': f'state:{constants.state_fips} county:{c}',
            'get': ','.join(columns),
            'key': constants.key
        }
        if not data:
            data = requests.get(base_url, params=parameters).json()
        else:
            data = requests.get(base_url, params=parameters)[1:]
        print('here')
    return data


