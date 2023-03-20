#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from models import storage
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True)
    cur_date = datetime.utcnow()
    created_at = Column(DateTime, nullable=False, default=cur_date)
    updated_at = Column(DateTime, nullable=False, default=cur_date)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        new = None
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get('updated_at') is not None:
                kwargs['updated_at'] =\
                    datetime.strptime(
                        kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.now()
            if kwargs.get('created_at') is not None:
                kwargs['created_at'] =\
                    datetime.strptime(kwargs['created_at'],
                                      '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.now()
            if kwargs.get('__class__') is not None:
                del kwargs['__class__']

            if kwargs.get('id') is None:
                self.id = str(uuid.uuid4())
                new = True

            kwargs = dict_convert_no_value(kwargs)
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        object_dict = self.__dict__
        if object_dict.get('_sa_instance_state'):
            del object_dict['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, object_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """delete the current instance from the storage (models.storage)"""
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if dictionary.get('_sa_instance_state') is not None:
            del dictionary['_sa_instance_state']
        return dictionary


def dict_convert_no_value(kwargs):
    for key, value in kwargs.items():
        if key not in ['city_id', 'user_id', 'created_at', 'updated_at']\
                and type(value) not in [int, float, datetime]:
            if value.isnumeric():
                kwargs[key] = int(value)
            elif isfloat(value):
                kwargs[key] = float(value)

    return kwargs


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
