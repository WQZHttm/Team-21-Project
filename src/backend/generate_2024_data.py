import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from db_server import db

def generate_general_data():
    # Generate date range
    date_range = pd.date_range(start="2024-01-01", end="2025-01-05")

    public_holidays = {
        "2024-01-01": "New Year's Day",
        "2024-02-10": "Chinese New Year",
        "2024-02-11": "Chinese New Year",
        "2024-02-12": "Chinese New Year",
        "2024-03-29": "Good Friday",
        "2024-04-10": "Hari Raya Puasa",
        "2024-05-01": "Labour Day",
        "2024-05-22": "Vesak Day",
        "2024-06-17": "Hari Raya Haji",
        "2024-08-09": "National Day",
        "2024-10-31": "Deepavali",
        "2024-12-25": "Christmas Day",
        "2025-01-01": "New Year's Day",
    }

    # Day of the week column
    days_of_week = date_range.day_name()

    # Adding public holiday column
    holiday_names = [public_holidays.get(date.strftime("%Y-%m-%d"), "") for date in date_range]

    df = pd.DataFrame({
        "Date": date_range,
        "Day": days_of_week,
        "Public_Holiday": holiday_names
    })

    # add Month column
    df['Month'] = df['Date'].dt.month_name()

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

    # India Reservation
    np.random.seed(45)
    # Generating random reservations (1 or 0) for each day
    df['India_Reservation'] = np.random.choice([True, False], size=len(df))

    # adjust reservation to be true when there is holiday or promotion
    # on holiday and events, I assume that there must be India reservation
    df.loc[df['Event'] | (df['Public_Holiday'] != ""), 'India_Reservation'] = True

    engine=db.engine
    df.to_sql('general_data', if_exists='replace',
                con=engine, index=False)
