import datetime
import json

import ciso8601
import grequests
import requests
import urllib3

urllib3.disable_warnings()
import time

from scripts.db_link import check_for_bearer_token, save_bearer_token, use_bearer_token


def sci_discover_connect():
    return


def sci_discover_startup():
    return


def auth_discover_bearer_token():
    try:
        api_token = check_for_bearer_token()
        if type(api_token) == bool:
            url = 'https://hallam.sci-toolset.com/api/v1/token'
            payload = 'grant_type=password&username=hallam-d&password=b\P7?Cw#'
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Accept': "*/*",
                'Host': "hallam.sci-toolset.com"
            }
            response = requests.request("POST", url, auth=(
                "b2166e80-b732-4408-92f1-c53a523f2123",
                "79c0063046539713e1ad99c3a2ab24e2fd787bd37adca581e11cbc951fdac583"),
                                        data=payload, headers=headers, verify=False)
            data = json.loads(response.text)
            save_bearer_token(data)
        else:
            use_bearer_token()
    except Exception as e:
        print(e)


def get_server_data(date_start, date_end):
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
    urls2 = [f'https://hallam.sci-toolset.com/discover/api/v1/products/{y["id"]}' for x in res for y in
             json.loads(x.text)["scenes"]]
    rs = (grequests.get(u, headers=headers, verify=False) for u in urls2)
    res = grequests.map(rs)
    data = {"data": []}
    if date_start == 0 and date_end == 0:
        for i in res:
            data["data"].append(json.loads(i.text))
        with open("data2.json", "w") as file:
            file.write(json.dumps(data))
    else:
        for i in res:
            start = int(str(json.loads(i.text)["product"]["result"]["objectstartdate"])[:-3])
            end = int(str(json.loads(i.text)["product"]["result"]["objectenddate"])[:-3])
            if start > time.mktime(ciso8601.parse_datetime(date_start).timetuple()) and end < time.mktime(ciso8601.parse_datetime(date_end).timetuple()):
                data["data"].append(json.loads(i.text))

    return data
