from transform import transform_run
from decision_tree_model import predict

def backend_run():
    # 1. generate data from decision tree model
    predict()
    # 2. get optimised schedule   
    transform_run()



