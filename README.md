# Test Assignment for Data Engineer Position

This repository contains a complete data pipeline implementation, covering data extraction, transformation, and storage using modern data engineering tools. The project includes data cleaning, validation, structured storage, logging, and automation to ensure efficient data processing and management.
---

## 🧑‍💻 Task 1: NYC 2015 Street Tree Census Data Processing
### Requirements:
- **Download dataset from Kaggle: NYC 2015 Street Tree Census.**
- **Data Analysis & Cleaning:**
- **Perform Data Quality Analysis.**
- **Handle missing values, incorrect formats, duplicates, and errors.**
- **Database Setup in PostgreSQL:**
- **Define the schema based on cleaned data.**
- **Optimize table with indexes.**
- **Load Data into PostgreSQL:**
- **Insert cleaned dataset into the created table.**

---

## 🛠️ Provided Files:
- **task1/ - Directory containing the script for data processing.**
- **docker-compose.yml - Docker setup for PostgreSQL.**
- **SQL script - To create the required table.**
- **Python script - To clean and load the dataset into PostgreSQL.**

---

## 💻 How to Run Task 1:
- **Setup**
```bash
  git clone https://github.com/Fox1ine/DataWeave.git
cd task1
```
- **Start PostgreSQL using Docker:**
```bash
    docker-compose up -d
    
    To verify that PostgreSQL is running, use command :
    docker ps
```
- **Download & Install DBeaver:**
```bash

1.Create a Connection to PostgreSQL:
2.Open DBeaver.
3.Click Database → New Connection.
4.Select PostgreSQL.
5.In the connection settings, enter:
6.Take creds from .env
```
---

## 🐍 Provided Python Scripts:
### 📌 analyze_data.py - Initial Data Analysis
- **Loads the raw dataset from Kaggle.**
- **Performs exploratory data analysis (EDA):** Identifies missing values, duplicates, and inconsistent formats.
    Prints a summary of dataset structure and statistics.
- **Example output:**
```bash
Column 'tree_id': No missing values
Column 'species': 150 missing values detected
```
- **Starting from the root folder as a module**
```bash 
  python -m task1.src.analyze_data
```

### 📌 clean_data.py - Data Cleaning
- **Removes duplicate records.**
- **Handles null values by applying appropriate imputation or dropping.**
- **Standardizes column formats (e.g., date formats, numeric types).**
- **Saves the cleaned data to a .csv file for further processing.**

### 📌 create_table.py - Database Table Setup
- **Defines the PostgreSQL schema.**
- **Executes an SQL script to create an optimized table in PostgreSQL.**
- **Ensures indexes are created for faster queries.**

### 📌 load_data.py - Data Loading
- **Reads the cleaned dataset and inserts records into PostgreSQL.**
- **Uses batch inserts to improve performance.**

### 📌 test_connection.py - Database Connection Test
- **Verifies if PostgreSQL is accessible.**
- **Runs a simple SELECT query to validate data presence.**

### 📁 data folder
- **Raw data from API**
- **Data after cleaning**

---

## 📝 Additional information
### Missing Values in Multiple Columns:
#### Affected Columns:
- health (31,616 missing values)
- spc_latin, spc_common (31,619 missing values)
- steward (519,438 missing values)
- guards (603,922 missing values)
- sidewalk (31,616 missing values)
- problems (457,944 missing values)
- council district (6,519 missing values)
- census tract (6,519 missing values)
- bin, bbl (9,559 missing values)

Fix:
- For categorical columns like health, spc_latin, spc_common, steward, guards, sidewalk, and problems, missing values were replaced with "Unknown" or "Not Reported", depending on the column's context.
- For numerical columns like council district, census tract, bin, and bbl, missing values were forward-filled (ffill()) where possible, or replaced with -1 as a placeholder.
#### Duplicate Rows:
- Identified: 0 duplicate rows were found in the dataset.
- Fix: No action needed.

#### Incorrect Data Formats:
- Issue: created_at column stored as object (string).
- Fix: Converted created_at to a proper datetime format using:
 ```bash
      df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
```

#### Inconsistent Column Names:
- Some column names had spaces or special characters that could cause issues when loading into PostgreSQL.
- Fix: Renamed columns for better consistency:
```bash 
    df.rename(columns={
        "community board": "community_board",
        "council district": "council_district",
        "census tract": "census_tract",
      }, inplace=True)
```

