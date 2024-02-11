#!/usr/bin/python3

"""This module initializes the package"""

from models.engine.file_storage import FilesStorage

storage = FilesStorage()
storage.reload()
