#!/usr/bin/python3

"""This module creates a User class"""

from models.basemodel import BaseModel


class City(BaseModel):
    """A class for managing city objects"""

    state_id = ""
    name = ""
