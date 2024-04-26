#import necessary packages, including schedule to import the mathematical model algorithm for a week's schedule
import pandas as pd
from datetime import datetime
from schedule import *
from sqlalchemy.types import VARCHAR
import sys
sys.path.append('../')
from db_server import db

pub_hols = ["New Year's Day", "Chinese New Year", "Good Friday", "Hari Raya Puasa", "Labor Day", "Vesak Day", "Hari Raya Haji", "National Day", "Deepavali", "Christmas Day"]

#calculate_hourly_rate_xxx functions will help to determine the hourly pay for each worker since the pays change according to different roles, job statuses, whether it is a public holiday, and type of day
def calculate_hourly_rate_chef(day, public_holiday):
  if public_holiday in pub_hols:
    return 17
  elif day == 'Saturday' or day == 'Sunday':
      return 16
  else:
      return 15

def calculate_hourly_rate(day, public_holiday):
  if public_holiday in pub_hols:
    return 16
  elif day == 'Saturday' or day == 'Sunday':
    return 15
  else:
    return 14

def calculate_hourly_rate_part(day, public_holiday):
  if public_holiday in pub_hols:
    return 15
  elif day == 'Saturday' or day == 'Sunday':
    return 14
  else:
    return 13
  
def transform_run():

  #create lists of all the current workers available in the restaurant. should there be more workers, these lists will need to be amended
  chefs = ['A1', 'A2', 'A3', 'A4', 'A5']
  service = ['B1', 'B2', 'B3', 'B4', 'B5']
  dishwashers = ['C1', 'C2']
  parttimers = ['D1', 'D2', 'D3']

  #this will contain the schedules for every day of the year at the end
  schedule_data = []
  chunk_df=pd.read_sql_query('SELECT * FROM predictions', con=db.engine,chunksize=7)

  #we will begin by reading in the predictions.csv file containing the customer predictions in chunks of 7. this is to ensure that in every iteration we are optimizing over exactly 7 days of the week
  for chunk in chunk_df:
    chunk = chunk.reset_index(drop=True)

    #smart_Schedule() is the function we have imported from the schedule package. final_schedule is the optimized schedule generated for every unique 7 day chunk
    final_schedule = smart_Schedule(chunk)
    for idx, row in chunk.iterrows():

      #we will extract the day, date, and public holiday (if applicable) from the chunk
      dat = row['Date']
      date = datetime.strptime(dat, '%d/%m/%Y')
      day = row['Day']
      public_holiday = row['Public_Holiday']
      Indian_R = row['India_Reservation']

      #next, we apply the hourly_rate_xxx helper functions from earlier
      hourly_rate_chef = calculate_hourly_rate_chef(day, public_holiday)
      hourly_rate = calculate_hourly_rate(day, public_holiday)
      hourly_rate_part = calculate_hourly_rate_part(day, public_holiday)

      #in the following sections, we will be compiling the necessary information from the chunk and employee-specific information, and then appending this list to schedule_data
      #final_schedule[idx][0] refers the the lunch hour shift in this particular chunk
      for employee_id in final_schedule[idx][0]:
        if employee_id in chefs:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Chef', 6.5, hourly_rate_chef, 'full-time'])
        elif employee_id in service:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Service', 6.5, hourly_rate, 'full-time'])
        elif employee_id in parttimers:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Service', 6.5, hourly_rate_part, 'part-time'])
        else:
          schedule_data.append([date, day, public_holiday, employee_id, '10am-4.30pm', 'Dishwasher', 6.5, hourly_rate, 'full-time'])

      #final_schedule[idx][1] refers the the Chinese buffet shift in this particular chunk
      for employee_id in final_schedule[idx][1]:
        if employee_id in chefs:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Chef', 3, hourly_rate_chef, 'full-time'])
        elif employee_id in service:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Service', 3, hourly_rate, 'full-time'])
        elif employee_id in parttimers:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Service', 3, hourly_rate_part, 'part-time'])
        else:
          schedule_data.append([date, day, public_holiday, employee_id, '7pm-10pm', 'Dishwasher', 3, hourly_rate, 'full-time'])

      #final_schedule[idx][2] refers the the Indian shift in this particular chunk
      #there are various circumstances to check for given the fact that we should not repeat workers who are already working in the Chinese buffet. We also need to make sure no workers are assigned on days that there is no Indian Reservation at all
      for employee_id in final_schedule[idx][2]:
        if Indian_R:
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

  #schedule_data now contains all the relevant information. final_sched is a dataframe that contains the necessary information according to the following column names
  final_sched = pd.DataFrame(schedule_data, columns=['Date', 'Day', 'Public_Holiday', 'Employee_ID', 'Shift', 'Role', 'Hours_worked', 'Hourly_rate', 'Job_status'])

  #this step is to ensure that small bugs like confusing between 1/2/24 and 2/1/24 do not occur
  final_sched['Date'] = pd.to_datetime(final_sched['Date'], errors='coerce')

  #this step makes the dataframe more organised by sorting it according to date, shift and employee
  final_sched = final_sched.sort_values(by=['Date', 'Shift', 'Employee_ID'])
  final_sched.dropna(subset=['Date'], inplace=True)
  engine=db.engine

  #final_sched is coverted from a dataframe to a readable sql file
  final_sched.to_sql('final_schedule', if_exists='replace',
                con=engine, index=False,dtype={'Date': VARCHAR(50)})
  
# transform_run()