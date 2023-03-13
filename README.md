# Timelogger


## Installation

Start by creating a virtual environment using at least python 3.10
and activate it
```
python -m venv $PATH_TO_DIR-VENV_NAME
source $PATH_TO_DIR-VENV_NAME/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```


Now your ready to start using the timelogger, however i recommend adding the following 
in your terminal config file e.g. `.bash_profile`, `.zshrc` 

```
python_file="$(dirname -- "(insert path to timlogger.py file)"
logger() {
	~/.venv/my_bash/bin/python $python_file $@
}
```

That way you don't need to worry about activating the virtual environment and
the "app" can be accessed directly by just typing `logger ...` in your terminal

## Available commands


* create        Time logger, log/display/export your time
* update        Update a log entry with given id
* remove        Remove log entry with given Id

* list          List all log entries with timestamp today
  * Accepts dates argument with formats: YYYY:MM:DD, MM:DD DD (can either be `/` `:`or nothing between year, month and day values)
  e.g 
  ```
  logger list 202310 (list current day 2023 10 month)
  logger list 11 (list day 11 for 2023 and in current month )
  ```
* list_week     List all log entries by day for each weekday Mon-Sun
  * Accepts dates argument with formats: YYYY:WW, WW (can either be `/` `:`or nothing between year, month and day values)
  e.g 
  ```
  logger list_week 202310 (list week 10 in 2023)
  logger list_week 11 (list week 11 in 2023)
  ```

* set_tags      Tag log entries for special export time groups (works but be careful, cant currently remove tag)

* export        Export week of log entries to json format
  * Accepts dates argument with formats: YYYY:WW, WW (can either be `/` `:`or nothing between year, month and day values)
  e.g 
  ```
  logger export 202310 (export week 10 in 2023)
  logger export 11 (export week 11 in 2023)
  ```
* config        Configure the application settings, can run with config...
* display_conf  prints current configuration
* reset         Resets application settings and db
