import requests


def sci_discover_connect():
    return


def sci_discover_startup():
    return


def get_discover_bearer_code():
    url = 'https://hallam.sci-toolset.com/api/v1/token'
    payload = 'grant_type=password&username=hallam-d&password=b\P7?Cw#'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Host': "<hallam.sci-toolset.com>"
    }

    response = requests.request("POST", url, auth=("b2166e80-b732-4408-92f1-c53a523f2123", "79c0063046539713e1ad99c3a2ab24e2fd787bd37adca581e11cbc951fdac583"), data=payload, headers=headers, verify=False)
    print(response.text)
    return response
