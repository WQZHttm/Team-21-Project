import pandas as pd
customer_prediction = pd.read_csv('output/predictions.csv')
manpower_schedule = pd.read_csv('output/final_schedule.csv')

# DAY

manpower_schedule ['Date_and_day'] = manpower_schedule['Date'] + ' ' + manpower_schedule['Day']
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d')

# WEEK

customer_prediction ['Date_and_day'] = customer_prediction['Date'] + ' ' + customer_prediction['Day']
customer_prediction['Date'] = pd.to_datetime(customer_prediction['Date'], format='%d/%m/%Y')

customer_prediction['Public_Holiday'] = customer_prediction['Public_Holiday'].fillna('')


# LCP
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']
manpower_schedule['Total Paid'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

