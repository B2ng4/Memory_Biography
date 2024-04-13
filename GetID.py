import requests
from config import MEMORY_TOKEN


url = "https://mc.dev.rand.agency/api/cabinet/individual-pages"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": f"Bearer {MEMORY_TOKEN}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")