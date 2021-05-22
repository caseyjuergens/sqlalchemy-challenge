import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy.sql.selectable import DeprecatedSelectBaseGenerations

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """Available API Routes"""
    return(
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

#################################################
@app.route("/api/v1.0/precipitation")
#covert query results to a dict using date as the key and prcp as the value
#return json of your dict
def precipitation():
    """Returns precipitation data """
    #create session link
    session=Session(engine)
    #query results to a dict
    prcp_results= session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcps= []
    for prcp in prcp_results:
        prcp_dict={}
        prcp_dict['Date']= Measurement.date
        prcp_dict['PRCP']= Measurement.prcp
        prcps.append(prcp_dict)

    return jsonify(prcps)


#################################################
@app.route("/api/v1.0/stations")
#return a json of stations from dataset
def stations():
    """visible comment"""
    session=Session(engine)
    station_results= session.query(Station.station, Station.name).all()
    session.close()
    
    return jsonify(station_results)


#################################################
@app.route("/api/v1.0/tobs")
#query dates and temp observations of the most active station for the last year of data
#return a json list of temp observations (TOBS) for the previous year
def tobs():
    """visible comment"""
    session= Session(engine)
    most_active= 'USC00519281'
    tob_results= session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.date> '2016-8-23').filter(Measurement.station == most_active).\
        order_by(Measurement.date).all()
    return jsonify(tob_results)


#################################################
#@app.route("/api/v1.0/<start>")
#return a json of min/max/avg temp for a given start or start-end range
#when given the start only, calculate the TMIN, TAVG, and TMAX for all dates greater
#---than or equal to the start date




#@app.route("/api/v1.0/<start>/<end>")
#when given the start and end date, calculate the TMIN, TAVG, and TMAX for dates
#---between the start and end date

if __name__ == '__main__':
    app.run(debug=True)