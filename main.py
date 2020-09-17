from data_extractor import *
from psql_writer import *

if __name__ == '__main__':
    data = DataExtractor().extract()
    SQLWriter().write_to_sql(data)
