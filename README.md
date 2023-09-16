
###### InsightHub API ######


### Installation


# Install Python

Python 3.10.5

https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe


# Install database

1. PostgreSql 14

https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

2. PgAdmin 4

https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v6.16/windows/pgadmin4-6.16-x64.exe


# Install Editor

Pycharm  2022.1.3

https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC

or 

Visual Studio Code 1.74.0

https://code.visualstudio.com/Download


# Clone a repository

Run command in terminal

git clone https://github.com/CreativeBufferOfficial/insighthub_backend.git

# Create and Activate virtual environment

For Windows run:

1. py -m pip install --upgrade pip

2. py -m pip --version

3. py -m pip install --user virtualenv

4. py -m venv insightHub_env

5. .\insightHub_env\Scripts\activate

For Unix/macOS run:

1. python3 -m pip install --user --upgrade pip

2. python3 -m pip --version

3. python3 -m pip install --user virtualenv

4. python3 -m venv insightHub_env

5. source insightHub_env/bin/activate

# Change the directorary

cd insighthub_backend

# Install requirement.txt file

Run command in terminal

pip install -r requirement.txt


# Create database

Create a database from pgadmin

1. Open pgadmin.

2. Enter password created at the time of Installation.

3. Click on Servers.

4. Right click on PostgreSQL 14 then go on Create and then click on Database.

5. Fill database name and then click on save.

6. Your database is created now.

# Create .env file

You have to craete a '.env' file inside 'InsightHubAPI'.

# Environment Variables

To run this project, you will need to add the following environment variables to your .env file

DATABASE_NAME = your database name
DATABASE_USER = postgres
DATABASE_PASS = your password
HOST = localhost

# Migrate database

To migrate the database you have to run this command

python manage.py migrate

# Run server

To run the server you have to run this command

python manage.py runserver