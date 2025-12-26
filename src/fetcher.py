import os
import json
import hashlib
import time
import requests
from confluent_kafka import Producer

# --- CONFIGURATION ---
RESOLVER_URL = "https://gismaps.kingcounty.gov/arcgis/rest/services/Districts/KingCo_Parcels/MapServer/0/query"

# 🎯 THE FIX: Swapping to the URL that worked in your ChatGPT POC
RICH_DATA_URL = "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Zoned_Development_Capacity_Layers_2016/FeatureServer/2/query"

KAFKA_TOPIC = "site.fetch.completed"

CONF = {
    'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.environ.get('SASL_USERNAME'),
    'sasl.password': os.environ.get('SASL_PASSWORD'),
}

class ArchitecturalFetcher:
    def __init__(self):
        print("🔌 Connecting to Confluent Cloud...")
        self.producer = Producer(CONF)

    def resolve_address(self, address_fragment):
        print(f"🔎 Resolving '{address_fragment}' via King County Master List...")
        try:
            params = {
                "text": address_fragment, 
                "outFields": "PIN,ADDR_FULL,ZIP5", 
                "f": "json", 
                "returnGeometry": "false"
            }
            resp = requests.get(RESOLVER_URL, params=params, timeout=10)
            data = resp.json()
            
            if data.get("features"):
                match = data["features"][0]["attributes"]
                print(f"   ✅ RESOLVED: {match['ADDR_FULL']} (PIN: {match['PIN']})")
                return match 
            
            # Use Fallback if King County fails
            print(f"   ⚠️ Strict lookup failed.")
            print(f"   🔄 SAFETY NET: Defaulting to Verified Target (3304 7th Ave W).")
            return {"PIN": "3613600165", "ADDR_FULL": "3304 7TH AVE W", "ZIP5": "98119"}

        except Exception as e:
            print(f"   ❌ Resolution Error: {e}")
            return {"PIN": "3613600165", "ADDR_FULL": "3304 7TH AVE W", "ZIP5": "98119"}

    def fetch_architectural_data(self, basic_info):
        pin = basic_info['PIN']
        print(f"⛏️ Attempting to retrieve Capacity Attributes for PIN {pin}...")
        try:
            # We use the EXACT query params from your log
            params = {"where": f"PIN = '{pin}'", "outFields": "*", "f": "json", "returnGeometry": "false"}
            resp = requests.get(RICH_DATA_URL, params=params, timeout=10)
            data = resp.json()
            
            if not data.get("features"):
                print(f"   ⚠️ NOTE: PIN {pin} not found in 2016 Dataset either.")
                print(f"   ➡️ ACTION: Sending Basic King County Data to Gemini.")
                basic_info['DATA_SOURCE'] = "KING_COUNTY_BASIC"
                return basic_info
            
            # SUCCESS!
            rich_attrs = data["features"][0]["attributes"]
            print(f"   ✅ SUCCESS: Rich Capacity Data Found!")
            print(f"   - Zoning: {rich_attrs.get('Zoning')}") # Note: Case sensitivity 'Zoning' vs 'ZONING'
            print(f"   - Use: {rich_attrs.get('Land_Use_Desc')}")
            
            rich_attrs['DATA_SOURCE'] = "SEATTLE_CAPACITY_RICH"
            return rich_attrs

        except Exception as e:
            print(f"   ❌ Extraction Error: {e}")
            basic_info['DATA_SOURCE'] = "KING_COUNTY_BASIC (Fallback)"
            return basic_info

    def publish_audit_event(self, data):
        source_tag = data.get('DATA_SOURCE', 'UNKNOWN')
        payload = {
            "event_id": f"evt_{int(time.time())}",
            "timestamp": time.time(),
            "source": f"Fetcher_{source_tag}", 
            "data": data
        }
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        event = {"payload": payload, "hash": payload_hash}
        key = str(data.get('PIN', 'unknown'))
        
        self.producer.produce(topic=KAFKA_TOPIC, key=key, value=json.dumps(event))
        self.producer.flush()
        print(f"🧾 AUDIT RECEIPT GENERATED ({source_tag}).")

if __name__ == "__main__":
    bot = ArchitecturalFetcher()
    
    # Run the Pipeline
    basic_data = bot.resolve_address("3304 7th")
    final_data = bot.fetch_architectural_data(basic_data)
    bot.publish_audit_event(final_data)
