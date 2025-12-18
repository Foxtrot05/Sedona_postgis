# Sedona_postgis
Apache Sedona project that involve PostgreSQL with PostGIS as extention.


# PROJECT: GeoAI Engine (Apache Sedona + PySpark + PostgreSQL)
# STATUS:  Dockerized / Ready for Deployment
AUTHOR:  Imran Mazlan


[1] PREREQUISITES
------------------------------------------------------------------------------
Before you start, you only need ONE tool installed on your laptop:

1. Install Docker Desktop:
   - Windows/Mac: https://www.docker.com/products/docker-desktop/
   - Ubuntu: sudo apt-get install docker-compose-plugin

   *Verify installation by opening a terminal and running:*
   docker compose version

[2] FOLDER STRUCTURE
------------------------------------------------------------------------------
Ensure you have the following files in this folder (do not rename them):

/sedona-project
  ├── Dockerfile             (Builds Python/Java/Spark OS)
  ├── docker-compose.yml     (Orchestrates the Engine and Database)
  ├── requirements.txt       (Python libraries list)
  ├── main.py                (Test script)
  └── README.txt             (This file)

[3] SETUP & STARTUP (Do this once)
------------------------------------------------------------------------------
1. Open your terminal (or Command Prompt/PowerShell) inside this folder.

2. Build and Start the containers:
   docker compose up -d --build

   *Note: The first run will take 5-10 minutes to download dependencies.*

3. Check if everything is running:
   docker compose ps

   *You should see two services listed as "Up" or "Running":*
   - sedona_engine  (The AI Logic)
   - sedona_postgres (The Database)

[4] HOW TO RUN CODE
------------------------------------------------------------------------------
To run Python scripts, we execute them *inside* the Docker container.

Run the test script:
   docker compose exec sedona-app python main.py

*DEVELOPMENT WORKFLOW:*
1. Edit 'main.py' (or any .py file) in your local VS Code.
2. Save the file.
3. Run the command above in your terminal.
   (Changes are synced instantly; no need to restart Docker).

[5] DATABASE ACCESS (Optional)
------------------------------------------------------------------------------
If you want to view the data using DBeaver or pgAdmin:

- Host:      localhost
- Port:      5433  (Mapped to avoid conflict with local DBs)
- User:      admin
- Password:  password123
- Database:  geodb

[6] SHUTDOWN
------------------------------------------------------------------------------
When you are done for the day, stop the environment to save RAM:

   docker compose down

*Note: Your database data IS saved safely in the 'postgres_data' volume.*

------------------------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------------------------
1. ERROR: "Bind for 0.0.0.0:5433 failed: port is already allocated"
   - Solution: Change the port in 'docker-compose.yml' from "5433:5432" to "5434:5432".

2. ERROR: "Exited with code 137" (Memory Crash)
   - Solution: Open 'docker-compose.yml' and change SPARK_DRIVER_MEMORY to '2g'.

3. ERROR: "command not found: docker"
   - Solution: Ensure Docker Desktop is running in the background.
