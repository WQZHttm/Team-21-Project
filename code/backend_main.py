# import sys
# sys.path.append('.')
from schedule import *
from decision_tree_model import *

df = pd.read_csv('../input/data_with_hour.csv')
data2024 = pd.read_csv('../input/test.csv')

stuff = DecisionTree(df, data2024)
#Finally = smart_Schedule(stuff)

stuff = {'Date': ['John', 'Anna', 'Peter', 'Linda'],
        'Day': [28, 35, 25, 42],
        'City': ['New York', 'Paris', 'London', 'Tokyo']}

### Finally is a dataframe already in the desired format, that needs to be sent to database