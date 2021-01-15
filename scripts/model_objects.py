from scripts.api_functions import *
from scripts.mission import Mission
from scripts.scene import Scene

def model_mission_objects():
    all_missions = get_missions()
    all_mission_objects = []
    for k in all_missions['missions']:  # loop to get all missions from API
        scene_id_collector = []  # used to hold every scene id in a list from a single mission
        scene_object_collector = []  # used to hold scene data to model objects for
        scene_data = get_mission_search_data(k['name'])  # holds the scene data for current mission in loop
        list_iterator = 0
        while list_iterator < len(scene_data):  # loop to get every scene from every mission
            scene_id_collector.append(scene_data[list_iterator]['sceneId'])
            scene_name = get_scene(k['id'], scene_data[list_iterator]['sceneId'])
            scene_time = []
            scene_time.append(get_scene_time(k['id'], scene_data[list_iterator]['sceneId']))
            scene_coords = get_scene_coordinates(scene_data[list_iterator]['sceneId'])
            scene_object_collector.append(Scene(scene_data[list_iterator]['sceneId'], k['id'], scene_name, scene_time,
                                                scene_coords))
            list_iterator = list_iterator + 1
        all_mission_objects.append(Mission(k['id'], k['name'], k['aircraftTakeOffTime'], scene_object_collector))
    return all_mission_objects

total_missions = model_mission_objects()