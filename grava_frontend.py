import requests
import os
import json

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



#curl 'http://admin:admin@192.168.99.100:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"localGraphite","type":"graphite","url":"http://192.168.99.100","access":"proxy","isDefault":true,"database":"asd"}'

