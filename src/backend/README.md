# Backend Folder

### Overview
This folder contains all the codes used by the backend to output predictions and optimal schedule. 
This folder also contains the optimal schedule in the form of a csv file.

### Content
- `data_generate.py`: Codes used to generate training data (2010-2023) for training our preditive model based on the relevant knowledge we learnt about the business from both stakeholders' meeting and public data
- `decision_tree_model.py`: Codes for the predictive model that we used to predict customer counts
- `generate_2024_data.py`: Codes for generating target data (2024) for our predictive model to predict desired information
- `requirements.txt`: A copy of requirements from other file "deployments". Copied here so it is more convenient to build a virtual environment
- `schedule.py`: Codes for the integer program based scheduling algorithm that optimises weekly schedule
- `transform.py`: Codes that combine year worth of weekly schedules and transform it into a dataframe (later converted into sql) file called "final_schedule"

### Usage and Possible changes
- Historical data can be used to replace data_generate.py and real time information about the future can replace generate_2024_data.py
- The Machine-Learning (ML) model we used to predictive customer count is a decision tree regressor, we might have experimented with other ML model, but feel free to experiment with any ML model that is suitable
- Linear time paradigm is used in the formulation of the integer program that is coded inside schedule.py
