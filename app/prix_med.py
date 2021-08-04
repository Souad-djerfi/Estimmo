#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:15:03 2021
@author: simplon
"""

from app.base import Base
from sqlalchemy import Column, Integer, Float, String


class Prix_Median(Base):
    __tablename__ = 'prix_median'
    
    id_prix_median = Column(Integer, primary_key=True)
    
    longitude = Column(Float)
    latitude = Column(Float)
    housing_median_age = Column(Float)
    total_rooms = Column(Float)
    total_bedrooms = Column(Float)
    population = Column(Float)
    households = Column(Integer)
    median_income = Column(Float)
    median_house_value = Column(Integer)
    ocean_proximity = Column(Integer)
    ocean_proximity_str = Column(String)
    
    
    def __init__(self, longitude, latitude, housing_median_age, total_rooms,
                 total_bedrooms, population, households, median_income,
                 median_house_value, ocean_proximity, ocean_proximity_str):
        #self.id_prix_median=id_prix_median
        self.longitude = longitude
        self.latitude = latitude
        self.housing_median_age = housing_median_age
        self.total_rooms = total_rooms
        self.total_bedrooms = total_bedrooms
        self.population = population
        self.households = households
        self.median_income = median_income
        self.median_house_value = median_house_value
        self.ocean_proximity = ocean_proximity
        self.ocean_proximity_str = ocean_proximity_str