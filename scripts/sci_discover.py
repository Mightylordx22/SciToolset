import json

import requests

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
                "b2166e80-b732-4408-92f1-c53a523f2123", "79c0063046539713e1ad99c3a2ab24e2fd787bd37adca581e11cbc951fdac583"),
                                        data=payload, headers=headers, verify=False)
            data = json.loads(response.text)
            save_bearer_token(data)
        use_bearer_token()
    except Exception as e:
        print(e)
