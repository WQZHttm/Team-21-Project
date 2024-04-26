#  Manpower Optimisation in the F&B industry: Team-21 project, Time for Change

## Overview

In context of Good Old Days’ (under Mount Faber Leisure Group) difficulty in finding potential part-time staff to support the business, “Time for Change” is an ambitious endeavour that aims to predict customer count, make use of predicted customer count to generate an optimal schedule for the week based on business requirements and build a simple yet meaningful dashboard that displays the schedule and many more information to empower stakeholders’ decision making in an interactive way. This project’s backend exemplifies how data science involves more than just statistical learning such as machine learning models, but also includes operation research (OR) techniques, and specifically for this project, a branch of OR known as scheduling theory. On the other hand, frontend demonstrates how the utilisation of advanced softwares such as mySQL, python flask and docker, can greatly improve the delivery of information on the business operation to relevant stakeholders in the most appealing and efficient ways. In conclusion, “Time for Change” is a full stack data science project aimed at solving real-world business problems and delivering the solution as a product in the form of a dashboard.

## Methodology

### Exploratory Data Analysis (EDA)

We decided to look into possible influences for customer retention and acquisition for this restaurant. Given the high numbers of Chinese and Indian foreigners frequenting the restaurant, we looked into popular times of the year when these foreigners like to visit Singapore and the restaurant by extension. We also looked at the times of the year where locals mostly visited the restaurant for reasons such as public holidays, school holidays months and special events nearby. Furthermore, we analysed the different days of the week and times of the day to identify peak days and hours.

### Data Generation

To generate realistic customer head-count data for predictive analysis, we analyse daily, weekly, and yearly customer traffic patterns, utilising observed data sources such as Google Maps foot traffic and tourism statistics. Data we generate captures daily surges in activity at food courts around lunchtime, heightened weekly traffic on weekends and holidays, and yearly spikes during major vacation months like July, August, December, and January. This comprehensive, multi-dimensional approach, grounded in real-world trends and detailed data analysis, allows us to develop a robust dataset. This multi-dimensional approach, informed by real-world trends and comprehensive data analysis, enables us to construct a robust dataset that enhances the accuracy of our predictive models and supports strategic business planning.

### Predictive Model Development

This project utilises a decision tree model trained on historical data to predict customer flow in a food court. The model takes in data such as date, day, public holiday, event, Indian reservation and returns the predicted number of customers for different time slots and the overall customer flow for a given day. The service is built using Python, particularly leveraging libraries such as numpy, pandas and scikit-learn. The model is then evaluated using various metrics such as Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, R-squared Score, and Adjusted R-squared.

### Mathematical Model Development (Scheduling theory)

- Understanding the mathematics: Visualise work schedule transformed from natural table format to a column vector, so that linear algebra can be applied to solve the problem. More specifically, the cost function and constraint functions can be written as row vectors as a consequence of re-writing the schedule into a column vector.
- Mathematical formulation: Formulate an integer program in accordance to above visualisation
- Implement scheduling algorithm: Implement scheduling algorithm in python and using ortools by Google Cloud. The algorithm takes in the prediction for the week by above predictive model and use it to solve scheduling problem for kitchen, Full-time service & Part-timers and dishwashers based on formulation above before combining them to form a complete schedule for the week

### Dashboard

Our dashboard is designed to be simple and easy for you to use, while still providing you relevant information.

The dashboard consists of the following pages:
- Daily page: Pick a date of the year to see schedule for the day, events for the day and predicted customers count for every operational hour of the day
- Weekly page: Pick a week of the year to see the allocated manpower of each role for everyday of the week, its corresponding costs and events for the week 
- Employee Details Page: Pick a range of dates within a year and an employee’s name to see the employee’s role, status, hours worked, total pay and schedule throughout the date range given. Additionally, the page is also equipped with a whatsapp button to directly message given employee
- Labour Cost Percentage (LCP) Page: Sliders to adjust number of employee of each role and each shift to form a customised schedule and a bar graph to display labour costs of a manually written schedule, optimised schedule and aforementioned customised schedule

### Dashboard Features

- Recommendation & Information: Our dashboard not only informs stakeholders, but it also provides recommendation (optimal schedule) to assist in their work
- The Human Touch: Our dashboard does not see employees as just another data point in their project. Thus, we included a whatsapp direct message button as a means to reach out to them from the dashboard
- Room for experimentation: Our dashboard’s LCP page is dedicated towards informing stakeholders manpower costs for every possible schedules and how it fared against a manually written schedule and optimal schedules through interactive experiment 

### Deployment (and Monitoring)

- Staged Rollout: Begin by deploying the dashboard to a select group of users in a controlled environment. This approach enables us to collect valuable feedback and identify any issues, allowing for gradual refinements prior to a comprehensive rollout.
- Integration: Ensure the dashboard integrates smoothly with existing restaurant management systems to enhance and support current operational workflows. This will allow for a seamless transition and improved overall efficiency.
- Training: Conduct comprehensive training sessions for all end-users, focusing on how to navigate the dashboard, understand the data visualisations, and utilise the recommendation tools effectively.

## Impact of Project

The implementation of manpower optimization in restaurants can lead to a wide array of benefits, including reduced labour costs, increased employee satisfaction and reduced turnover rates. By implementing the optimised manpower schedule, the restaurant would be able to resolve the issue of manpower shortages and reduce overstaffing and underutilization of staff during off-peak hours. This in turn allows for a reduction in labour cost. 

Optimised staffing can prevent employee burnout and ensure a fair distribution of work among staff, which in turn reduces turnover rates for both part-time and full time employees. By leveraging data-driven insights, restaurants can make informed decisions that positively impact their operations, ultimately leading to greater efficiency and profitability.

## Future Enhancements

Future enhancements to this project may include:

Backend:
- Proprietary data: Use proprietary data that competitors have no access to, to gain a data edge over them
- Custom made ML model: Build proprietary machine learning model to suit business needs
- Optimising optimisers: Buy licence to use “Gurobi” optimiser as it is renowned to produce the best results in constraint optimisation (such as the one in our project) but has not been tried due to lack of funds
- Deferred offs feature: Instead of completely separating the weeks to optimise schedule, we can take into account future week’s to defer offs that employees missed in the present week 

Frontend

- Authentication Login: Having users to login before accessing the dashboard can improve application’s data privacy for stakeholders  
- Save Report Feature: Download feature to save staff schedules, relevant employee information, etc for future reference
- Employee Availability page: The page will feature employees who initially indicated their availability for each day in the form of employee cards (which features their name, role, Whatsapp button to contact them). In the event staff allocated for the day cannot attend work last minute, the head chef can fill up these vacancies easily by checking this page and conveniently contacting them.


## Running the App

### Build application
1. Ensure Docker Desktop is downloaded and open in the background. Remove all existing containers and images if possible.
2. Open Command Prompt.
3. Ensure directory in Command Prompt is the same as the cloned repository.
4. Build the Docker image manually by cloning the Git repo. It will take approximately 30 minutes to build the image. (docker compose works well)
```
git clone git@github.com:WQZHttm/Team-21-Project.git
```
```
docker-compose up --build
```
5. Visit http://localhost:8050 once image is built.

### Troubleshooting
If you face the following issue: `backend-1  | /usr/bin/env: ‘bash\r’: No such file or directory`, go to `wait-for-it.sh` file, change End of Line Sequence from "CRLF” to “LF” for. For users using Visual Studio Code on Windows, refer to the bottom of the page and click on "CRLF".

### Additional Notes
Kindly ignore all commit messages, as all final code pushed into main works.
