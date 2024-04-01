import json

import requests

url = "http://localhost:8000/send-msg"

data = {
    "senderId": 11,
    "message": "now add 2 to that",
    "timestamp": "2024-03-28T13:49:34.755Z"
}

headers = {"Content-type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers) as r:
    print(json.loads(r.text)["message"])