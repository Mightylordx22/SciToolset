class Scene:
    def __init__(self, scene_id, mission_id, scene_name, time, scene_coords):
        self.scene_id = scene_id
        self.mission_id = mission_id
        self.scene_name = scene_name
        self.time = time
        self.scene_coords = scene_coords

    def get_scene_id(self):
        return self.scene_id

    def get_mission_id(self):
        return self.mission_id

    def get_scene_name(self):
        return self.scene_id

    def get_scene_coords(self):
        return self.scene_coords

    def get_time(self):
        return self.time

    def set_scene_id(self, scene_id):
        self.scene_id = scene_id

    def set_mission_id(self, mission_id):
        self.mission_id = mission_id

    def set_scene_name(self, scene_name):
        self.scene_name = scene_name

    def set_scene_coords(self, scene_coords):
        self.scene_coords = scene_coords