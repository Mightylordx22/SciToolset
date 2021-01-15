class Mission:
    def __init__(self, mission_id, mission_name, takeoff, scenes):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.takeoff = takeoff
        self.scenes = scenes

    def get_mission_id(self):
        return self.mission_id

    def get_mission_name(self):
        return self.mission_name

    def get_scenes(self):
        return self.scenes

    def get_takeoff(self):
        return self.takeoff

    def set_mission_id(self, mission_id):
        self.mission_id = mission_id

    def set_mission_name(self, mission_name):
        self.mission_name = mission_name

    def set_scenes(self, scenes):
        self.scenes = scenes

    def set_takeoff(self, takeoff):
        self.takeoff = takeoff