#### Outliers in tree_dbh (Tree Diameter):
- Issue: tree_dbh (diameter at breast height) had extreme values up to 450.
- Fix: Values greater than 100 were considered unrealistic and set to NaN, then forward-filled.
```bash
   df.loc[df['tree_dbh'] > 100, 'tree_dbh'] = np.nan
df['tree_dbh'].fillna(method='ffill', inplace=True)
```

#### Encoding Issues in Categorical Columns:
- 'status' column contains values: ['Alive', 'Stump', 'Dead']
- Fix: Converted to lowercase for consistency.
```bash
    df['status'] = df['status'].str.lower()
```




---


## 🧑‍💻 Task 2: Weather Data Collection and Processing
### Overview
This task involves setting up an Apache Airflow pipeline to collect hourly weather data for Minsk using the OpenWeatherMap API. 
The data includes temperature and wind speed and is stored in Parquet format for historical analysis.

---

### Requirements
Airflow Deployment:
- Deploy Airflow using Docker Compose. 
- Ensure Webserver, Scheduler, and Worker are correctly configured.

Weather Data Collection:
- Fetch temperature and wind data hourly using the OpenWeatherMap API.

Data Processing:
- Convert API response into pandas DataFrame.
Ensure the data contains:
- Temperature Data (temp.parquet):
- datetime, temp, feels_like, temp_min, temp_max, pressure 
- Wind Data (wind.parquet):
- datetime, speed, deg, gust

### **Storage:**
**Raw Data:** : 
- Fetched weather data is stored in JSON format inside the ```data/raw/ directory.```
- Filenames follow the pattern ```current_raw_{YYYYMMDD_HHMMSS}.json.```
**Processed Data** :
- Two main directories exist for structured storage: ```data/temperature/ → Stores hourly temperature data.```
- ```data/wind/ → Stores hourly wind data.```
**Inside each directory, data is grouped into daily folders, such as** :
- ```data/temperature/minsk_YYYY-MM-DD_temp/```
- ```data/wind/minsk_YYYY-MM-DD_wind/```

**Processed Data** :
Two main directories exist for structured storage: 
- ```data/temperature/ → Stores hourly temperature data.```
- ```data/wind/ → Stores hourly wind data.```

Inside each directory, data is grouped into daily folders, such as:
- ```data/temperature/minsk_YYYY-MM-DD_temp/```
- ```data/wind/minsk_YYYY-MM-DD_wind/```

Each folder contains hourly .parquet files named with timestamps:
- ```time-HH-MM-SS.parquet```

**Schedule DAG in Airflow:**
```Runs every 60 minutes.```

**Provided Files:**
- ```task2/ ``` - Contains Airflow DAG and weather processing scripts. 
- ```docker-compose.yml``` - Airflow deployment configuration.
- ```Example parquet files``` - Demonstrating expected output. 
- Screenshots of DAG execution in Airflow UI.

### **How to Run Task 2**
- Start Airflow with Docker:
```aiignore
docker-compose up -d
```
- Check Airflow Web UI (```default localhost:8080```).
- Enable and start the weather data pipeline:
```docker exec -it airflow_webserver airflow dags unpause weather_dag```
- Verify Data Output - Processed data should be saved in:
```aiignore
data/
 ├── temperature/
 │   ├── minsk_2025-02-27_temp/
 │       ├──time-13-00-03.parquet
 │   ├── minsk_2025-02-28_temp/
 │      ├──time-13-00-03.parquet
 │   
 ├── wind/
 │   ├── minsk_2025-02-27_wind/
 │       ├──time-13-00-03.parquet
 │   ├── minsk_2025-02-28_wind/
 │       ├──time-13-00-03.parquet
 
```

#### Docker Compose Configuration:
- The ```docker-compose.yml``` file provided in this repository sets up the following services:
```aiignore
PostgreSQL - Stores Airflow metadata.
Redis - Used as a message broker for task queues.
Airflow Webserver - Provides the UI for monitoring DAGs.
Airflow Scheduler - Periodically checks and triggers DAGs.
Airflow Worker - Executes tasks asynchronously.
```

#### Steps to Deploy Airflow Locally
- Ensure Docker and Docker Compose Are Installed:
```sudo apt update && sudo apt install -y docker.io docker-compose```
- After:
```docker-compose up -d```

