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

### Database Location

