import json
import requests

url = 'http://66.175.215.240:1000/log-id'
file_name = '/var/www/c26-analytics/info.json'
headers = {'content-type': 'application/json'}

with open(file_name) as data_file:
	info = json.load(data_file)

requests.post(url, data=json.dumps(info["LogID"]), headers=headers)