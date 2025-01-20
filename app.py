import aiohttp        # async http req 
# postgresql- ACID(ATOMICITY,CONSISTENCY,ISOLATION,DUARABILITY -FOR TRANSACTIONS)
# SUPPORTS JSON DATA AND GEOSPATIAL DATA
# SCALABLE,RIGID unlike mongo(generally for semi-structured data) AND ADVANCED QUERIES 
# data was structured TABLES- MEASUREMENTS, LOCATIONS

from flask import Flask, jsonify, request # web apps
from dotenv import load_dotenv # storing env vars
import os # read env vars
from flask_cors import CORS # cross origin resource sharing-accept requests from diff domains
from flask_sqlalchemy import SQLAlchemy # orm FOR SQL(LIKE PRISMA)
from datetime import datetime # WORK WITH DATES AND TIMES

# loading env vars
load_dotenv()

# initialised flask 
app = Flask(__name__)

CORS(app)

# sets url for db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db MODELS DEFINED
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    measurements = db.relationship('Measurement', backref='location', lazy=True) 
    # ESTABLISHING RELATIONSHIP-1( TO MANY)... lazy loading is used to load data only when needed

    def __repr__(self):
        return f"<Location {self.city}, {self.country}>"

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"<Measurement {self.parameter} - {self.value} {self.unit}>"

OPENAQ_API_URL = "https://api.openaq.org/v2/latest"
API_KEY = os.getenv("API_KEY")

# to fetch data from openaq api
async def fetch_data(session, params, headers):
    async with session.get(OPENAQ_API_URL, headers=headers, params=params) as response: # make an http get request
        response.raise_for_status() # ERROR HANDLED
        data = await response.json() # RESPONSE PARSED IN JSON   
        print(f"Fetched data: {data}") 
        return data

# CHECKS IF DATA IS PRESENT/ITERATES THROUGH DATA AND UPDATES/INSERTS IN DB
async def process_data(data):
    if not data or 'results' not in data:
        print("No data to process.")
        return

    # List of cities to update
    existing_cities = ["Hyderabad", "Chennai", "Delhi", "Kolkata", "Mumbai", "Kanpur"]

    for result in data['results']:
        city = result.get('city')
        country = result.get('country')
        latitude = result.get('coordinates', {}).get('latitude')
        longitude = result.get('coordinates', {}).get('longitude')

        if not city or not country:
            print(f"Skipping entry with missing city or country: {result}")
            continue

        # Ensure that the city name is correct and meaningful
        if city.lower() == "india":
            city = result.get('location', 'Unknown')

        print(f"Processing: City={city}, Country={country}, Latitude={latitude}, Longitude={longitude}")

        # Only process cities in India
        if country == "IN" and city:
            location = Location.query.filter_by(city=city, country=country).first()

            if location:
                if city in existing_cities:
                    # Update existing city data
                    location.latitude = latitude
                    location.longitude = longitude
                    db.session.commit()
                    print(f"Updated location: {location}")

                # Delete old measurements for this location
                Measurement.query.filter_by(location_id=location.id).delete()
            else:
                # Insert new city data
                location = Location(city=city, country=country, latitude=latitude, longitude=longitude)
                db.session.add(location)
                db.session.commit()
                print(f"Added new location: {location}")

            for measurement in result.get('measurements', []):
                parameter = measurement['parameter']
                value = measurement['value']
                unit = measurement['unit']
                timestamp = datetime.strptime(measurement['lastUpdated'], "%Y-%m-%dT%H:%M:%S+00:00")

                measurement_entry = Measurement(
                    parameter=parameter,
                    value=value,
                    unit=unit,
                    timestamp=timestamp,
                    location=location
                )
                db.session.add(measurement_entry)

            db.session.commit()
            print(f"Added/Updated measurements for location: {location.city}")
        else:
            print(f"Skipping non-IN country or missing city: {country}, {city}")

# to dump data in chunks of 1000 entries/useful in usecases where data is very large to process in single time
async def dump_data_in_chunks():
    params = {"country": "IN", "limit": 1000}
    headers = {"Accept": "application/json", "X-API-Key": API_KEY}

    # creating async session for http req
    async with aiohttp.ClientSession() as session:
        page = 1 # page param for pagination(doc divided among pages)
        while True:
            params['page'] = page
            data = await fetch_data(session, params, headers)
            await process_data(data)
            
            if len(data['results']) < 1000:
                break
            
            page += 1

# route to dump data in chunks-1000 at a time
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Data dumped successfully into the database."}), 200

# avoiding 404 err
@app.route('/favicon.ico')
def favicon(): 
    return '', 204

# Route to get data from the database
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Query all measurements and related locations
        measurements = Measurement.query.join(Location).all()

        # Serialize data into a list of dictionaries
        data = []
        for measurement in measurements:
            data.append({
                "city": measurement.location.city,
                "country": measurement.location.country,
                "parameter": measurement.parameter,
                "value": measurement.value,
                "unit": measurement.unit,
                "timestamp": measurement.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })

        print(f"Retrieved {len(data)} measurements from the database.")
        return jsonify({"results": data}), 200
    except Exception as e:
        print(f"Error while fetching data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)