from grafana_api_client import GrafanaClient
import json
import sys
import glob

user = "admin"
password = "admin"
host = "127.0.0.1"
port = "3000"
dashboard_path = "./dashboards/"
organistation = "Grava"

strafana = GrafanaClient((user, password), host=host, port=port)

#XXX move to make_datasource.py
strafana.org.replace(name=organistation)


dashboards = glob.glob('dashboard_path + "*.json"')
print "... dashboards loaded", dashboards

for db in dashboards:
    with open(db) as dash_json:
        dashboard = json.load(dash_json)
    print "... creating dashboard ", dashboard
    strafana.dashboards.db.create(dashboard=dashboard, overwrite=True)


