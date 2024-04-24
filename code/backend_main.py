from data_generate import generate_data_hour
from generate_2024_data import generate_general_data
from transform import transform_run
from decision_tree_model import predict
from time import sleep,monotonic
import sys
sys.path.append('../')
from db_server import db
import pandas as pd


def backend_run():
    print('START OF BACKEND_RUN')
    print(pd.read_sql_query('SELECT DATABASE()', con=db.engine))
    print(pd.read_sql_query("SHOW TABLES LIKE 'team21_v1_general_data'", con=db.engine))
    # 1. generate data from decision tree model
    generate_data_hour()
    start = monotonic()
    print (monotonic() - start)
    sleep(100)
    generate_general_data()
    sleep(120) 
    # 2. Predict customer demand
    predict()
    sleep(120)
    # 3. get optimised schedule   
    transform_run()
    print('END OF BACKEND_RUN')

# backend_run()