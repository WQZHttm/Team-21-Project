from data_generate import generate_data_hour
from generate_2024_data import generate_general_data
from transform import transform_run
from decision_tree_model import predict
from time import sleep

def backend_run():
    print('START OF BACKEND_RUN')
    # 1. generate data from decision tree model
    generate_data_hour()
    generate_general_data()
    sleep(120) 
    # 2. Predict customer demand
    predict()
    sleep(120)
    # 3. get optimised schedule   
    transform_run()
    print('END OF BACKEND_RUN')

# backend_run()