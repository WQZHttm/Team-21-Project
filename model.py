import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt

# read in data, here I use the first store's data
df = pd.read_csv("air_visit_data.csv" ,parse_dates=True, index_col='visit_date') # use date as index column
print(df.head()) # print first few rows to check

# plot

"""
df.plot()
plt.show()
"""

# check for stationarity
from statsmodels.tsa.stattools import adfuller

result = adfuller(df["visitors"])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1]) # the p-value is 0.092878

# Select ARIMA parameters
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# plot ACF
"""
plt.figure(figsize=(10,6))
plot_acf(df['visitors'], ax=plt.gca())
plt.show()
"""
# plot PACF
"""
plt.figure(figsize=(10,6))
plot_pacf(df['visitors'], ax=plt.gca())
plt.show()
"""
# q = 1, p = 1 or 2 (well the prediction result looks weird with this p, so I set it to 7)

# fit the model
model_arima = ARIMA(df['visitors'], order = (7, 1, 1)) # p, d, q
model_fit = model_arima.fit()

predictions = model_fit.forecast(steps = 5) # number of predictions (here is 5)
print(predictions)