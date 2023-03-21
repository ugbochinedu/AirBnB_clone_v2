#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""


from os import getenv

storage = None
if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

"""support for lines like `from models import *`
"""
if True:
    """
    module level import needs to be at the top of the file,
    hence this if block.
    Placed down here to avoid circular import clash with the modules
    below trying to import `storage` before it declared.
    """
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review
