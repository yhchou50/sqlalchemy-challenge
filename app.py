# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

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
# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
    		f"Welcom to the weather page <br/>"
    		f"/api/v1.0/precipitation <br/>"
    		f"/api/v1.0/stations <br/>"
    		f"/api/v1.0/tobs <br/>"
    		)



@app.route("/api/v1.0/stations")
def station():
    result = session.query(Station.station).all()
    st_list = [row[0] for row in result]
    return jsonify (st_list)


@app.route("/api/v1.0/tobs")

def tobs():
    tobs_1 = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobs_1))
    return jsonify (tobs_list)

@app.route("/api/v1.0/tstats/<start>/<end>")
@app.route("/api/v1.0/tstats/<start>")
def tstats(start, end=None):
    if not end:
        end = dt.date.max
    temp_stats = session.query(Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()
    temp_stat_list = list(np.ravel(temp_stats))
    return jsonify (temp_stat_list)




if __name__ == "__main__":
    app.run(debug=True)