#### Airflow DAG Execution Screenshots
Below are screenshots of the Airflow UI displaying DAG execution and task logs.

- ![img_1.png](img/img_1.png)
- ![img_2.png](img/img_2.png)

#### Notes
- The pipeline runs hourly, and each day's data is stored in its respective daily partition.
- DAG logs and errors can be found inside the ```logs/``` folder.
- Environment variables are managed via ```.env ``` for flexibility.
- Additional processing steps (e.g., aggregations, transformations) can be added in ```fetch_weather.py```,
- Examples of batch files are in the repository,
- Libraries can be loaded from - ```requirements.txt```.
    
---

## 🧑‍💻 Task 3: ETL: Data Loading
### Overview
This task involves setting up a data pipeline to extract, transform, and load (ETL) session data from multiple project databases into an analytics database (analytics_db).
### 📌 Objectives:
- Extract user session data from multiple project databases (project_a_db, project_b_db, project_c_db).
- Enrich session data with transaction details and currency conversion.
- Load the transformed data into the analytics_sessions table in the analytics_db.
- Automate the entire process using Apache Airflow DAG, running every 10 minutes.
- Ensure scalability for future project expansions.

### ⚙️ Airflow Setup
Installing and Running Airflow with Docker. I use docker-compose.yaml from ```task2```
Airflow is orchestrated using Docker Compose, which launches the required services:
- PostgreSQL as Airflow's metadata database.
- Redis as the Celery broker.
- Airflow Webserver, Scheduler, Worker for DAG execution.

#### 🛠 Airflow configuration
Firstly I have .env file inside Airflow contains:

![img_1.png](img/img_3211.png)

🔌 This ensures Airflow tasks can read environment variables for database connections.

Start Airflow:
```bash
docker compose up -d

Initialize the Airflow database:
docker exec -it airflow-webserver airflow db init
```
Access the Airflow Web UI at ```http://localhost:8080.```

I had a problem with several Docker Compose files that I was using, my docker is docker-compose.yml:
- Airflow (task 2): It contains Airflow services (web server, scheduler, worker).
- Databases (Task 3): Contains three project databases and an analytical database.

Since these are separate docker-compose environments, they do not share the same network by default. To enable communication, I linked them ```via a common external network.```

 ![img.png](img/img312312.png)
 
🔌 Connecting Airflow to Multiple Databases:
```bash

docker network create airflow_network
```
This ensures:
- All containers in task2 (Airflow) and task3 (PostgreSQL) are in the same network.
- Airflow can now access databases by their container names instead of localhost.

🔌 **Also, for connection to database, I used:**
```bash
postgresql://user:password@project_a_db:5432/project_a_db
```
Here, ```project_a_db``` is the container name, allowing Airflow to resolve it within the Docker network.

**And I manually configured connections in Airflow UI (Admin → Connections) for:**
- postgres_default: Connection to the analytics database.
- project_a_db, project_b_db, project_c_db: Connections for each project database.
- ![img_2.png](img/img_213211.png)

