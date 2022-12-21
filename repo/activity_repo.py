from model.activity import Activity
from typing import List

import json

class ActivityRepository(object):
    __file_path: str

    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path

    def get_activities(self) -> List[Activity]:
        try:
            with open(self.__file_path, "r") as fp:
                return json.loads(fp.read())
        except Exception as e:
            print(f"An error occured getting activities {e}")
            return []

    def save_activities(self, activities: List[Activity]) -> None:
        
        with open(self.__file_path, "w+") as file:
            json.dump()
    
    def add_activity(self, activity: Activity) -> bool:
        activities = self.get_activities()
        
        if (len(list(filter(lambda act: act.activity_name == activity.activity_name, activities))) > 0):
            return False

        activities.append(activity)
        self.save_activities(activities)
        return True