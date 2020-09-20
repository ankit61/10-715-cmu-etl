# 10-718-cmu-etl
Code for ETL Assignment for 10-718 at CMU

### Instructions to run

The instructions are contained in the PDF document submitted on canvas.

### Table Information

The table is located in the `schools3_database` database and `etl_ankit` schema with name `schools_external_factors`. It has 52 columns and 9238 rows. The column names resemble those that are found on the [ACS website](https://api.census.gov/data/2018/acs/acs5/variables.html). However, since the column names are not that descriptive, each column has a comment containing longer descriptions.


### Code Flexiblity & Modularity

The code has been written in a highly flexible manner to aid in its incorporation in the final project. All parameters/constants in the code are stored in a separate file named constants.py. The state, the granularity level, the year of survey, and the variables of interest can all be very easily changed in the constants.py file.

Further, the code is also very modular, and has a clear separation between the part that does the extraction of data and the part that does the creation of PostgreSQL table.

### Transforming Variables

All variables we chose from the 5-year ACS survey API are only available in the form of raw counts. Consequently, all raw counts are going to be strongly correlated to the population in the block, which is undesirable. Therefore, we convert the estimates obtained from the ACS API to percentage estimates by dividing each field by the total sample size. Further, since estimates from ACS survey may not be fully accurate, it is likely that attributes that occur very rarely in the population are highly underestimated. Therefore, to prevent underrepresented attributes from being more underrepresented in the data, we use [Laplace smoothing](https://en.wikipedia.org/wiki/Additive_smoothing). We basically just add 1 to the most specific/granular fields in the data and also accordingly adjust the total sample size. This technique ensures that highly underrepresented groups do not show up as occuring with 0% probability.
