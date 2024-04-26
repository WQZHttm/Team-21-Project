# Team-21-Project 

## Manpower Optimisation in the F&B industry

The business we are cooperating with is Mount Faber Leisure Group (MFLG), and this project focuses on MFLG’s Good Old Days located in Siloso Beach Sentosa.

In recent years, it has become increasingly difficult to find part-time employees to fill in the manpower deficit due to an increase in Chinese, Philipino and Indian customers from the restaurant's buffet service.

In anticipation of decreasing prospective part-time employees, Good Old Days is seeking to find solutions to optimise its manpower allocation. The business also considered the utilisation of automation to help alleviate manpower shortage.

This project aims to relieve the problem of manpower shortages by optimising labour utilisation while reducing costs of manpower to its minimum.

This is done so in the following order: 

1. A Decision Tree model to predict customer counts for the week

2. A scheduling algorithm that recommends a schedule based on the prediction of customer count for the week and the number of employees 

3. Display of customer counts, recommended schedule and costs reduced by using the recommended schedule as compared to a manually written schedule  


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
