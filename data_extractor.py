import re
import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
import constants


def get_prefix(name):
    '''
        helper function to simply get the prefix of a variable name
    '''
    split = name.split('!!')
    return '!!'.join(split[:-1])


def get_column_descs(columns):
    '''
        helper function to get descriptions of given abbreviated column names
    '''
    column_name_url = constants.all_variables_link
    d = requests.get(column_name_url, headers=constants.headers).json()['variables']
    return [d[c]['concept'].title() + ' | ' + re.sub('!!', ' | ', d[c]['label']) for c in columns]


def get_estimate_columns(data):
    '''
        helper function to get column names of all fields that are numeric
        and contain quantitive data
    '''
    return data.columns[:-4]


class DataExtractor():
    def extract(self, group_name_desc=None, percent_form=True):
        '''
            main function of the class to extract all data from ACS APIs in
            either percent format or raw format given the variable groups of
            interest
        '''
        if group_name_desc is None:
            group_name_desc = constants.group_name_desc

        group_vars = self.get_group_variables(group_name_desc)

        cols = [c for k in group_vars for c in group_vars[k]]

        data = self.get_raw_data(cols)
        if percent_form:
            data = self.get_percent_form(data, group_vars)

        return data

    def get_group_variables(self, group_name_desc: dict):
        '''
            given group variables, the function returns names of all individual
            estimate variables which will be used to query APIs later
        '''
        groups_link = constants.groups_link

        groups = requests.get(groups_link).json()['groups']

        group_vars = {}
        for d in groups:
            if d['name'] in group_name_desc:
                # verify that group_name and group_desc match
                assert \
                    d['description'].lower() == group_name_desc[d['name']].lower(),\
                    f'{d["name"]} and {group_name_desc[d["name"]]} do not match'

                group_vars_link = constants.get_group_vars_link(d['name'])
                fields = requests.get(group_vars_link).json()['variables']

                estimate_fields = {}
                for f in fields:
                    if f.endswith('E'): # if field is an "estimate"
                        estimate_fields[f] = fields[f]['label']

                group_vars[d['name']] = estimate_fields

        return group_vars

    def get_raw_data(self, columns):
        '''
            given column names, query APIs to return raw data in pandas
            dataframe style
        '''
        base_url = constants.raw_data_base_link
        data = None
        for c in tqdm(constants.counties_fips):
            parameters = {
                'for': constants.for_param,
                'in': constants.get_in_param(constants.state_fips, c),
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

        return df

    def get_percent_form(self, data, group_vars):
        '''
            given raw data and variables with their column descriptions, convert
            raw population counts into percentages
        '''
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
