import os
import json
import hashlib
import time
import requests
from confluent_kafka import Producer

# --- CONFIGURATION ---
# 1. The Resolver (King County - "The Phonebook")
RESOLVER_URL = "https://gismaps.kingcounty.gov/arcgis/rest/services/Districts/KingCo_Parcels/MapServer/0/query"

# 2. The Extractor (Seattle Capacity - "The Gold Mine")
RICH_DATA_URL = "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Zoned_Development_Capacity_by_Development_Site_Current/FeatureServer/2/query"

KAFKA_TOPIC = "site.fetch.completed"

# --- CONFLUENT CONFIG ---
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
        """Step 1: Get the PIN (The Key)."""
        print(f"🔎 Resolving '{address_fragment}' via King County Master List...")
        params = {
            "where": f"UPPER(ADDR_FULL) LIKE '%{address_fragment.upper()}%'",
            "outFields": "PIN,ADDR_FULL", 
            "f": "json", 
            "returnGeometry": "false"
        }
        try:
            resp = requests.get(RESOLVER_URL, params=params, timeout=10)
            data = resp.json()
            if data.get("features"):
                match = data["features"][0]["attributes"]
                print(f"   ✅ RESOLVED: {match['ADDR_FULL']} -> PIN: {match['PIN']}")
                return match['PIN']
            print(f"   ⚠️ Resolution Failed: No match for '{address_fragment}'")
            return None
        except Exception as e:
            print(f"   ❌ Resolution Error: {e}")
            return None

    def fetch_architectural_data(self, pin):
        """Step 2: Get the 65 Attributes (The Gold)."""
        print(f"⛏️ Extracting Capacity Attributes for PIN {pin} from FeatureServer/2...")
        
        fields = "*" # Get everything per PRD requirements
        
        params = {
            "where": f"PIN = '{pin}'",
            "outFields": fields,
            "f": "json",
            "returnGeometry": "false"
        }

        try:
            resp = requests.get(RICH_DATA_URL, params=params, timeout=10)
            data = resp.json()
            
            if not data.get("features"):
                print(f"   ⚠️ PIN {pin} not found in Zoned Development Capacity Layer.")
                return None
            
            attrs = data["features"][0]["attributes"]
            print(f"   ✅ DATA EXTRACTED: {len(attrs)} Attributes Found.")
            print(f"   - Zoning (Legacy): {attrs.get('ZONING')} (Matches PRD Logic)")
            print(f"   - Parcel Area: {attrs.get('PARCEL_AREA_SQ_FT')} sqft")
            print(f"   - Max FAR: {attrs.get('MAX_ALLOWED_FAR')}")
            return attrs

        except Exception as e:
            print(f"   ❌ Extraction Error: {e}")
            return None

    def publish_audit_event(self, data):
        """Step 3: Stamp the Truth onto the Ledger."""
        payload = {
            "event_id": f"evt_{int(time.time())}",
            "timestamp": time.time(),
            "source": "Seattle_Capacity_FeatureServer_2", 
            "schema_version": "v1_architectural",
            "data": data
        }
        # Hash for immutability check
        payload_str = json.dumps(payload, sort_keys=True)
        payload_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        
        event = {"payload": payload, "hash": payload_hash}
        
        # Send to Confluent
        key = str(data.get('PIN', 'unknown'))
        self.producer.produce(topic=KAFKA_TOPIC, key=key, value=json.dumps(event))
        self.producer.flush()
        print(f"🧾 AUDIT RECEIPT GENERATED.")
        print(f"   - Ledger Hash: {payload_hash}")

if __name__ == "__main__":
    bot = ArchitecturalFetcher()
    pin = bot.resolve_address("3304 7th Ave W")
    if pin:
        data = bot.fetch_architectural_data(pin)
        if data:
            bot.publish_audit_event(data)
        else:
            print("   ℹ️ NOTE: Property exists but has no Capacity Data (Valid per PRD).")
