import logging
import constants
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from data_extractor import *
import json
import psycopg2 as ps
import io


class SQLWriter():
    def __init__(self):
        config = json.load(open(constants.db_config_path, 'r'))

        self.host = config['host']
        self.dbname = config['dbname']
        self.user = config['user']

    def write_to_sql(self, data):
        '''
            the main function of the class responsible for creating a SQL file
            with statements to create the schema and table, annotate the columns
            and copy the data from a CSV file.
        '''
        schema_stmt = self.gen_schema_stmt()
        create_stmt = self.gen_create_table_stmt(data)

        cols = get_estimate_columns(data)

        col_comments = \
            {c: comment for c, comment in zip(cols, get_column_descs(cols))}

        comments_stmt = self.gen_column_comments_stmts(col_comments)

        stmts = [
            schema_stmt,
            create_stmt,
            comments_stmt,
        ]

        conn = ps.connect(host=self.host, dbname=self.dbname, user=self.user)
        with conn:
            with conn.cursor() as curs:
                for s in stmts:
                    curs.execute(s)

                curs.copy_from(
                    self.get_data_buf(data),
                    f'{constants.schema_name}.{constants.table_name}',
                    sep=','
                )

        conn.close()

    def gen_schema_stmt(self, schema_name=constants.schema_name):
        '''
            returns the CREATE SCHEMA statement
        '''
        return f'CREATE SCHEMA IF NOT EXISTS {schema_name};'

    def gen_create_table_stmt(self, data, table_name=constants.table_name, schema_name=constants.schema_name):
        '''
            returns the CREATE TABLE statement
        '''
        types_dict = {
            'float64': 'DECIMAL',
            'object': 'VARCHAR',
            'int64': 'DECIMAL'
        }
        nl = '\n'
        tc = '\t'
        cols = [
            c.lower().replace(" ", "_") + " " + types_dict[str(data[c].dtype)]
            for c in data.columns
        ]
        return \
            f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (\n\t' + \
                f'{f",{nl + tc}".join(cols)}' + \
            '\n);'

    def gen_column_comments_stmts(self, col_descs: dict, table_name=constants.table_name,
        schema_name=constants.schema_name
    ):
        '''
            returns SQL statements that annotate the columns of the table
        '''
        comments = []
        for k, v in col_descs.items():
            comm = v.replace('\'','')
            comments.append(f"COMMENT ON COLUMN {schema_name}.{table_name}.{k} IS '{comm}';")

        return '\n'.join(comments)

    def get_data_buf(self, data):
        '''
            returns a buffer with dataframe loaded as csv
        '''
        f_buf = io.StringIO()
        data.to_csv(f_buf, index=False, header=False)
        f_buf.seek(0)

        return f_buf

