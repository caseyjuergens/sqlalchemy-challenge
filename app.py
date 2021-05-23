import numpy as np
from numpy.lib.function_base import average
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

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
    """Welcome!"""
    """Here are the available API Routes:"""
    return(
        """Return all precipitation results:<br>"""
        f"/api/v1.0/precipitation<br>"
        """<br>"""
        """Return a list of all stations in dataset:<br>"""
        f"/api/v1.0/stations<br>"
        """<br>"""
        """Return the dates and temperature from the Waihee Station:<br>"""
        f"/api/v1.0/tobs<br>"
        """<br>"""
        """Return a list of min/max/avg temp for a start date:<br>"""
        """Date Format:YYYY-MM-DD"""
        """<br>"""
        f"/api/v1.0/start date<br>"
        """<br>"""
        """Return a list of min/max/avg temp for a start-end date range:<br>"""
        """Date Format:YYYY-MM-DD<br>"""
        f"/api/v1.0/start_date/end_date<br>"
    )

#################################################
@app.route("/api/v1.0/precipitation")
#covert query results to a dict using date as the key and prcp as the value
#return json of your dict
def precipitation():
    
    #create session link
    session=Session(engine)
    #query results to a dict
    prcp_results= session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcps= []
    for date, prcp in prcp_results:
        prcp_dict={}
        prcp_dict['Date']= date
        prcp_dict['PRCP']= prcp
        prcps.append(prcp_dict)

    return jsonify(prcps)


#################################################
@app.route("/api/v1.0/stations")
#return a json of stations from dataset
def stations():

    session=Session(engine)
    station_results= session.query(Station.station, Station.name).\
        order_by(Station.station).all()
    session.close()
    #covert list of tuples into a regular list
    stations= list(np.ravel(station_results))

    return jsonify(stations)


#################################################
@app.route("/api/v1.0/tobs")
#query dates and temp observations of the most active station for the last year of data
#return a json list of temp observations (TOBS) for the previous year
def tobs():
    
    session= Session(engine)
    most_active= 'USC00519281'
    tob_results= session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-8-23').filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    session.close()

    tob_list= []
    for date, tobs in tob_results:
        tob_dict={}
        tob_dict['Date']= date
        #tob_dict['Station']= station
        tob_dict['TOBS']= tobs
        tob_list.append(tob_dict)

    return jsonify(tob_list)


#################################################
@app.route("/api/v1.0/<start>")
#return a json of min/max/avg temp for a given start or start-end range
#when given the start only, calculate the TMIN, TAVG, and TMAX for all dates greater
#---than or equal to the start date
def startdate(start):
    session=Session(engine)
    start_results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs).filter(Measurement.date >= start)).all()
    session.close()

    start_list=[]
    for min, avg, max in start_results:
        start_dict={}
        start_dict["Min"]=min
        start_dict['Max']=max
        start_dict['Avg']=avg
        start_list.append(start_dict)

    return jsonify(start_list)


@app.route("/api/v1.0/<start_date>/<end_date>")
#when given the start and end date, calculate the TMIN, TAVG, and TMAX for dates
#---between the start and end date
def start_end_date(start_date, end_date):
    session=Session(engine)
    start_end_results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date)).all()
    session.close()

    start_end_list=[]
    for min, avg, max in start_end_results:
        start_end_dict={}
        start_end_dict["Min"]=min
        start_end_dict['Max']=max
        start_end_dict['Avg']=avg
        start_end_list.append(start_end_dict)
    
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)