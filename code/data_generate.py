import csv
import pandas as pd
import numpy as np

# Generate date range
date_range = pd.date_range(start="2021-01-01", end="2023-12-31")

# Public holidays
public_holidays = {
    "2021-01-01": "New Year's Day",
    "2021-02-12": "Chinese New Year",
    "2021-04-02": "Good Friday",
    "2021-05-01": "Labour Day",
    "2021-05-13": "Hari Raya Puasa",
    "2021-05-26": "Vesak Day",
    "2021-08-09": "National Day",
    "2021-11-04": "Deepavali",
    "2021-12-25": "Christmas Day",
    "2022-01-01": "New Year's Day",
    "2022-02-01": "Chinese New Year",
    "2022-04-15": "Good Friday",
    "2022-05-01": "Labour Day",
    "2022-05-16": "Vesak Day",
    "2022-06-09": "Hari Raya Puasa",
    "2022-08-09": "National Day",
    "2022-10-24": "Deepavali",
    "2022-12-25": "Christmas Day",
    "2023-01-01": "New Year's Day",
    "2023-01-22": "Chinese New Year",
    "2023-04-07": "Good Friday",
    "2023-05-01": "Labour Day",
    "2023-05-30": "Vesak Day",
    "2023-06-22": "Hari Raya Puasa",
    "2023-08-09": "National Day",
    "2023-11-22": "Deepavali",
    "2023-12-25": "Christmas Day"
}

# On Chinese New year, more people for CN buffet, same for Deepavali
CN_holiday = {
    "2021-02-12": "Chinese New Year",
    "2022-02-01": "Chinese New Year",
    "2023-01-22": "Chinese New Year"
}

India_holiday = {
    "2021-11-04": "Deepavali",
    "2022-10-24": "Deepavali",
    "2023-11-22": "Deepavali"
}

# Day of the week column
days_of_week = date_range.day_name()

# Number of customers
# Simulating Customers for Chinese Buffet
np.random.seed(42)  # for reproducibility
num_customers_CN = np.where(date_range.weekday < 5,
                         np.random.randint(80, 120, len(date_range)),  # Weekdays
                         np.random.randint(100, 150, len(date_range)))  # Weekends

# Simulating Customers for Indian Buffet
np.random.seed(43) # for reproducibility
num_customers_India = np.where(date_range.weekday < 5,
                         np.random.randint(60, 100, len(date_range)),  # Weekdays
                         np.random.randint(80, 120, len(date_range)))  # Weekends

# Adding public holiday column
holiday_names = [public_holidays.get(date.strftime("%Y-%m-%d"), "") for date in date_range]

# Assemble to be a data frame 
df = pd.DataFrame({
    "Date": date_range,
    "Day": days_of_week,
    "Customers_Chinese": num_customers_CN,
    "Customers_India": num_customers_India,
    "Public_Holiday": holiday_names
})

# add Month column
df['Month'] = df['Date'].dt.month_name()

# Adjusting the customer numbers to be higher on public holidays for both Chinese and Indian customers

# Define adjustment function to increase customer numbers for holidays
def adjust_for_holidays(num_customers, dates, increase_factor=1.5): # use a increase factor
    return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in public_holidays else customer
            for customer, date in zip(num_customers, dates)]

df['Customers_Chinese'] = adjust_for_holidays(df['Customers_Chinese'], df['Date'])
df['Customers_India'] = adjust_for_holidays(df['Customers_India'], df['Date'])

# adjust for CN new year and Deepavali
def adjust_for_chinese_holidays(num_customers, dates, increase_factor=1.5):
    return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in CN_holiday else customer
            for customer, date in zip(num_customers, dates)]

df['Customers_Chinese'] = adjust_for_chinese_holidays(df['Customers_Chinese'], df['Date'])

def adjust_for_india_holidays(num_customers, dates, increase_factor=1.5):
    return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in India_holiday else customer
            for customer, date in zip(num_customers, dates)]

df['Customers_India'] = adjust_for_india_holidays(df['Customers_India'], df['Date'])

# adjust for peak month (summer vacation)
def adjust_for_summer_months(num_customers, dates, increase_factor=1.2):
    return [int(customer * increase_factor) if date.month in [6, 7, 8] else customer
            for customer, date in zip(num_customers, dates)]

df['Customers_Chinese'] = adjust_for_summer_months(df['Customers_Chinese'], df['Date'])
df['Customers_India'] = adjust_for_summer_months(df['Customers_India'], df['Date'])

# Adding an "Event" column to indicate days with a promotion, happening 3 times a month randomly
# randomly select 3 days in each month for the promotion
def assign_promotions(dates):
    unique_months = dates.dt.to_period('M').unique()
    promotion_days = []

    for month in unique_months:
        month_days = dates[dates.dt.to_period('M') == month]
        promotions = np.random.choice(month_days, size=min(3, len(month_days)), replace=False)
        promotion_days.extend(promotions)

    return dates.isin(promotion_days)

# Apply the function to assign promotions
df['Event'] = assign_promotions(df['Date'])

# adjust for promotion
def adjust_customers_for_events(customers, event_flag, increase_factor=1.25):
    return [int(customer * increase_factor) if event else customer for customer, event in zip(customers, event_flag)]

df['Customers_Chinese'] = adjust_customers_for_events(df['Customers_Chinese'], df['Event'])
df['Customers_India'] = adjust_customers_for_events(df['Customers_India'], df['Event'])

# India Reservation
np.random.seed(45)
# Generating random reservations (1 or 0) for each day
df['India_Reservation'] = np.random.choice([True, False], size=len(df))

# adjust reservation to be true when there is holiday or promotion
# on holiday and events, I assume that there must be India reservation
df.loc[df['Event'] | (df['Public_Holiday'] != ""), 'India_Reservation'] = True

# adjust the customer for India buffet
df['Customers_India'] = df.apply(lambda row: row['Customers_India'] if row['India_Reservation'] else 0, axis=1)
print(df.sample(10))  # Display a random sample to see the distribution

# add cols indicate whether > 100
df['Chinese > 100'] = df['Customers_Chinese'] > 100
df['Indian > 100'] = df['Customers_India'] > 100

# save the file

df.to_csv('../input/data.csv', index = False)

