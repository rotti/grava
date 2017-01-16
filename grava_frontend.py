import requests
import os
import json


host = "localhost"
user = "admin"
password = "admin"

grafana_host = "localhost"
grafana_port = "3000"
grafana_url = "http://" + host + ":" + grafana_port
grafana_auth_url = "http://" + user + ":" + password + "@" + host + ":" + grafana_port

ifdb_database = "test"
datasource_name = "XXX xxx"
ifdb_port = "8086"
ifdb_url = "http://" + host + ":" + ifdb_port

datasource_url = grafana_auth_url + "/api/datasources"
headers = {'content-type': 'application/json;charset=UTF-8'}

# XXX write like POST
session = requests.Session()
login_post = session.post(
   os.path.join(grafana_url, 'login'),
   data=json.dumps({
      'user': user,
      'password': password }),
   headers={'content-type': 'application/json'})

# Get list of datasources
datasources_get = session.get(os.path.join(grafana_url, 'api', 'datasources'))
datasources = datasources_get.json()
print "...get datasources", datasources

# Add new datasource

ifdb_source = {
    'access': 'direct',
    'database': ifdb_database,
    'name': datasource_name,
    'password': password,
    'type': 'influxdb',
    'url': ifdb_url,
    'user': user
}




session = requests.session()
print "XXX ", datasource_url
#make_datasource = session.post("http://admin:admin@localhost:3000/api/datasources", data=json.dumps(source), headers=headers)
make_datasource = session.post(url=datasource_url, data=json.dumps(ifdb_source), headers=headers)

#curl 'http://admin:admin@192.168.99.100:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"localGraphite","type":"graphite","url":"http://192.168.99.100","access":"proxy","isDefault":true,"database":"asd"}'

