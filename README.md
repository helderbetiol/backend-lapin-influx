# Backend

This the Backend in Python and Flask for the Lapin Project 2020-2021 at IMT Atlantique. 

## Setup

### Setup environment variables
Create a file called .env with the variables related to the InfluxDB you wish to connect. It should be defined as this example:
```terminal
INFLUX_HOST=localhost
INFLUX_PORT=8086
USER=root
PASSWORD=root
DBNAME=rabbit
```

### Option 1: Setup with requirements.txt
* Setup Virtual Environment
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Install Requirements
```terminal
pip install -r requirements.txt
```
### Option 2: Setup from scratch
* Setup Virtual Environment
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Install packages
```terminal
pip install flask
pip install python-dotenv
pip install Flask-Cors
pip install influxdb
pip install requests
pip install gunicorn
```

### Option 3: Setup for Heroku or Scalingo
Create an application in the selected platform and link it to your GitHub repository fork of this project. The Procfile is used to start the application. The environment variables should be defined in the respective platform (not as a .env file). Heroku calls them "Config Vars".

### Execution and Testing (locally)

* Run the application. It can be run with the command
```terminal
flask run
```
or the command 
```terminal
gunicorn --bind :5000 -w 1 project:app
```

* Make a GET request to http://localhost:5000/ with the browser or with curl
```terminal
curl http://localhost:5000/

OUTPUT:
Hello, World!
```