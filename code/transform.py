import pandas as pd
from datetime import datetime
from schedule import *
from sqlalchemy.types import VARCHAR
import sys
sys.path.append('../')
from db_server import db


def calculate_hourly_rate_chef(day, public_holiday):
  if public_holiday:
    return 17
  elif day == 'Saturday' or day == 'Sunday':
      return 16
  else:
      return 15

def calculate_hourly_rate(day, public_holiday):
  if public_holiday:
    return 16
  elif day == 'Saturday' or day == 'Sunday':
    return 15
  else:
    return 14

def calculate_hourly_rate_part(day, public_holiday):
  if public_holiday:
    return 15
  elif day == 'Saturday' or day == 'Sunday':
    return 14
  else:
    return 13
  
def transform_run():
  chefs = ['A1', 'A2', 'A3', 'A4', 'A5']
  service = ['B1', 'B2', 'B3', 'B4', 'B5']
  dishwashers = ['C1', 'C2']
  parttimers = ['D1', 'D2', 'D3']
  schedule_data = []
  chunk_df=pd.read_sql_query('SELECT * FROM predictions', con=db.engine,chunksize=7)
  # chunk_df=pd.read_csv('../output/predictions.csv',chunksize=7)
  for chunk in chunk_df:
    chunk = chunk.reset_index(drop=True)
    final_schedule = smart_Schedule(chunk)

    for idx, row in chunk.iterrows():
      dat = row['Date']
      date = datetime.strptime(dat, '%d/%m/%Y')
      day = row['Day']
      public_holiday = row['Public_Holiday']
      hourly_rate_chef = calculate_hourly_rate_chef(day, public_holiday)
      hourly_rate = calculate_hourly_rate(day, public_holiday)
      hourly_rate_part = calculate_hourly_rate_part(day, public_holiday)

      for employee_id in final_schedule[idx][0]:
        if employee_id in chefs:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Chef', 6.5, hourly_rate_chef, 'full-time'])
        elif employee_id in service:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Service', 6.5, hourly_rate, 'full-time'])
        elif employee_id in parttimers:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Service', 6.5, hourly_rate_part, 'part-time'])
        else:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Dishwasher', 6.5, hourly_rate, 'full-time'])


      for employee_id in final_schedule[idx][1]:
        if employee_id in chefs:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Chef', 3, hourly_rate_chef, 'full-time'])
        elif employee_id in service:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Service', 3, hourly_rate, 'full-time'])
        elif employee_id in parttimers:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Service', 3, hourly_rate_part, 'part-time'])
        else:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Dishwasher', 3, hourly_rate, 'full-time'])


      for employee_id in final_schedule[idx][2]:
        if schedule_data:
          for rw in schedule_data:
            if employee_id in rw and date in rw and rw[4] == '7pm-10pm':
              break
          else:
            if employee_id in chefs:
              schedule_data.append([date, day, public_holiday, employee_id, '8pm-10pm', 'Chef', 2, hourly_rate_chef, 'full-time'])
            elif employee_id in service:
              schedule_data.append([date, day, public_holiday, employee_id, '8pm-10pm', 'Service', 2, hourly_rate, 'full-time'])
            elif employee_id in parttimers:
              schedule_data.append([date, day, public_holiday, employee_id, '8pm-10pm', 'Service', 2, hourly_rate_part, 'part-time'])
            else:
              schedule_data.append([date, day, public_holiday, employee_id, '8pm-10pm', 'Dishwasher', 2, hourly_rate, 'full-time'])

  final_sched = pd.DataFrame(schedule_data, columns=['Date', 'Day', 'Public_Holiday', 'Employee_ID', 'Shift', 'Role', 'Hours_worked', 'Hourly_rate', 'Job_status'])
  final_sched['Date'] = pd.to_datetime(final_sched['Date'], errors='coerce')
  final_sched = final_sched.sort_values(by=['Date', 'Shift', 'Employee_ID'])
  final_sched.dropna(subset=['Date'], inplace=True)
  # final_sched.to_csv('final_schedule.csv', index=False)
  engine=db.engine
  final_sched.to_sql('final_schedule', if_exists='replace',
                con=engine, index=False,dtype={'Date': VARCHAR(50)})
  
# transform_run()
