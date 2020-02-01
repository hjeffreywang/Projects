# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:47:43 2020

@author: User2
"""
import os
import json
import sqlalchemy

import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Integer
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template


app = Flask(__name__)


'''these are for preview purposes'''
import pandas as pd
import numpy as np


#==================================
#setup of the flask server


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resources/hawaii.sqlite"
db = SQLAlchemy(app)

engine = create_engine("sqlite:///resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

session = Session(engine)


Measurement = Base.classes.measurement
Station = Base.classes.station




# PREVIEWING with pandas



session = Session(engine)

ts = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

newest  = dt.datetime.strptime(ts[0],'%Y-%m-%d').date()
yearprevious = newest  - dt.timedelta(365)
start_date = yearprevious.strftime('%Y-%m-%d')
precip_data = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= start_date).\
                    order_by(Measurement.date).\
                    all()
#the query gives a tupled list!


precip_df= pd.DataFrame(precip_data)
precip_dict=precip_df.to_dict()

datelist=precip_df.loc[:,'date'].to_list()


dicts=[{tpl[0]:{'date':tpl[0], 'prcp':tpl[1]}} for tpl in precip_data]

prcipdatalistdict=[]
for tpl in precip_data:
    dateprcpdict={}
    dateprcpdict["date"]=tpl[0]
    dateprcpdict["prcp"]=tpl[1]
    prcipdatalistdict.append(dateprcpdict)
    
    
'''From the dataframe, we know we can jsonify the two columns'''


'''Creating the routing for the apis'''

@app.route("/")
def home():
    return (
        "Hawaii Precipitation and Weather API list<br/><br/>"
        
        "<a href='/api/precipitation' target='_blank'>/api/precipitation</a><br/>"
        
        "<a href='/api/stations' target='_blank'>/api/stations</a><br/>"
        
        "<a href='/api/tobs' target='_blank'>/api/tobs</a><br/>"
        
        "/api/&lt;start&gt; (Formatted as: <a href='/api/2016-08-23' target='_blank'>/api/2016-08-23</a>)<br/>"
        
        "/api/&lt;start&gt;/&lt;end&gt; (Formatted as: <a href='/api/2011-01-01/2011-12-31' target='_blank'>/api/2011-01-01/2011-12-31</a>)"
    )






@app.route("/api/precipitation")
def precipitation():
    session = Session(engine)

    ts = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    newest = dt.datetime.strptime(ts[0],'%Y-%m-%d').date()
    yearprevious = newest - dt.timedelta(365)
    start_date = yearprevious.strftime('%Y-%m-%d')
    precip_data = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= start_date).\
                    order_by(Measurement.date).\
                    all()
    prcipdatalistdict=[]
    for tpl in precip_data:
        dateprcpdict={}
        dateprcpdict["date"]=tpl[0]
        dateprcpdict["prcp"]=tpl[1]
        prcipdatalistdict.append(dateprcpdict)
   
    
    return jsonify(prcipdatalistdict)




@app.route("/api/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    #using iterative solution for a faster and native solution
    return jsonify([{tpl[0]:{'name':tpl[1], 'loc':{'lat':tpl[2], 'lng':tpl[3]}, 'elev':tpl[4]}} for tpl in stations])





@app.route("/api/tobs")
def tobs():
    session = Session(engine)

    ts = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    newest  = dt.datetime.strptime(ts[0],'%Y-%m-%d').date()
    start_date = newest  - dt.timedelta(365)
    tobs_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.station, Measurement.date).\
        all()
    return jsonify([{'station': tpl[0], 'date': tpl[1], 'tobs': tpl[2]} for tpl in tobs_data])







#this will return the temperature data for the route
def TemperatureDatas(start, end=None):
    session = Session(engine)

    ts = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    newest  = dt.datetime.strptime(ts[0],'%Y-%m-%d').date()
    start_date = newest  - dt.timedelta(365)
    
    
#Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start date
    # Query all the stations and for the given date. 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    #Json is a list of dictionaries, so we need to make an empty list and append
    
    temp_stats = []
    
    
    # Create dictionaries from the row data and append to a list of for the temperature data.
    for Tmin, Tmax, Tavg in results:
        temp_stats_dict = {}
        temp_stats_dict["Minimum Temp"] = Tmin
        temp_stats_dict["Maximum Temp"] = Tmax
        temp_stats_dict["Average Temp"] = Tavg
        temp_stats.append(temp_stats_dict)
    
    
    return jsonify(temp_stats)


@app.route("/api/<start>")
def start(start):
    return TemperatureDatas(start)



@app.route("/api/<start>/<end>")
def start_end(start, end):
    return TemperatureDatas(start, end)






if __name__ == "__main__":
    app.run()