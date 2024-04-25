


from time import sleep,monotonic
import pandas as pd
import sys
import datetime

def backend_run():
    print(datetime.datetime.now())
    print('START OF BACKEND_RUN')

    # 1. generate data from decision tree model
    sys.path.append('./code')
    from data_generate import generate_data_hour
    generate_data_hour()
    start = monotonic()
    print (monotonic() - start)
    sleep(100)
    from generate_2024_data import generate_general_data
    generate_general_data()
    sleep(120) 
    # 2. Predict customer demand
    
    
    from decision_tree_model import predict
    predict()
    sleep(120)
    # 3. get optimised schedule
    from transform import transform_run   
    transform_run()
    sleep(120)
    print(datetime.datetime.now())
    print('END OF BACKEND_RUN')
    


backend_run()