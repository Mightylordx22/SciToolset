import json
import grequests
import requests
import urllib3

from scripts.db_link import check_for_bearer_token

urllib3.disable_warnings()


headers = {
    'Content-Type': "application/json",
    'Authorization': f"Bearer {check_for_bearer_token()}",
    'Accept': "*/*",
    'Host': "hallam.sci-toolset.com"
}

url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions"
response = requests.get(url, headers=headers, verify=False)
urls = [f'https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/{x["id"]}' for x in
        json.loads(response.text)["missions"]]
rs = (grequests.get(u, headers=headers, verify=False) for u in urls)
res = grequests.map(rs)
urls2 = [f'https://hallam.sci-toolset.com/discover/api/v1/products/{y["id"]}' for x in res for y in json.loads(x.text)["scenes"]]
rs = (grequests.get(u, headers=headers, verify=False) for u in urls2)
res = grequests.map(rs)
data = {"data": []}
for i in res:
    data["data"].append(json.loads(i.text))

