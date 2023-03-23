#!/usr/bin/python3
"""Database storage engine for Airbnb project"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage():
    """Database storage engine class for Airbnb project"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the Database storage"""
        user = getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        password = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )

        if (getenv('HBNB_ENV') == 'test'):
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name (argument cls)"""
        if cls:
            return self.__session.query(cls).all()
        else:
            state_query = self.__session.query(State).all()
            city_query = self.__session.query(City).all()
            user_query = self.__session.query(User).all()
            amenity_query = self.__session.query(Amenity).all()
            place_query = self.__session.query(Place).all()
            review_query = self.__session.query(Review).all()

            return [state_query, city_query, user_query, amenity_query,
                    place_query, review_query]

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        1) Create all tables in the database,
        2) creates a new session for database access
        """
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False, )
        Session = scoped_session(session_factory)
        self.__session = Session()
