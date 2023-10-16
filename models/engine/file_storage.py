#!/usr/bin/python3
"""Define class FileStorage"""
import json


class FileStorage(object):
    """Define class FileStorage"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Function to return var __objects

        Returns:
            dict: list of objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id

        :rtype: object
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)

        :rtype: object
        """
        new = {}
        with open(self.__file_path, "w") as my_file:
            for k, v in FileStorage.__objects.items():
                new.update({k: v.to_dict()})
            my_file.write(json.dumps(new))

    def reload(self):
        """deserializes the JSON file to __objects

        :rtype: object
        """
        if self.__file_path is not None:

            try:
                with open(self.__file_path) as f:
                    from models.base_model import BaseModel
                    from models.user import User
                    from models.state import State
                    from models.city import City
                    from models.amenity import Amenity
                    from models.place import Place
                    from models.review import Review
                    new_dict = json.loads(f.read())
                    for key, value in new_dict.items():
                        class_name = value.get("__class__")
                        obj = eval(class_name + "(**value)")
                        FileStorage.__objects[key] = obj
            except IOError:
                pass