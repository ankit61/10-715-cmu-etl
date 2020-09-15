# 10-715-cmu-etl
Code for ETL Assignment for 10-715 at CMU

### Instructions to run

There are two steps to load data into the PostgreSQL database: 

1. Generate a SQL file to create the schema and table, and load data into it 
2. Execute the SQL file using PostgresSQL

The following lines can be executed in the terminal to do both:

```bash
source /data/groups/schools3/dssg_env/bin/activate  # activate the relevant venv
python main.py # will generate a create.sql file in the current working directory
psql -h mlpolicylab.db.dssg.io -U {YOUR_ANDREW_ID} schools3_database -f create.sql # to execute the sql file
```

### Table Information

The table is located in the `schools3` database and `etl_ankit` schema with name `family_influence` (`Object ID: 2698042`). It has 41 columns and 9238 rows. The column names resemble those that are found on the [ACS website](https://api.census.gov/data/2018/acs/acs5/variables.html). However, since the column names are not that descriptive, each column has a comment containing longer descriptions.


### Code Generalizability & Modularity
