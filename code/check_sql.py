import sys
sys.path.append('../')
from main import db
import pandas as pd
df2 = pd.read_sql_query('SELECT * FROM final_schedule', con=db.engine)
print(df2.dtypes)
manpower_schedule = pd.read_csv('../output/final_schedule.csv')

print('csv',manpower_schedule.dtypes)