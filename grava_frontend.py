import requests
import os
import json
import glob
#import sys

session = requests.Session()
headers = {'content-type': 'application/json;charset=UTF-8'}


host = "localhost"
user = "admin"
password = "admin"


grafana_port = ":3000"
grafana_url = "http://" + host + grafana_port
grafana_login_url = "http://" + host + grafana_port + "/login"
grafana_auth_url = "http://" + user + ":" + password + "@" + host + grafana_port


api_url_datasources = grafana_auth_url + "/api/datasources"


ifdb_database = "strava"
ifdb_port = ":8086"
ifdb_url = "http://" + host + ifdb_port
datasource_name = "Grava Source"

ifdb_source = {
    'access': 'proxy',
    'database': ifdb_database,
    'name': datasource_name,
    'password': password,
    'type': 'influxdb',
    'url': ifdb_url,
    'isDefault': True,
    'user': user
}

############## Do stuff here ##########################

do_login = session.post(url=grafana_login_url, data=json.dumps({'user': user, 'password': password}), headers=headers)

print "...looking for existing datasources in", grafana_url
get_datasources = session.get(url=api_url_datasources)
datasources = get_datasources.json()


if not datasources:
    post_datasource = session.post(url=api_url_datasources, data=json.dumps(ifdb_source), headers=headers)
    print "...create datasource. using config", ifdb_source
else:
    print "...existing datasource(s) found."
    print "...skipping create datasource."


dashboards = glob.glob('./dashboards/*.json')
#dashboards = glob.glob('./simple.json')
print "...dashboards loaded", dashboards
api_url_dashboards = grafana_auth_url + "/api/dashboards/db"

for db in dashboards:
    with open(db) as dash_json:
        dashboard = json.load(dash_json)
        #print "dashboard", type(dashboard)
        #dashdata = {}
        #dashdata ['dashboard'] = dashboard
        #dashdata = json.dumps(dashdata)
        dashdata = { "dashboard": dashboard }
        print "XXX", type(dashdata), dashdata
    #print "... creating dashboard ", dashboard
    #post_dashboard = session.post(url=api_url_dashboards, data=json.dumps(dashboard), headers=headers)
    post_dashboard = session.post(url=api_url_dashboards, data=json.dumps(dashdata), headers=headers)
    print "XXX", post_dashboard






