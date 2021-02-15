import json
import grequests
import requests
import urllib3

urllib3.disable_warnings()

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer cfebb766-4165-4db9-801f-0d5f32f241bf",
    'Accept': "*/*",
    'Host': "hallam.sci-toolset.com"
}
url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions"
response = requests.get(url, headers=headers, verify=False)
urls = [f'https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/{x["id"]}' for x in
        json.loads(response.text)["missions"]]
rs = (grequests.get(u, headers=headers, verify=False) for u in urls)
res = grequests.map(rs)
urls2 = [f'https://hallam.sci-toolset.com/discover/api/v1/products/{json.loads(x.text)["scenes"][0]["id"]}' for x in res]
rs = (grequests.get(u, headers=headers, verify=False) for u in urls2)
res = grequests.map(rs)
# data = {"data": []}
# for i in res:
#     data["data"].append(json.loads(i.text))
# with open("data2.json", "w") as file:
#     file.write(json.dumps(data, indent=4))
