import requests
import json
import jsonpath_rw_ext as jp

host_name = "hallam.sci-toolset.com"


def get_access_token():
    url = 'https://hallam.sci-toolset.com/api/v1/token'
    payload = 'grant_type=password&username=hallam-d&password=b\P7?Cw#'

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Host': host_name
    }

    response = requests.request("POST", url, auth=("b2166e80-b732-4408-92f1-c53a523f2123",
                                                   "79c0063046539713e1ad99c3a2ab24e2fd787bd37adca581e11cbc951fdac583"),
                                data=payload, headers=headers, verify=False)
    json_file = response.json()

    token = json_file['access_token']
    return token


access_token = get_access_token()


def return_all_products():
    url = 'https://hallam.sci-toolset.com/discover/api/v1/products/search'

    payload = '{"size":10, "keywords":""}'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token,
        'Accept': "*/*",
        'Host': host_name
    }

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)

    json_file = response.json()
    all_products = json_file
    return all_products


def retrieve_metadata(product_id):
    url = 'https://hallam.sci-toolset.com/discover/api/v1/products/' + product_id

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token,
        'Accept': "*/*"
    }

    response = requests.get(url, headers=headers, verify=False)

    json_data = json.loads(response.text)

    return ("Four-Corner Coordinates: {}".format(jp.match("$.product.result.footprint.coordinates[*]", json_data)))


def get_missions():
    url = 'https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions'

    payload = {}
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + access_token,
        'Accept': "*/*"
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    missions = json_file
    return missions


def get_specified_mission():
    url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/38235891-d3b3-4e88-be74-e5076c665db2"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    specified_mission = json_file
    return specified_mission


def mission_footprint(mission):
    url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/" + mission + "/footprint"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    footprint = json_file
    return footprint


def get_scene_times(scene_id):
    url = "https://hallam.sci-toolset.com/discover/api/v1/products/" + scene_id

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    all_times = []
    json_file = response.json()
    time_data = json_file
    all_times.append(time_data['product']['result']['objectstartdate'])
    all_times.append(time_data['product']['result']['objectenddate'])
    return all_times


def get_scene_coordinates(scene_id):
    url = "https://hallam.sci-toolset.com/discover/api/v1/products/" + scene_id

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    coordinates = json_file
    return coordinates['product']['result']['footprint']['coordinates']


def get_mission_search_data(mission_name):
    url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/search?keyword=" + mission_name

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    search_data = json_file
    return search_data['results']


def get_scene(mission_id, scene_id):  # scene name
    url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/" + mission_id + "/scene/" + scene_id + "/frames"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    scene_data = json_file
    return scene_data['scenes'][0]['name']


def get_scene_time(mission_id, scene_id):  # scene name
    url = "https://hallam.sci-toolset.com/discover/api/v1/missionfeed/missions/" + mission_id + "/scene/" + scene_id + "/frames"

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    scene_data = json_file
    return scene_data['scenes'][0]['firstFrameTime']


def get_scene_footprint(scene_id):
    url = "https://hallam.sci-toolset.com/discover/api/v1/products/" + scene_id

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    json_file = response.json()
    scene_footprint = json_file
    return scene_footprint['product']['result']['footprint']['coordinates']
