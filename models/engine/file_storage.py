#!/usr/bin/python3

"""This module is for FileStorage class"""
from datetime import datetime
import json
import os


class FileStorage:
    """This class stores and retrieves data"""

    __file_path = "file.json"
    __obects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__obects
    
    def attributes(self):
        """Returns valid attributes with their types for classname"""
        attributes = {
            "BaseModel":
            {
                "id": str,
                "created_at": datetime,
                "updated_at": datetime
            },
            "Amenity":
            {
                "name": str
            },
            "User":
            {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "Review":
            {
                "place_id": str,
                "user_id": str,
                "text": str
            },
            "State":
            {
                "name": str
            },
            "Place":
            {
                "city_id": str,
                "description": str,
                "user_id": str,
                "name": str,
                "price_by_night": int,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list
            }
        }

        return attributes
    
    def classes(self):
        """Returns a dictionary of valid classes with their references"""

        from models.amenity import Amenity
        from models.basemodel import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {
            "Amenity": Amenity,
            "BaseModel": BaseModel,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
        }
        return classes
    
    def new(self, obj):
        """Sets in __objects int obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__obects[key] = obj

    def reload(self):
        """Reloads the stored objects"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as a:
            ob_d = json.load(a)
            ob_d = {
                b: self.classes()[c["__class__"]](**c)
                for b, c in ob_d.items()
                    }
            FileStorage.__obects = ob_d

    def save(self):
        """Serializes __objects to JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as a:
            d = {
                b: c.to_dict() for b, c in FileStorage.__obects.items()
            }
            json.dump(d, a)