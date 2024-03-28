import json

import requests

url = "http://localhost:8000/send-msg"
message = "Hello, how are you?"
data = {
    "senderId": 11,
    "message": "who's Adam Khemiri and how old is he",
    "timestamp": "2024-03-28T13:49:34.755Z"
}

headers = {"Content-type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)