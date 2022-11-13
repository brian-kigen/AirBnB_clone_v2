#!/usr/bin/python3
"""This module contains the class DBStorage which
is the database storage engine for the clone
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {'User': User, 'State': State, 'City': City,
           'Amenity': Amenity, 'Place': Place, 'Review': Review}


class DBStorage:
    """The class that defines the Database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name (argument cls)
        Args:
            cls: the name of the class passed as an argument
        Returns:
            dict: a dictionary of cls instances
        """
        if cls is None:
            obj = self.__session.query(State).all()
            obj.extend(self.__session.query(City).all())
            obj.extend(self.__session.query(User).all())
            obj.extend(self.__session.query(Place).all())
            obj.extend(self.__session.query(Review).all())
            obj.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            obj = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in obj}

    def new(self, obj):
        """
        add the object to the current database session
        Args:
            obj: the instance to add to the database
        Returns:
            nothing
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        Returns:
            nothing
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        Args:
            obj: the oobject to delete
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database (feature of SQLAlchemy)
        Talking to the database
        """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
