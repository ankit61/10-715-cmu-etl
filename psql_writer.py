import constants
import os
from stat import S_IREAD, S_IGRP, S_IROTH
from data_extractor import get_column_names, get_estimate_columns


class SQLWriter():
    def write(self, data, out_file=constants.sql_file):
        if os.path.exists(out_file):
            raise ValueError(f'{out_file} already exists!')

        with open(out_file, 'w') as f:

            schema_stmt = self.gen_schema_stmt()
            create_stmt = self.gen_create_table_stmt(data)

            cols = get_column_names(data)

            col_comments = \
                {c: comment for c, comment in zip(cols, get_column_names(cols))}

            comments_stmt = self.gen_column_comments_stmts(col_comments)
            copy_stmt = self.gen_copy_stmt(data)

            stmts = [
                schema_stmt,
                create_stmt,
                comments_stmt,
                copy_stmt
            ]

            for s in stmts:
                f.write(s)
                f.write('\n\n')


        os.chmod(out_file, S_IREAD|S_IGRP|S_IROTH)


    def gen_schema_stmt(self, schema_name=constants.schema_name):
        return f'CREATE SCHEMA IF NOT EXISTS {schema_name}'


    def gen_create_table_stmt(self, data, table_name=constants.table_name):
        types_dict = {
            'float64': 'DECIMAL',
            'object': 'VARCHAR'
        }
        nl = '\n'
        cols = [
            c.lower().replace(" ", "_") + " " + types_dict[str(data[c].dtype)]
            for c in data.columns
        ]
        return \
            f'CREATE TABLE IF NOT EXISTS {table_name} (\n' + \
                f'{f",{nl}".join(cols)}' + \
            '\n)'


    def gen_column_comments_stmts(self, col_descs: dict, table_name=constants.table_name):
        comments = []
        for k, v in col_descs.items():
            comments.append(f'COMMENT ON COLUMN {table_name}.{k} IS {v}')

        return '\n'.join(comments)


    def gen_copy_stmt(self, data, table_name=constants.table_name):
        if not os.path.exists(constants.csv_path):
            data.to_csv(constants.csv_path, index=False)

        return f"\\COPY {table_name} FROM '{constants.csv_path}' WITH CSV HEADER"
