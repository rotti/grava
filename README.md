# Strava Dashboard Docu
## step 1: clone github project
..* search for user "rotti" on github
..* select project korekuta
..* clone project by copying project url and executing git clone "url" in a shell
## step 2: get authentication toxen for strava api
..* create directory "config" with the command "mkdir config"
..* swith to directory "config" with command "cd config"
..* create the files "auth_code", "client_id" and "strava_secret" in the config directory with the command "touch auth_code"
..* register as a developer at strava.com and create your project
..* logon to the strave website "https://www.strava.com/settings/api" to get your client_id and strava_secret
..* copy your client_id from strava in the file "client_id" and your your strava secret in the file "strava_secret" both as strings; to do so open the listed files with an editor like nedit using the command "nedit client_id"; save and close them once you're done
..* edit the file token_helper.py deleting the # for comment as indicated in the code
..* execute file "token_helper.py" with the command "python token_helper.py"; this will open a webbrowser. you have to login to Strava and allow Korekuta to connect to Strava; you will then get an "Unable to connect" failure. But you will receive your tempory code listed at the end of the url; it will look something like "http://localhost/token_exchange?state=mystate&code=1d1de858d2005b56e02d16d657cfad8bbc769a6f"
..* copy the "code" as a string in the file "auth_code" in your config directory
..* reset the the file token_helper.py marking comments with a # sign again 
..* execute python token_helper.py from korekuta directory
..* the script writes the access token into the config file access_token


http://docs.grafana.org/installation/debian/

https://docs.influxdata.com/influxdb/v0.9/introduction/installation/

http://www.andremiller.net/content/grafana-and-influxdb-quickstart-on-ubuntu

pip install influxdb

https://github.com/weaveworks/grafanalib
