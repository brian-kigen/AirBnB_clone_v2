#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_engine
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models


if storage_engine == 'db':
    metadata = Base.metadata

    place_amenity = Table('place_amenity', metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if storage_engine == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", backref="place", cascade="delete")

        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False, overlaps="place_amenity")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter attribute reviews that returns the list of Review
               instances with place_id equals to the
               current Place.id => It will be the FileStorage
               relationship between Place and Review

               Returns:
                   list: list of Review instances with place_id equals
                   to the current Place.id
            """
            from models import storage
            linked_objs = []
            reviews = storage.all(Review)

            for key in reviews.values():
                if key.place_id == self.id:
                    linked_objs.append(key)
            return linked_objs

        @property
        def amenities(self):
            """
            Getter attribute amenities that returns the list of Amenity instances based on the
            attribute amenity_ids that contains all Amenity.id linked to the Place
            Returns:
                list: list of Amenity instances based on the
                attribute amenity_ids that contains all Amenity.id linked to the Place
            """
            from models import storage
            linked_objs = []
            amenities = storage.all(Amenity)

            for key in amenities.values():
                if key.id in self.amenity_ids:
                    linked_objs.append(key)
            return linked_objs

        @amenities.setter
        def amenities(self, amenity_obj):
            """
            handles append method for adding an Amenity.id to the
            attribute amenity_ids. This method should
            accept only Amenity object,
            otherwise, do nothing

            Args:
                amenity_obj: an instance of class Amenity
            Returns:
                nothing
            """
            if amenity_obj is not None:
                if isinstance(amenity_obj, Amenity):
                    if amenity_obj.id not in self.amenity_ids:
                        self.amenity_ids.append(amenity_obj.id)
