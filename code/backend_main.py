# import sys
# sys.path.append('.')
#from schedule import *
from decision_tree_model import *

df = pd.read_csv('../input/data_with_hour.csv')
data2024 = pd.read_csv('../input/test.csv')

# stuff = DecisionTree()