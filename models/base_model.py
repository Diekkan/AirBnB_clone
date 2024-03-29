#!/usr/bin/python3
"""
Created class Base Model, attributes and methods.
"""
from datetime import date, datetime
import uuid
import models


class BaseModel:
    """
    Base Model

        Att:
        id: randomly generated id, unique for each instance.
        created_at: original time in which the instance was created.
        updated_at: this will update every time save method runs.

        Methods:
        __init__: instancing with or without dictionary.
        __str___: a string representation of an instance.
        save: updates the updated_at attr with the current datetime
        to_dict: returns a dictionary containing all keys/values of __dict__.
    """

    def __init__(self, *args, **kwargs):
        """ Instance constructor that can receive dictionary """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key in kwargs:
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime
                            (kwargs[key], "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, kwargs[key])
        else:
            models.storage.new(self)

    def __str__(self):
        """ String representation of instance"""
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """ updates public instance attribute updated_at"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Instance to dictionary"""
        new_dict = self.__dict__.copy()
        new_dict.update({'created_at': self.created_at.strftime
                        ("%Y-%m-%dT%H:%M:%S.%f"), 'updated_at':
                        self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                        '__class__': 'BaseModel'})
        return new_dict
