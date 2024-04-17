CREATE DATABASE IF NOT EXISTS customer_data;
USE customer_data;

CREATE TABLE IF NOT EXISTS customers (
  date VARCHAR(20),
  day VARCHAR(20),
  customer_chinese INT,
  customer_india INT,
  public_holiday VARCHAR(30),
  month VARCHAR(20),
  event TINYINT(1),
  india_reservation TINYINT(1),
  chinese_busy TINYINT(1),
  indian_busy TINYINT(1),
  food_court_customer INT,
  customer10 INT,
  customer11 INT,
  customer12 INT,
  customer13 INT,
  customer14 INT,
  customer15 INT,
  customer16 INT,
  customer17 INT,
  customer18 INT,
  customer19 INT,
  customer20 INT,
  customer21 INT
);



-- LOAD DATA LOCAL INFILE '/var/lib/mysql-files/data.csv'
-- INTO TABLE customers
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (date,day,customer_chinese,customer_india,public_holiday,month,event,india_reservation,chinese_busy,indian_busy,food_court_customer,customer10,customer11,customer12,customer13,customer14,customer15,customer16,customer17,customer18,customer19,customer20,customer21);

-- CREATE TABLE IF NOT EXISTS prediction (
--   date VARCHAR(20),
--   day VARCHAR(20),
--   public_holiday VARCHAR(30),
--   customer_chinese INT,
--   chinese_busy TINYINT(1),
--   india_reservation TINYINT(1),
--   customer_india INT,
--   indian_busy TINYINT(1),
--   food_court_customer INT,
--   customer10 INT,
--   customer11 INT,
--   customer12 INT,
--   customer13 INT,
--   customer14 INT,
--   customer15 INT,
--   customer16 INT,
--   customer17 INT,
--   customer18 INT,
--   customer19 INT,
--   customer20 INT,
--   customer21 INT
-- );

LOAD DATA LOCAL INFILE '/var/lib/mysql-files/predictions.csv'
INTO TABLE prediction
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (date,day,public_holiday,customer_chinese,chinese_busy,india_reservation,customer_india,indian_busy,food_court_customer,customer10,customer11,customer12,customer13,customer14,customer15,customer16,customer17,customer18,customer19,customer20,customer21);

-- CREATE TABLE IF NOT EXISTS schedule(
--   date VARCHAR(20),
--   day VARCHAR(20),
--   public_holiday VARCHAR(30),
--   employee_id VARCHAR(2),
--   shift VARCHAR(20),
--   role VARCHAR(10),
--   hours_work FLOAT,
--   hourly_rate INT,
--   job_status VARCHAR(20)
-- );
LOAD DATA LOCAL INFILE '/var/lib/mysql-files/schedule.csv'
INTO TABLE schedule
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (date,day,public_holiday,employee_id,shift,role,hours_work,hourly_rate,job_status)