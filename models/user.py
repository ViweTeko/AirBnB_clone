#!/usr/bin/python3

"""This module creates a User class"""

from models.basemodel import BaseModel


class User(BaseModel):
    """This class manages user objects"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""