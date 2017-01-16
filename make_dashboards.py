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

grava = GrafanaClient((user, password), host=host, port=port)

#XXX move to make_datasource.py
grava.org.replace(name=organistation)

# dashboards
#dashboards = glob.glob('dashboard_path + "*.json"')
dashboards = glob.glob('./dashboards/*.json')
print "... dashboards loaded", dashboards

for db in dashboards:
    with open(db) as dash_json:
        dashboard = json.load(dash_json)
    print "... creating dashboard ", dashboard
    grava.dashboards.db.create(dashboard=dashboard, overwrite=True)


#XXXX
datasource = {
    "name":"test_datasource",
    "type":"graphite",
    "url":"http://mydatasource.com",
    "access":"proxy",
    "foo":"bar"
}

foo = {"name":"test","type":"influxdb_08","url":"http://localhost:8086","access":"proxy","isDefault":"true","database":"asd","user":"asd","password":"asd"}

grava.datasources.create("")


