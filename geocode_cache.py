
import sqlite3
import os
import googlemaps
import math
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

DB_PATH = "geocache.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS geocache (
                   address TEXT PRIMARY KEY,
                   lat REAL,
                   lng REAL
               )'''
        )

def get_coordinates(address):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT lat, lng FROM geocache WHERE address = ?", (address,))
        row = cursor.fetchone()
        if row:
            return {"lat": row[0], "lng": row[1]}
        else:
            geocode_result = gmaps.geocode(address)
            if not geocode_result:
                return {"lat": 0.0, "lng": 0.0}
            location = geocode_result[0]["geometry"]["location"]
            conn.execute("INSERT INTO geocache (address, lat, lng) VALUES (?, ?, ?)",
                         (address, location["lat"], location["lng"]))
            return {"lat": location["lat"], "lng": location["lng"]}

def get_distance(origin, destination):
    # Straight-line distance fallback (not route-based)
    lat1, lon1 = origin["lat"], origin["lng"]
    lat2, lon2 = destination["lat"], destination["lng"]
    radius = 3958.8  # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) *         math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c
