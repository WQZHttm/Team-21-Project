import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sqlalchemy.types import VARCHAR
import sys
sys.path.append('../')
from db_server import db
#This Python script utilises the 'pandas' library for data manipulation.
#It also employs 'sklearn' for machine learning tasks, such as decision tree regression, model evaluation, and splitting the dataset into training and testing subsets.


data2024 = pd.read_sql_query('SELECT * FROM general_data', con=db.engine)
df = pd.read_sql_query('SELECT * FROM data_with_hour', con=db.engine)
#The data_with_hour.csv dataset contains the data generated using data_generate.py in the previous section, which consists of historical data from the year 2021 to 2023 used for training the model.
#The general_data.csv dataset contains data such as date, day, public holiday, event and Indian reservation, generated using generate_2024_data.py, for which the model will make predictions with.

def predict():
    def DecisionTree(data,prediction_data):
      def pub_hol_df(data):
        public_holidays_df = data[data['Public_Holiday'].notna()]
        public_holidays_df['Date'] = pd.to_datetime(public_holidays_df['Date'],dayfirst = True)
        public_holidays_df['Date'] = public_holidays_df['Date'].dt.strftime('%d/%m/%Y')
        return public_holidays_df
      #This function extracts public holidays from the dataset and converts the date column to the correct datetime format.
      #This is to store the names of the public holidays for future referencing.

      def clean_data(data):
        data['Date'] = pd.to_datetime(data['Date'],dayfirst = True)
        data['Year'] = data['Date'].dt.year
        data['Month'] = data['Date'].dt.month
        data['Day_of_week'] = data['Date'].dt.dayofweek
        data['Day'] = data['Date'].dt.day
        data['Date'] = data['Date'].dt.strftime('%d/%m/%Y')
        public_holiday = pub_hol_df(data)
        data['Public_Holiday'] = data['Public_Holiday'].fillna(0)
        data['Public_Holiday'] = data['Public_Holiday'].apply(lambda x: 1 if x else 0)
        data['Event'] = data['Event'].apply(lambda x: 1 if x == 'TRUE' else 0)
        return data
      #This function cleans and preprocesses the data.
      #It converts the 'Date' column to datetime format, extracts the year, month, day of the week, and day from the 'Date' column.
      #It also fill in missing values in the 'Public_Holiday' column with 0 and converts 'Public_Holiday' and 'Event' columns to binary (1 for true, 0 for false).

      def data_prep_train(data):
        train = clean_data(data)
        X = train.drop(columns=['Date',
                         'Customers_Chinese',
                         'Customers_India',
                         'Chinese > 100',
                         'Indian > 100',
                         'Food_Court_Customer',
                         '10am-11am',
                         '11am-12pm',
                         '12pm-1pm',
                         '1pm-2pm',
                         '2pm-3pm',
                         '3pm-4pm',
                         '4pm-5pm',
                         '5pm-6pm',
                         '6pm-7pm',
                         '7pm-8pm',
                         '8pm-9pm',
                         '9pm-10pm'])
        y = train[['Customers_Chinese',
            'Customers_India',
            'Food_Court_Customer',
            '10am-11am',
            '11am-12pm',
            '12pm-1pm',
            '1pm-2pm',
            '2pm-3pm',
            '3pm-4pm',
            '4pm-5pm',
            '5pm-6pm',
            '6pm-7pm',
            '7pm-8pm',
            '8pm-9pm',
            '9pm-10pm']]
        X_train,X_test,y_train, y_test = train_test_split(X,y, random_state=42)
        return X_train,X_test,y_train, y_test
      #This function prepares training data for the model.
      #It cleans the data using the clean_data function, separating the features (X) and the target variables (y)
      #It then split the dataset into training and testing sets using a 75/25 split ratio.


      def data_prep_predict(data):
        predict = clean_data(data)
        data = predict.drop(columns = ['Date'])
        return data
      #This function prepares data for making predictions by cleaning the prediction data and dropping the ‘Date’ column.

      training_ph = pub_hol_df(data) #public holidays in training data
      pred_ph = pub_hol_df(prediction_data) #public holidays in prediction data
      X_train,X_test,y_train,y_test = data_prep_train(data) #cleaned training data
      pred = data_prep_predict(prediction_data) #cleaned prediction data

      busy_threshold = 100
      def is_busy(customers_prediction):
          return customers_prediction > busy_threshold
      #This function take in the predictions for customer count and compare it with the threshold.
      #If the customer count is greater than the busy threshold, is_busy will return true.

      model = DecisionTreeRegressor(random_state=42)
      model.fit(X_train,y_train)
      y_pred = pd.DataFrame(model.predict(X_test), columns=['Predicted_Customers_Chinese',
                                                             'Predicted_Customers_India',
                                                             'Food_Court_Customer',
                                                             '10am-11am',
                                                             '11am-12pm',
                                                             '12pm-1pm',
                                                             '1pm-2pm',
                                                             '2pm-3pm',
                                                             '3pm-4pm',
                                                             '4pm-5pm',
                                                             '5pm-6pm',
                                                             '6pm-7pm',
                                                             '7pm-8pm',
                                                             '8pm-9pm',
                                                             '9pm-10pm'])
      mae = mean_absolute_error(y_test, y_pred)
      mse = mean_squared_error(y_test, y_pred)
      rmse = mean_squared_error(y_test, y_pred, squared=False)
      r2 = r2_score(y_test, y_pred)
      n = len(y_test)
      k = X_test.shape[1]
      adjusted_r2 = 1 - ((1 - r2) * (n - 1) / (n - k - 1))
      print("Mean Absolute Error:", mae)
      print("Mean Squared Error:", mse)
      print("Root Mean Squared Error:", rmse)
      print("R-squared (R2) Score:", r2)
      print("Adjusted R-squared:", adjusted_r2)

      predictions = pd.DataFrame(model.predict(pred), columns=['Predicted_Customers_Chinese',
                                                             'Predicted_Customers_India',
                                                             'Food_Court_Customer',
                                                             '10am-11am',
                                                             '11am-12pm',
                                                             '12pm-1pm',
                                                             '1pm-2pm',
                                                             '2pm-3pm',
                                                             '3pm-4pm',
                                                             '4pm-5pm',
                                                             '5pm-6pm',
                                                             '6pm-7pm',
                                                             '7pm-8pm',
                                                             '8pm-9pm',
                                                             '9pm-10pm'])
      #predicted customer count by day and the customer spread for the day.

      #post-processing of data
      prediction_data.reset_index(drop=True, inplace=True)
      date = prediction_data.apply(lambda row: f"{row['Day']}/{row['Month']}/{row['Year']}", axis=1)
      predictions['Date'] = pd.to_datetime(date,format = "%d/%m/%Y").dt.strftime('%d/%m/%Y')
      predictions['Day'] = pd.to_datetime(date,format = "%d/%m/%Y").dt.day_name()

      def get_public_holiday(date):
          if date in pred_ph['Date'].values:
              return pred_ph.loc[pred_ph['Date'] == date, 'Public_Holiday'].iloc[0]
          else:
              return ''
      #to return the public holiday name if it is a public holiday on that date
      predictions['Public_Holiday'] = predictions['Date'].apply(get_public_holiday)
      predictions['India_Reservation'] = prediction_data['India_Reservation']
      predictions['Chinese_Buffet_Busy'] = predictions['Predicted_Customers_Chinese'].apply(is_busy)
      predictions['Indian_Buffet_Busy'] = predictions['Predicted_Customers_India'].apply(is_busy)
      predictions = predictions[['Date',
                             'Day',
                             'Public_Holiday',
                             'Predicted_Customers_Chinese',
                             'Chinese_Buffet_Busy',
                             'India_Reservation',
                             'Predicted_Customers_India',
                             'Indian_Buffet_Busy',
                             'Food_Court_Customer',
                             '10am-11am',
                             '11am-12pm',
                             '12pm-1pm',
                             '1pm-2pm',
                             '2pm-3pm',
                             '3pm-4pm',
                             '4pm-5pm',
                             '5pm-6pm',
                             '6pm-7pm',
                             '7pm-8pm',
                             '8pm-9pm',
                             '9pm-10pm']]
      #final predictions table with all the information needed
      return(predictions)



    predicted = DecisionTree(df,data2024)
    engine=db.engine
    predicted.to_sql('predictions', if_exists='replace',
                con=engine, index=False,dtype={'Date': VARCHAR(50)})
