import pandas as pd
import sys

# import database
from db_server import db

# read data from database
manpower_schedule = pd.read_sql_query('SELECT * FROM final_schedule', con=db.engine)
customer_prediction = pd.read_sql_query('SELECT * FROM predictions', con=db.engine)


# AMEND DATA FOR THE FOLLOWING PAGES:
# DAY
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d %H:%M:%S')
manpower_schedule['Day'] = manpower_schedule['Day'].astype(str)
manpower_schedule['Date_and_day'] = manpower_schedule['Date'].dt.strftime('%Y-%m-%d') + ' ' + manpower_schedule['Day']

# WEEK
customer_prediction ['Date_and_day'] = customer_prediction['Date'] + ' ' + customer_prediction['Day']
customer_prediction['Date'] = pd.to_datetime(customer_prediction['Date'], format='%d/%m/%Y')
customer_prediction['Public_Holiday'] = customer_prediction['Public_Holiday'].fillna('')


# LCP
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']
manpower_schedule['Total Paid'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