### 🏗 The main ETL strategy
1. **🔹Designing the ETL Workflow**
- When implementing the ETL pipeline, my main focus was ensuring scalability, modularity, and efficiency. I needed to extract, transform, and load data from three separate project databases (project_a_db, project_b_db, project_c_db) into a centralized analytics database (analytics_db).
- The decision to separate extraction, transformation, and loading into different scripts (```extract_data.py, enrich_data.py, and load_to_analit_bd.py)``` was made to keep each process isolated, making debugging and testing easier.
- Using Airflow DAGs for scheduling allowed me to automate the process, ensuring data freshness every 10 minutes.
- I structured the DAG tasks (extract, enrich, load) to execute sequentially while allowing potential parallelism in the future.

2. **🔹Schemas**
- I saved the scripts for creating tables in ```task3/src/sql``` there are ```analytics_tables.sql``` and schema for others PostgreSQL
- One of the key considerations in database design was query performance optimization. Since analytics queries involve aggregations and joins, I created indexes on frequently used fields.
- **🔹Indexes in ```projects_tables.sql``` :**
- Primary Key Indexes: id fields in tables like user_sessions, events, and transactions are indexed automatically.
- ```bash 
  CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_events_user_id ON events(user_id);
``` These ensure fast lookups for ```user-based``` analytics.
- Timestamps Indexes:
```bash 
CREATE INDEX idx_user_sessions_last_activity ON user_sessions(last_activity_at);
```
Since filtering by session date is frequent, this helps optimize query execution time.

- **🔹Indexes in ```analytics_tables.sql (Analytics Database)```** (how I said u can check the script ```task3/src/sql/analytics_tables.sql```)
```bash 
CREATE INDEX idx_analytics_sessions_user_date ON analytics_sessions(user_id, session_date);
```
This ensures efficient filtering and aggregation when querying user sessions per date.

### Handling Multiple Projects & Scalability
The system is designed to support up to 10 project databases in the future. To achieve this:
- Instead of hardcoding database URLs, I store them in an .env file and read them dynamically in ```extract_data.py```:
```bash
DB_CONNECTIONS = {
    "project_a": os.getenv("PROJECT_A_DB_URL"),
    "project_b": os.getenv("PROJECT_B_DB_URL"),
    "project_c": os.getenv("PROJECT_C_DB_URL")
}
```
- This allows for adding more projects without modifying the DAG, only updating the .env file.
- The ```extract_data.py``` script loops over all project databases, making it adaptable for future expansion.

### 🚀 Ensuring Incremental Data Loads
- To avoid reprocessing the entire dataset every time:
    I retrieve the last processed session date from analytics_sessions:
```aiignore
SELECT MAX(session_date) FROM analytics_sessions;
```
- Only new sessions are inserted, preventing duplication.

### 🔄 Data Storage and Processing Locations
- Raw data is stored in: /opt/airflow/data/extracted_sessions;
- Enriched data is stored in: /opt/airflow/data/enriched_sessions
- Final loaded data goes to: analytics_sessions table in analytics_db
**I also saved the conclusions in the repository, you can look in the folder - ```task3/data```**

### 🖥️  DAG Automation & Monitoring - ```etl_analytics_sessions_dag_task3.py```
- The ETL process runs every 10 minutes to ensure fresh data.
- If any task fails, Airflow automatically retries up to 1 time before marking it as failed.
- Logs are available in /opt/airflow/logs for debugging.

![img_3.png](img/img_3311.png)


### 🏆 Final Thoughts & Reflections on the Test Assignment
**🌟 Overview of the Challenge**

**This test assignment was an extensive real-world simulation of a data engineer’s responsibilities—designing an end-to-end ETL pipeline from scratch, handling multiple data sources, ensuring data integrity, and integrating everything into a scalable workflow using Airflow.**

**The challenge required:**
- ✔️ Database architecture design – planning schema structure, optimizing indexing, and handling transactions efficiently.
- ✔️ Airflow automation – implementing DAGs to extract, transform, and load session data at regular intervals.
- ✔️ Dockerized environment setup – managing multiple services across separate docker-compose configurations while ensuring proper networking between them.
- ✔️ Handling multiple databases dynamically – making the pipeline scalable to support up to 10 projects in the future.
- ✔️ Debugging connectivity & permission issues – resolving network, access, and connection problems while integrating various components.

This was not just a coding challenge—it tested problem-solving abilities, debugging skills, and architectural decision-making.

### 📈 Additional Improvements & Future Work (Just my thoughts)

While the ETL pipeline is now fully functional, there are further improvements that could enhance its robustness and efficiency:
- **🚀 1. Distributed Processing with Apache Spark**
-Currently, data transformation & enrichment happens using Pandas, which works well for moderate-sized datasets. However, as the data grows:
- ✔️ Switching to Apache Spark could allow distributed processing for better scalability.
- ✔️ Using Spark SQL for transformations instead of Pandas would improve parallel execution.
- 🔄 2. Implementing Change Data Capture (CDC)

- Right now, session updates rely on SELECT MAX(session_date) to detect new data.
- An event-driven CDC approach (e.g., Debezium + Kafka) would:
- ✔️ Enable real-time updates instead of batch processing.
- ✔️ Improve efficiency by reducing the amount of scanned data.

- 🛠️ 3. Adding Unit Tests for ETL Components

- ✔️ Implementing unit tests for data extraction & transformation would improve pipeline reliability.
- ✔️ Using pytest + mock databases could allow automated validation of data integrity.

- 🔒 4. Enhancing Security & Access Control

- ✔️ Role-based access control (RBAC) in Airflow UI to prevent unauthorized DAG execution.
- ✔️ Storing sensitive credentials in a secrets manager instead of .env files.

---