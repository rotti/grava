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
grafana_auth_url = "http://" + user + ":" + password + "@" + host + grafana_port
print "XXX", grafana_auth_url

ifdb_database = "test"
ifdb_port = ":8086"
ifdb_url = "http://" + host + ifdb_port

datasource_name = "XXX xxx"
datasource_api = grafana_auth_url + "/api/datasources"

ifdb_source = {
    'access': 'direct',
    'database': ifdb_database,
    'name': datasource_name,
    'password': password,
    'type': 'influxdb',
    'url': ifdb_url,
    'user': user
}


# XXX write like POST
login_post = session.post(
   os.path.join(grafana_url, 'login'),
   data=json.dumps({
      'user': user,
      'password': password }),
   headers={'content-type': 'application/json'})

datasources_get = session.get(os.path.join(grafana_url, 'api', 'datasources'))
datasources = datasources_get.json()
print "...get datasources", datasources

print "XXX", grafana_auth_url
create_datasource = session.post(url=datasource_api, data=json.dumps(ifdb_source), headers=headers)



#make_datasource = session.post("http://admin:admin@localhost:3000/api/datasources", data=json.dumps(source), headers=headers)

#curl 'http://admin:admin@192.168.99.100:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"localGraphite","type":"graphite","url":"http://192.168.99.100","access":"proxy","isDefault":true,"database":"asd"}'

