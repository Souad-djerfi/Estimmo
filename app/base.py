#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:45:44 2021

@author: simplon
"""

# pip install psycopg2-binary
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker


d={'user':'Simplon',
   'pwd':'Simplon2021',
   'host':'localhost'}

db_string = "postgresql://"+d['user']+":"+d['pwd']+"@"+d['host']+':5432/housing'

engine = create_engine(db_string)


Session = sessionmaker(bind=engine)

Base = declarative_base()