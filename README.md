# PROJECT: GeoAI Engine (Apache Sedona + PySpark + PostgreSQL)
STATUS:  Dockerized / Ready for Deployment

AUTHOR:  Imran Mazlan


[1] PREREQUISITES
------------------------------------------------------------------------------
1. Install Docker Desktop:
   - Windows/Mac: https://www.docker.com/products/docker-desktop/
   - Linux: sudo apt-get install docker-compose-plugin

2. Install VS Code Extension (REQUIRED for Notebooks):
   - Search for "Dev Containers" (by Microsoft) in VS Code and install it.

[2] FOLDER STRUCTURE
------------------------------------------------------------------------------
/sedona-project
  ├── Dockerfile             (Builds Python/Java/Spark OS)
  ├── docker-compose.yml     (Orchestrates the Engine and Database)
  ├── requirements.txt       (Python libraries list)
  ├── main.py                (Test script)
  └── test.ipynb             (Test notebook)

[3] SETUP & STARTUP (Do this once)
------------------------------------------------------------------------------
1. Open terminal inside this folder.
2. Build and Start the containers:
   docker compose up -d --build

3. Verify they are running:
   docker compose ps
   (You should see 'sedona_engine' and 'sedona_postgres' as "Up")

[4] HOW TO RUN PYTHON SCRIPTS (.py)
------------------------------------------------------------------------------
To run standard scripts like 'main.py':

1. Edit the file locally in VS Code.
2. Run this command in your terminal:
   docker compose exec sedona-app python main.py

[5] HOW TO RUN NOTEBOOKS (.ipynb)
------------------------------------------------------------------------------
To use Jupyter Notebooks, we must connect VS Code *inside* the container.

1. Click the blue "><" button in the bottom-left corner of VS Code.
2. Select "Attach to Running Container..." from the menu.
3. Choose "/sedona_engine".
   (A new VS Code window will open. This window is inside Docker).

4. Open your .ipynb file in this new window.

5. IMPORTANT: SELECT KERNEL
   - Look at the top-right of the notebook editor.
   - Click "Select Kernel".
   - Choose "Python Environments..." -> "Python 3.10 /usr/local/bin/python".
   - Ensure the code highlighting turns colorful (not plain text).

6. Run your cells!

[6] DATABASE ACCESS
------------------------------------------------------------------------------
To view data using DBeaver or pgAdmin from your laptop:

- Host:      localhost
- Port:      5433  (Mapped to 5433 to avoid local conflicts)
- User:      admin
- Password:  password123
- Database:  geodb

*NOTE: Inside Python code, use port 5432 and host 'sedona-db'.*

[7] SHUTDOWN
------------------------------------------------------------------------------
When finished, stop the engine to save RAM:

   docker compose down

------------------------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------------------------
1. ERROR: "Bind for 0.0.0.0:5433 failed"
   - Fix: Change port in docker-compose.yml to "5434:5432".

2. ERROR: "Kernel died" or "Exit code 137"
   - Fix: Open docker-compose.yml and lower SPARK_DRIVER_MEMORY to '2g'.

3. ERROR: "Plain Text" in Notebook
   - Fix: You forgot to select the Kernel (Step 5 above).
