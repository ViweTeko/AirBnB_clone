#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime
from models import storage


class BaseModel:
    """This class is the Base model for creating and managing instances
        in which all classes shall inherit
    """

    def __init__(self, *args, **kwargs):

        """Initializes an instance of the  base model
            Args:
                args: list of arguments
                kwargs: dictionary for keys/values
        """
        if kwargs is None and kwargs is not {}:
            for key in kwargs:
                if key is "created_at":
                    self.__dict__['created_at'] = datetime.strptime(
                        kwargs['created_at'], "%Y-%m-%dT%H:%H:%S.%f")
                elif key is "updated_at":
                    self.__dict__['updated_at'] = datetime.strptime(
                        kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

        def to_dict(self):
            """Returns a dictionary with all the keys and values of __dict__"""
            the_dict = self.__dict__.copy()
            the_dict['__class__'] = type(self).__name__
            the_dict['created_at'] = self.created_at.isoformat()
            the_dict['updated_at'] = self.updated_at.isoformat()

            return the_dict

        def save(self):
            """Public instance updated_at becomes updated"""

            self.updated_at = datetime.now()
            storage.save()

        def __str__(self):
            """Returns official string representation"""

            return "[{}] ({}) {}".
        format(type(self).__name__, self.id, self.__dict__)
