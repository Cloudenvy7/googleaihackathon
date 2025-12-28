import os, json, time, requests
from confluent_kafka import Producer

API_URL = "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Zoned_Development_Capacity_Layers_2016/FeatureServer/2/query"

class ArchitecturalFetcher:
    def __init__(self):
        try:
            conf = {
                'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVERS'),
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': os.environ.get('SASL_USERNAME'),
                'sasl.password': os.environ.get('SASL_PASSWORD')
            }
            self.producer = Producer(conf) if os.environ.get('SASL_USERNAME') else None
        except:
            self.producer = None

    def fetch_architectural_data(self, pin):
        try:
            p = {"where": f"PIN = '{pin}'", "outFields": "*", "f": "json", "returnGeometry": "false"}
            res = requests.get(API_URL, params=p).json()
            if res.get("features"):
                return {k.lower(): v for k, v in res["features"][0]["attributes"].items()}
            return {"error": "PIN not found in Seattle dataset"}
        except:
            return {"error": "API Connection Failed"}

    def publish_audit_event(self, data):
        if self.producer:
            msg = {"timestamp": time.time(), "data": data}
            self.producer.produce(topic="site.fetch.completed", value=json.dumps(msg))
            self.producer.flush()
