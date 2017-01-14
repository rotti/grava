Grava - Analyse your Strava data in Grafana
=============================

Grava uses the [Strava API](https://strava.github.io/api/) to collect your personal activities. The activities are written inside a database and can be analysed afterwards.
The used database [InfluxDB](https://www.influxdata.com/) is a time series database. [Grafana](http://grafana.org/) is used for visualizing and analysing the metrics of the activities.


## Featureset
* *token_helper.py*: helps to get your Strava authentication tokens
* *filldb.py*: Reads all of your Strava activities and writes it into a InfluxDB database
* *make_dashboards.py*: Reads JSON templates and creates Grafana dashboards 

## How to see your Data in Grafana
1. Clone this repository
> git clone https://github.com/rotti/grava.git

2. InfluxDB Installation
TODO

3. Grafana Installation
TODO

4. Python library Installation
TODO

pip install influxdb, xxxxxxxxxx

5. Login to Grafana


## Usage of token_helper.py
Token helper gets your Strava access token and writes it to a file inside your authfile directory ("*./authfiles/access_token*"). It also provides help to get your code needed for the token exchange.

### Steps
1. Register as a developer at [strava.com](http://strava.com) and create your project to get your *ClientID* and your *Client Secret*.
2. Write your *ClientID* inside the file "./authfiles/client_id"
3. Write your *Client Secret* inside the file "./authfiles/client_id"
4. Write your *exchange token* inside the file "./authfiles/auth_code". 

To get your exchange token open a browser and use the following URL. Don't forget to put your *ClientID* inside the URL:
> https://www.strava.com/oauth/authorize?client_id=**YOURCLIENTID**&response_type=code&redirect_uri=http://localhost/token_exchange&scope=write&state=mystate&approval_prompt=force

Login with your Strava credentials and authorise your application. Afterwards you will receive and "Unable to connect" failure from your browser. Ignore it. You will receive your exchange token. It will loke something like "http://localhost/token_exchange?state=mystate&code=**1d1de858d2005b56e02d16d657cfad8bbc769a6f**". Paste the code to your file.

*token_helper.py* can provide some help to get your exchange token. Uncomment the specified section inside the code and execute it afterwards. Don't forget to put the comments in again afterwards. It will open a browser for you and will put in the needed URL.

5. Execute *token_helper.py* with 
> python token_helper.py



Find further help here: https://strava.github.io/api/v3/oauth/



## Inspiration and additional useful URLs

http://docs.grafana.org/installation/debian/

https://docs.influxdata.com/influxdb/v0.9/introduction/installation/

http://www.andremiller.net/content/grafana-and-influxdb-quickstart-on-ubuntu

https://github.com/weaveworks/grafanalib

https://groups.google.com/forum/m/#!forum/strava-api

https://github.com/hozn/stravalib

https://github.com/influxdata/influxdb-python
