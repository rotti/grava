import requests
import os
import json
import glob

session = requests.Session()
headers = {'content-type': 'application/json;charset=UTF-8'}


host = "localhost"
user = "admin"
password = "admin"
grava_org = "Grava"

grafana_port = ":3000"
grafana_url = "http://" + host + grafana_port
grafana_login_url = "http://" + host + grafana_port + "/login"
grafana_auth_url = "http://" + user + ":" + password + "@" + host + grafana_port

api_url_datasources = grafana_auth_url + "/api/datasources"
api_url_org = grafana_auth_url + "/api/org"


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


print "...setting up Grava"
put_organisation = session.put(url=api_url_org, data=json.dumps({'name': grava_org}), headers=headers)


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
print "...dashboard(s) loaded", dashboards
api_url_dashboards = grafana_auth_url + "/api/dashboards/db"

for db in dashboards:
    with open(db) as dash_json:
        dashboard = json.load(dash_json)
        #https://github.com/grafana/grafana/issues/2816#issuecomment-248795297
        dashdata = {}
        dashdata["dashboard"] = dashboard
        dashdata["overwrite"] = True
        dashdata["inputs"] = [{}]
        
    post_dashboard = session.post(url=api_url_dashboards, data=json.dumps(dashdata), headers=headers)
    print "...uploading dashboard '" + db , post_dashboard

    





