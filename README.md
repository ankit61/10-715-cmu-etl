# 10-715-cmu-etl
Code for ETL Assignment for 10-715 at CMU

### Instructions to run

The instructions are contained in the PDF document submitted on canvas. As explained there, running `python main.py` will generate a .sql file and .csv file (if not already present). Executing the .sql file with psql will create the actual table in PostgreSQL. To show the output of these generated files, they have also been uploaded to this repository.

### Table Information

The table is located in the `schools3` database and `etl_ankit` schema with name `schools_external_factors`. It has 52 columns and 9238 rows. The column names resemble those that are found on the [ACS website](https://api.census.gov/data/2018/acs/acs5/variables.html). However, since the column names are not that descriptive, each column has a comment containing longer descriptions.


### Code Flexiblity & Modularity

The code has been written in a highly flexible manner to aid in its incorporation in the final project. All parameters/constants in the code are stored in a separate file named constants.py. The state, the granularity level, the year of survey, and the variables of interest can all be very easily changed in the constants.py file.

Further, the code is also very modular, and has a clear separation between the part that does the extraction of data and the part that does the creation of the SQL file.
