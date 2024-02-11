#!/usr/bin/python3

"""This module  creates a review class"""

from models.basemodel import BaseModel


class Review(BaseModel):
    """This class manages review objects"""

    place_id = ""
    user_id = ""
    text = ""
