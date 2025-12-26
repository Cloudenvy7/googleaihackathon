import os
import json
import hashlib
import time
import requests
from confluent_kafka import Producer

# --- CONFIGURATION ---
SEATTLE_GIS_URL = "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Zoned_Development_Capacity_by_Development_Site_Current/FeatureServer/2/query"
KAFKA_TOPIC = "site.fetch.completed"

# --- CONFLUENT CONFIG ---
CONF = {
    'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.environ.get('SASL_USERNAME'),
    'sasl.password': os.environ.get('SASL_PASSWORD'),
}

class SeattleGISFetcher:
    def __init__(self):
        print("🔌 Connecting to Confluent Cloud...")
        self.producer = Producer(CONF)

    def fetch_parcel_data(self, parcel_id: str):
        print(f"📡 Fetching Live Truth for PIN: {parcel_id} (3304 7th Ave W)...")
        params = {
            "where": f"PIN = '{parcel_id}'",
            "outFields": "*", 
            "f": "json",
            "returnGeometry": "true" 
        }

        try:
            response = requests.get(SEATTLE_GIS_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get("features"):
                print(f"⚠️  No records found for PIN {parcel_id}")
                return None
            
            feature = data["features"][0]
            attrs = feature["attributes"]
            
            print(f"✅ FOUND: Parcel {attrs.get('PIN')}")
            print(f"   - Target: 3304 7th Ave W (Residential Control)")
            print(f"   - Zoning: {attrs.get('ZONING')}")
            print(f"   - Lot Area: {attrs.get('PARCEL_AREA_SQ_FT')} sqft")
            return feature

        except Exception as e:
            print(f"❌ API FAILURE: {e}")
            return None

    def create_truth_event(self, parcel_data):
        payload = {
            "event_id": f"evt_{int(time.time())}",
            "timestamp": time.time(),
            "source": "SeattleGIS_FeatureServer_2",
            "data": parcel_data
        }
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        return {"payload": payload, "hash": payload_hash}

    def publish(self, event):
        try:
            key = str(event['payload']['data']['attributes']['PIN'])
            self.producer.produce(topic=KAFKA_TOPIC, key=key, value=json.dumps(event))
            self.producer.flush()
            print(f"🧾 AUDIT RECEIPT GENERATED.")
            print(f"   - Ledger Hash: {event['hash']}")
        except Exception as e:
            print(f"❌ KAFKA ERROR: {e}")

if __name__ == "__main__":
    # CONTROL VARIABLE: 3304 7th Ave W -> PIN 3613600165
    tool = SeattleGISFetcher()
    data = tool.fetch_parcel_data("3613600165")
    if data:
        event = tool.create_truth_event(data)
        tool.publish(event)
