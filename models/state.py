#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models import storage_engine
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if storage_engine == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        @property
        def cities(self):
            from models import storage
            # list of related instances between city and state
            linked_objs = []
            cities = storage.all(City)

            for key in cities.values():
                if key.state_id == self.id:
                    linked_objs.append(key)
            return linked_objg
