![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![DBeaver](https://img.shields.io/badge/DBeaver-372923?style=for-the-badge&logo=dbeaver&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)


1.	Highlight of this project
2.	Main focus on ETL pipeline using AIRFLOW.
3.	Feature store implementation using Redis (linux based online feature store) because Job lib is slow for retrival and scalability issues.
4.	data drift detection using alibi detect library to calculate drift.
5.	ML monitoring using prometheus (Data source for metrics) and Grafana (for dashboard). However these two are resource intensive.

Step 1
Database setup
1.	Create bucket in GCP (untick Enforce) and upload data file into it.
2.	Create a service account and give permissions and download key (json file).
Now for service account we need to give access to bucket. So same as project 2. Refer: step 3

Step 2
Project setup
Same as project 2. Refer step 2.
Then run pip install -e .
So that we initialise the project and a folder is created with our name in setup.py.
Without this run , we can’t make our folders treated as a package.

Step 3
ETL from bucket to PostgreSQL Database
1.	Download astro cli for windows -  add path under environment variables -user variables-new-paste path-ok-closeall. Now in cmd check astro version and confirm it’s there.
2.	Now go to venv and astro dev init to inititalise astro in our project. This will ask y/n then you say y. Now you see some folders created in your project. Now go and copy the json file and paste it under include folder and rename json it for easy working.
3.	Go to .asto folder and to config.yaml file and paste the code from material. This code will fetch the gcp json file from include folder.
4.	Install apache airflow providers for google. Go to dockerfile and write commands. Now run the astro dev start in venv.
5.	It will create a local host astro UI (8080). Login with admin, admin 
6.	Now in UI – go to admin- create two connections – one for gcp – one for postgres- see material for info to fill in while creating these. 
7.	In postgres connection the host name  and port can be seen in the docker app when you click containers.
8.	Now we create a .py in dags directory and code it (from material) for Extracting data from gcp and transform it and load it to postgres database.
9.	Now we go to airflow UI and trigger the “extract_titanic_data” and it should show 3 green boxes.
10.	Now we successfully extract csv from bucket and transformed into postgres suitable format.
11.	To view this we cannot direct view. So we download and install dbeaver and establish a connect by opening the dbeaver – database-new database-select postgres-then give the username and password- test connection- ok-finish. Now you see your established connection on left pane.
12.	Now to see the data in Databases-postgres-schemas-public-tables-titanic. Go to the SQL editor and write the query and run. That’s it you can see the data now.


Step 4
Data Ingestion
1.	Add psycopg2(connector postgres to python) and scikit-learn to requirements.txt and run the pip install -e .
2.	Now create the paths_config.py, database_config.py and data ingestion.py and code all and run. You should see the artifacts downloaded from postgres to local machine (project directory).
3.	Notebook testing.

Step 5
Building feature store using Redis
1.	Go to requirements and write redis. Run the pip command to install.
2.	Then run 2 cmds from material so that it will install the redis image in the docker.
3.	Now you will see redis container running in docker.
4.	Now create feature_Store.py and code it.
5.	Data processing.py and code it, run it, see logs for confirmation.
6.	Model_training.py , code and run
7.	Training_pipeline.py , code and run.
8.	For code versioning, create git repo.
9.	In venv git init, add branch, add remote origin, add,commit, push.

    
Step 6
User app building using flask and chatgpt
1.	Create a index.html under templates, style.css under static and application.py in root, add flask to requirements. Code all and run. You should see the UI in web running successfully with predictions from the model
   
Step 7
Drift detection using Alibi-detect

1.	Add alibi-detect to requirements and run the pip to instal.
2.	Now come to application.py and make the code changes for alibi-detect.
3.	The code will compare and calculate the drift bet new data with reference data (train data).
4.	If you are seeing is_drift = 1 which means, there is drift in new and train data.
   
Step 8
ML monitoring : Prometheus and Grafana
1.	Install both of them. As they don’t support windows. We use docker.
2.	Make two file in root names docker_compose.yml and promethues.yml and code them from material.
3.	Add prometheus_client to requirements and run pip. It will take some time.
4.	Now after they are done. You see both running in docker. Then you go to http://localhost:9090/ for Prometheus and http://localhost:3030/ for Grafana and login with admin , admin.
5.	Now make some changes in application.py for the above both custom and inbuilt metrics. And you also set the app to run on 5000. So this time it doesn’t give the port. We just go to localhost:5000.
6.	Run docker restart Prometheus 
7.	Now run the application.py
8.	And run some prediction in the localhost:5000 and localhost:5000/metrics in another page to see the plain metrics. Whenever you make a prediction, the custom metrics change in this metrics page which means it is working fine.
9.	Now the metrics are showing in plain text. But we want in dashboard that is where Grafana comes into picture. So go to Grafana and datasources on the left pane under connections and select Prometheus.
10.	Now give http://prometheus:9090/ for connection.
11.	Click save and test in bottom. It should give successful message.
12.	Make sure your application is running (in your terminal you didn’t stop it).
13.	Now go to Prometheus – status – target health.
14.	Here you should see your metrics link and state should be UP(green)
15.	Now let’s create a dashboard. So go to it on left pane and create visualization and select Prometheus.
16.	Now go to metric under queries and select one and click run queries button. You see a nice viz on top of same page.
17.	Now let’s save the dashboard on top right and save. Go to dashboard on left pane and select yours.
18.	As we don’t have any predictions at the moment, the graph is empty. So lets make some on our flask app and see how it changes here.
19.	Run 4 predictions and refresh the plain text and you will the metrics increment. Now if you go dashboard , it will be updated and graph looks nice now.
20.	So you can add the metrics on the top right Add- Visualization- select metric- run queries- save dashboard.
21.	Note: while making predictions, you need to wait 15sec in bet each. Because we have mentioned this in Prometheus code.
22.	Done

