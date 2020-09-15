import requests
import constants
import re
from tqdm import tqdm
import numpy as np
import pandas as pd


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
    for c in tqdm(constants.counties_fips):
        parameters = {
            'for': 'block group:*',
            'in': f'state:{constants.state_fips} county:{c}',
            'get': ','.join(columns),
            'key': constants.key
        }
        if not data:
            data = requests.get(base_url, params=parameters).json()
        else:
            data += requests.get(base_url, params=parameters).json()[1:]
    
    df = pd.DataFrame(data[1:], columns=data[0])
    for c in columns:
        df[c] = df[c].astype(np.float)

    #df = df.rename({c: nc for c, nc in zip(columns, get_column_names(columns))}, axis=1)
    return df


def get_prefix(name):
    split = name.split('!!')
    return '!!'.join(split[:-1])


def get_percent_form(data, group_vars):
    for g in group_vars:
        links = {}
        labels = {}
        num_pointing = {}

        for k, name in group_vars[g].items():
            prefix = get_prefix(name)
            links[name] = prefix
            labels[name] = k

            if prefix in num_pointing:
                num_pointing[prefix] += 1
            else:
                num_pointing[prefix] = 1

        for k in sorted(links, key=lambda x: -len(x.split('!!'))):
            prefix = links[k]
            if prefix in links:
                smoothed_denom = data[labels[prefix]] + num_pointing[prefix]
                smoothed_numer = data[labels[k]] + 1

                data[labels[k]] = smoothed_numer / smoothed_denom

    return data


def get_column_names(columns):
    column_name_url = 'https://api.census.gov/data/2018/acs/acs5/variables.json'
    d = requests.get(column_name_url, headers=constants.headers).json()['variables']
    return [d[c]['concept'].title() + ' | ' + re.sub('!!', ' | ', d[c]['label']) for c in columns]


def write_to_csv(data, filename):
    pass


def write_to_postgres(csv_filename):
    pass
