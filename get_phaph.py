import requests
import json

ZABBIX_URL = "http://zabbix.airip.co.za/zabbix/api_jsonrpc.php"
USERNAME = "tanvir"
PASSWORD = "tnvr1123"

# Authenticate
payload = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "username": USERNAME,
        "password": PASSWORD
    },
    "id": 1
}

session = requests.Session()
response = session.post(ZABBIX_URL, json=payload).json()

auth_token = response['result']

# Get all graphs
payload = {
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": ["graphid","name"],
        "selectHosts": ["host"]
    },
    "auth": auth_token,
    "id": 2
}

graphs = session.post(ZABBIX_URL, json=payload).json()["result"]

for g in graphs:
    print(f" (host: {g['hosts'][0]['hostid']}-{g['hosts'][0]['host']})")
