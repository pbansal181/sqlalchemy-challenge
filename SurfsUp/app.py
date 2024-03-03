# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement to get date and Precipitation values
    most_recent_date = "2017-08-23"
    year_ago_date = "2016-08-23"
    prcp_results = (session.query(measurement.date, measurement.prcp)
        .filter(and_(measurement.date >= year_ago_date, measurement.prcp.isnot(None)))
        .order_by(measurement.date)
        .all()
    )

    session.close()

    #converting the output in dictionary format
    prcp_dict = {date: prcp for date, prcp in prcp_results}
    return jsonify(prcp_dict)
    

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query to get list of stations
    all_stations = session.query(measurement.station).distinct().all()
    
    session.close()

    #Convert into normal list and then jsonify the output
    station_list = [station[0] for station in all_stations]
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most-active station for last year
    year_ago_date = "2016-08-23"
    
    temp_results = (session.query(measurement.date, measurement.tobs)
         .filter(and_(measurement.date >= year_ago_date, measurement.station == 'USC00519281'))
         .group_by(measurement.date)
         .order_by(measurement.date).all()
    )

    session.close()

    #Create a list of dictionaries
    obs_dates = []
    obs_temp = []
    for date, tobs in temp_results:
        obs_dates.append(date)
        obs_temp.append(tobs)
    temp_obs_dict = dict(zip(obs_dates, obs_temp))
    
    return jsonify(temp_obs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date for a specified date
    temp_values = (session.query(func.min(measurement.tobs).label('TMIN'),
            func.avg(measurement.tobs).label('TAVG'),
            func.max(measurement.tobs).label('TMAX'))
        .filter(measurement.date >= start).all()
    )

    session.close()

    #Convert the outputs into a dictionary and then return jsonify form
    temp_values_dict = {'TMIN': temp_values[0][0],
        'TAVG': temp_values[0][1],
        'TMAX': temp_values[0][2]
    }

    return jsonify(temp_values_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date for a specified date
    temp_values = (session.query(func.min(measurement.tobs).label('TMIN'),
            func.avg(measurement.tobs).label('TAVG'),
            func.max(measurement.tobs).label('TMAX'))
        .filter(and_(measurement.date >= start, measurement.date <= end)).all()
    )

    session.close()

    #Convert the outputs into a dictionary and then return jsonify form
    temp_values_dict = {'TMIN': temp_values[0][0],
        'TAVG': temp_values[0][1],
        'TMAX': temp_values[0][2]
    }

    return jsonify(temp_values_dict)

if __name__ == '__main__':
    app.run(debug=True)




































