#!/usr/bin/python3
""" State Module for HBNB project """
from models import storage
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship('City', backref='state',
                          cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """ returns the list of City instances
        with state_id equals to the current State.id"""
        from models.city import City
        cities_dict = storage.all(City)
        return [obj for obj in cities_dict.values() if obj.state_id == self.id]
