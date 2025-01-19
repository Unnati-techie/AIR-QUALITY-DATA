import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database connection
engine = create_engine('postgresql://unnati:unnati@localhost:5432/air_quality_db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Models
class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    measurements = relationship('Measurement', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location {self.city}, {self.country}>"

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"<Measurement {self.parameter} - {self.value} {self.unit}>"

# Function to generate random latitude and longitude
def generate_random_coordinates():
    return round(random.uniform(8.0, 37.0), 5), round(random.uniform(68.0, 97.0), 5)

# List of Indian cities to be added
cities = [
    "Bangalore", "Ahmedabad", "Pune", "Surat", "Jaipur", "Lucknow", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik",
    "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad",
    "Dhanbad", "Amritsar", "Navi Mumbai", "Prayagraj", "Howrah", "Ranchi", "Jabalpur", "Gwalior", "Coimbatore",
    "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Chandigarh", "Guwahati", "Noida", "Guntur", "Solapur",
    "Jalandhar", "Thiruvananthapuram", "Bhubaneswar", "Salem", "Warangal", "Mysore", "Bareilly", "Aligarh",
    "Moradabad", "Bhubaneswar", "Tiruchirappalli", "Tiruppur", "Gurgaon", "Kochi", "Dehradun", "Durgapur",
    "Asansol", "Nanded", "Kolhapur", "Ajmer", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri",
    "Jhansi", "Ulhasnagar", "Nellore", "Jammu", "Sangli-Miraj & Kupwad", "Belgaum", "Mangalore", "Ambattur",
    "Tirunelveli", "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala", "Davanagere", "Kozhikode",
    "Kurnool", "Rajpur Sonarpur", "Bokaro Steel City", "South Dumdum", "Bellary", "Patiala", "Gopalpur",
    "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatpara", "Panihati", "Latur", "Dhule", "Rohtak",
    "Korba", "Bhilwara", "Brahmapur", "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam", "Avadi",
    "Kadapa", "Kamarhati", "Saharanpur", "Bilaspur", "Shahjahanpur", "Satara", "Bijapur", "Rampur",
    "Shimoga", "Chandrapur", "Junagadh", "Thrissur", "Alwar", "Bardhaman", "Kulti", "Kakinada",
    "Nizamabad", "Parbhani", "Tumkur", "Khammam", "Ozhukarai", "Bihar Sharif", "Panipat", "Darbhanga",
    "Bally", "Aizawl", "Dewas", "Ichalkaranji", "Karnal", "Bathinda", "Jalna", "Eluru",
    "Barasat", "Kirari Suleman Nagar", "Purnia", "Satna", "Mau", "Sonipat", "Farrukhabad", "Durg",
    "Imphal", "Ratlam", "Hapur", "Arrah", "Anantapur", "Karimnagar", "Etawah", "Ambarnath",
    "North Dumdum", "Bharatpur", "Begusarai", "New Delhi", "Gandhidham", "Baranagar", "Tiruvottiyur", "Pondicherry",
    "Sikar", "Thoothukudi", "Rewa", "Mirzapur", "Raichur", "Pali", "Ramagundam", "Silchar",
    "Haridwar", "Vijayanagaram", "Tenali", "Nagercoil", "Sri Ganganagar", "Karawal Nagar", "Mango", "Thanjavur",
    "Bulandshahr", "Uluberia", "Katni", "Sambalpur", "Singrauli", "Nadiad", "Secunderabad", "Naihati",
    "Yamunanagar", "Bidhannagar", "Pallavaram", "Bidar", "Munger", "Panchkula", "Burhanpur", "Raurkela",
    "Kharagpur", "Dindigul", "Gandhinagar", "Hospet", "Nangloi Jat", "Malda", "Ongole", "Deoghar",
    "Chapra", "Haldia", "Khandwa", "Nandyal", "Morena", "Amroha", "Anand", "Bhind",
    "Bhalswa Jahangir Pur", "Madhyamgram", "Bhiwani", "Berhampur", "Ambala", "Morbi", "Fatehpur", "Raebareli",
    "Khora, Ghaziabad", "Chittoor", "Bhusawal", "Orai", "Bahraich", "Phusro", "Vellore", "Mehsana",
    "Raiganj", "Sirsa", "Danapur", "Serampore", "Sultan Pur Majra", "Guna", "Jaunpur", "Panvel",
    "Shivpuri", "Surendranagar Dudhrej", "Unnao", "Chinsurah", "Alappuzha", "Kottayam", "Machilipatnam", "Shimla",
    "Adoni", "Udupi", "Katihar", "Proddatur", "Mahbubnagar", "Saharsa", "Dibrugarh", "Jorhat",
    "Hazaribagh", "Hindupur", "Nagaon", "Sasaram", "Hajipur", "Giridih", "Tadepalligudem", "Karaikudi",
    "Kishanganj", "Jamuria", "Ballia", "Kavali", "Tadepalle", "Bhimavaram", "Kumbakonam", "Dehri",
    "Madanapalle", "Siwan", "Bettiah", "Guntakal", "Srikakulam", "Motihari", "Dharmavaram", "Gudivada",
    "Phagwara", "Pudukkottai", "Chittoor", "Suryapet"]

# Adding the cities to the database
starting_id = 1000
timestamp = datetime.strptime("2025-01-19 11:30:00", "%Y-%m-%d %H:%M:%S")

for city in cities:
    latitude, longitude = generate_random_coordinates()
    location = Location(id=starting_id, city=city, country="IN", latitude=latitude, longitude=longitude)
    session.add(location)
    
    pm25_value = random.randint(50, 180)
    measurement = Measurement(id=starting_id + 1000, parameter="pm25", value=pm25_value, unit="µg/m³", timestamp=timestamp, location=location)
    session.add(measurement)
    
    starting_id += 1

session.commit()

print("Data seeding complete.")
