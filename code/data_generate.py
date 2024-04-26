import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from db_server import db

def generate_data_hour():
    # Generate date range
    date_range = pd.date_range(start="2021-01-01", end="2023-12-31")

    # Public holidays
    public_holidays = {
        "2021-01-01": "New Year's Day","2021-02-12": "Chinese New Year","2021-04-02": "Good Friday","2021-05-01": "Labour Day",
        "2021-05-13": "Hari Raya Puasa","2021-05-26": "Vesak Day","2021-08-09": "National Day","2021-11-04": "Deepavali",
        "2021-12-25": "Christmas Day","2022-01-01": "New Year's Day","2022-02-01": "Chinese New Year","2022-04-15": "Good Friday",
        "2022-05-01": "Labour Day","2022-05-16": "Vesak Day","2022-06-09": "Hari Raya Puasa","2022-08-09": "National Day",
        "2022-10-24": "Deepavali","2022-12-25": "Christmas Day","2023-01-01": "New Year's Day","2023-01-22": "Chinese New Year",
        "2023-04-07": "Good Friday","2023-05-01": "Labour Day","2023-05-30": "Vesak Day","2023-06-22": "Hari Raya Puasa",
        "2023-08-09": "National Day","2023-11-22": "Deepavali","2023-12-25": "Christmas Day"
    }

    # Culturally significant holidays：Chinese New year, Deepavali
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
    num_customers_Chinese = np.where(date_range.weekday < 5,
                            np.random.randint(80, 120, len(date_range)),  # Weekdays
                            np.random.randint(100, 140, len(date_range)))  # Weekends

    # Simulating Customers for Indian Buffet
    np.random.seed(43) # for reproducibility
    num_customers_Indian = np.where(date_range.weekday < 5,
                            np.random.randint(60, 100, len(date_range)),  # Weekdays
                            np.random.randint(80, 120, len(date_range)))  # Weekends

    # Adding public holiday column
    holiday_names = [public_holidays.get(date.strftime("%Y-%m-%d"), "") for date in date_range]

    # Assemble to be a data frame -- the base data frame to work on
    df = pd.DataFrame({
        "Date": date_range,
        "Day": days_of_week,
        "Customers_Chinese": num_customers_Chinese,
        "Customers_India": num_customers_Indian,
        "Public_Holiday": holiday_names
    })

    # add Month column
    df['Month'] = df['Date'].dt.month_name()

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

    # India Reservation:  simulates random reservations for the Indian buffet daily
    np.random.seed(45)
    # Generating random reservations (1 or 0) for each day
    df['India_Reservation'] = np.random.choice([True, False], size=len(df))

    # adjust reservation to be true when there is holiday or promotion
    df.loc[df['Event'] | (df['Public_Holiday'] != ""), 'India_Reservation'] = True

    # adjust the customer for India buffet for reservation (no customer when no reservation)
    df['Customers_India'] = df.apply(lambda row: row['Customers_India'] if row['India_Reservation'] else 0, axis=1)

    # Apply a series of adjustments to ensure the data reflects a realistic pattern.
    
    # Adjusting the customer numbers to be higher on public holidays for both Chinese and Indian customers
    # Define adjustment function to increase customer numbers for holidays
    def adjust_for_holidays(num_customers, dates, increase_factor=1.5): # use a increase factor
        return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in public_holidays else customer
                for customer, date in zip(num_customers, dates)]

    df['Customers_Chinese'] = adjust_for_holidays(df['Customers_Chinese'], df['Date'])
    df['Customers_India'] = adjust_for_holidays(df['Customers_India'], df['Date'])

    # adjust for CN new year and Deepavali (special holidays)
    def adjust_for_chinese_holidays(num_customers, dates, increase_factor=1.5):
        return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in CN_holiday else customer
                for customer, date in zip(num_customers, dates)]

    df['Customers_Chinese'] = adjust_for_chinese_holidays(df['Customers_Chinese'], df['Date'])

    def adjust_for_india_holidays(num_customers, dates, increase_factor=1.5):
        return [int(customer * increase_factor) if date.strftime("%Y-%m-%d") in India_holiday else customer
                for customer, date in zip(num_customers, dates)]

    df['Customers_India'] = adjust_for_india_holidays(df['Customers_India'], df['Date'])

    # adjust for peak month (summer and winter vacation)
    def adjust_for_peak_months(num_customers, dates, increase_factor=1.2):
        return [int(customer * increase_factor) if date.month in [1, 6, 7, 8, 12] else customer
                for customer, date in zip(num_customers, dates)]

    df['Customers_Chinese'] = adjust_for_peak_months(df['Customers_Chinese'], df['Date'])
    df['Customers_India'] = adjust_for_peak_months(df['Customers_India'], df['Date'])

    # adjust for promotion event
    def adjust_customers_for_events(customers, event_flag, increase_factor=1.25):
        return [int(customer * increase_factor) if event else customer for customer, event in zip(customers, event_flag)]

    df['Customers_Chinese'] = adjust_customers_for_events(df['Customers_Chinese'], df['Event'])
    df['Customers_India'] = adjust_customers_for_events(df['Customers_India'], df['Event'])

    # the food court customer and distribution 
    #  follow information from restaurant that food court's customer base closely mirrors that of the Chinese buffet.
    np.random.seed(46)
    random_factors = np.random.uniform(0.75, 1.25, size=len(df))
    df['Food_Court_Customer'] = (df['Customers_Chinese']) * random_factors
    df['Food_Court_Customer'] = df['Food_Court_Customer'].round()
    df['Food_Court_Customer'] = df['Food_Court_Customer'].astype(int)

    # Define the weights for each hour(10 AM to 5PM), with more weight during lunch hours(11 AM to 2 PM)
    weights = np.array([0.5, 1.5, 2, 1.5, 1, 0.5, 1.5])
    # Normalize the weights so they sum to 1
    weights /= weights.sum()
    # Initialize empty lists to hold the generated numbers
    columns = {f"{hour}am-5pm": [] for hour in range(10, 17)}
    # Generate the numbers
    for customer_count in df['Food_Court_Customer']:
        # Distribute the "food court customer" count according to the weights
        distributed_counts = np.floor(customer_count * weights).astype(int)
        
        # Adjust for rounding errors to ensure the sum equals the "food court customer" value
        while distributed_counts.sum() < customer_count:
            distributed_counts[np.random.choice(np.where(weights == weights.max())[0])] += 1
        
        # Append to respective lists
        for i, hour in enumerate(range(10, 17)):
            columns[f"{hour}am-5pm"].append(distributed_counts[i])

    # Add the new columns to the dataframe
    for col_name, col_values in columns.items():
        df[col_name] = col_values
    # rename the column
    new_column_names = {
        '10am-5pm': '10am-11am', '11am-5pm': '11am-12pm', '12am-5pm': '12pm-1pm',
        '13am-5pm': '1pm-2pm', '14am-5pm': '2pm-3pm', '15am-5pm': '3pm-4pm',
        '16am-5pm': '4pm-5pm'
    }
    df= df.rename(columns=new_column_names)
    # the restaurant closes from 5 to 7 PM
    df['5pm-6pm'] = 0
    df['6pm-7pm'] = 0

    # CN buffet start from 7pm
    # Define decreasing weights for the hours from 7pm to 10pm
    def distribute_customers(customers):
        # Randomly distribute the customers with preference to non-even distribution
        while True:
            distribution = np.random.multinomial(customers, [0.5, 0.3, 0.2])
            if len(set(distribution)) == 3:  # Ensure the distribution is not even
                break
        return distribution

    # Apply the distribution function to the 'Customers_Chinese' column
    df[['7pm-8pm', '8pm-9pm_CN', '9pm-10pm_CN']] = df.apply(
        lambda row: distribute_customers(row['Customers_Chinese']), axis=1, result_type='expand'
    )

    # for Indian buffet
    def distribute_customers_india_fixed(customers):
        part_one = round(customers * 0.65)  # 65% for 8PM to 9PM
        part_two = customers - part_one  # Remaining 35% for 9PM to 10PM
        return [part_one, part_two]

    # Re-apply the distribution function with fixed percentages
    df[['8pm-9pm_India', '9pm-10pm_India']] = df.apply(
        lambda row: distribute_customers_india_fixed(row['Customers_India']), axis=1, result_type='expand'
    )

    # Final 8-10 pm col
    df['8pm-9pm'] = df['8pm-9pm_CN'] + df['8pm-9pm_India']
    df['9pm-10pm'] = df['9pm-10pm_CN'] + df['9pm-10pm_India']
    df = df.drop(['8pm-9pm_CN', '9pm-10pm_CN', '8pm-9pm_India','9pm-10pm_India'], axis=1)

    # add cols indicate whether > 100
    df['Chinese > 100'] = df['Customers_Chinese'] > 100
    df['Indian > 100'] = df['Customers_India'] > 100

    # save the file
    engine=db.engine
    df.to_sql('data_with_hour', if_exists='replace',
                con=engine, index=False)


