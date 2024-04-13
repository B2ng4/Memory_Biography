import requests
import json

from config import MEMORY_TOKEN


url = "https://mc.dev.rand.agency/api/page/79051330"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": f"Bearer {MEMORY_TOKEN}"
}

dat = {
    "name": "Иванов Иван Иванович",
    "start": {
        "day": "02",
        "month": "01",
        "year": 1938
    },
    "end": {
        "day": "03",
        "month": "01",
        "year": 1975
    },
    "epitaph": "КРАТКАЯ ЭПИТАФИЯ",
    "author_epitaph": "АВТОР ЭПИТАФИИ",
    "page_type_id": "1"
}

response = requests.put(url, headers=headers, data=json.dumps(dat))

if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")