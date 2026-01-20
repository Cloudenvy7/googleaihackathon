import os
import uuid
import json
import requests
from datetime import datetime
from confluent_kafka import Producer

# SEATTLE GIS REPOS
URL_L0 = "https://services.arcgis.com/ZO977sSpxYbk3ZJu/arcgis/rest/services/Current_Land_Use_Zoning_Detail/FeatureServer/0/query"
URL_L2 = "https://services.arcgis.com/ZO977sSpxYbk3ZJu/arcgis/rest/services/Zoned_Development_Capacity_2016/FeatureServer/2/query"

class ArchitecturalFetcher:
    def __init__(self):
        conf = {
            'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': os.getenv('SASL_USERNAME'),
            'sasl.password': os.getenv('SASL_PASSWORD'),
        }
        self.producer = Producer(conf) if os.getenv('SASL_USERNAME') else None
        self.topic = "site.fetch.completed"

    def execute_major_pull(self, pin, address_input):
        trace_id = str(uuid.uuid4())
        action_ts = datetime.utcnow().isoformat() + "Z"
        
        l0_data = self._query(URL_L0, pin)
        l2_data = self._query(URL_L2, pin)

        # Standardizing fields to ensure NR3 is captured regardless of layer field names
        zoning = l0_data.get("ZONING") or l0_data.get("ZONING_CLASSIFICATION") or "UNKNOWN"

        ingestible = {
            "project_address": address_input.upper(),
            "zoning_designation": zoning,
            "lot_area_sqft": l2_data.get("LAND_SQFT", 0),
            "mha_zone": l2_data.get("MHA_ZONING", "None"),
            "resolution_method": "Multi_Layer_Deterministic_Merge_v3.4"
        }

        audit_envelope = {
            "audit_metadata": {"trace_id": trace_id, "timestamp": action_ts, "version": "3.4"},
            "ingestible_data": ingestible,
            "provenance_ledger": [
                {"source": "Layer_0_Current_Zoning", "purpose": "Zoning Name (NR3)", "raw": l0_data},
                {"source": "Layer_2_Capacity_2016", "purpose": "Physical Attributes", "raw": l2_data}
            ]
        }

        if self.producer:
            self.producer.produce(self.topic, key=pin, value=json.dumps(audit_envelope))
            self.producer.flush()
        
        return audit_envelope

    def _query(self, url, pin):
        params = {"where": f"PIN = '{pin}'", "outFields": "*", "f": "json"}
        try:
            resp = requests.get(url, params=params, timeout=10)
            features = resp.json().get("features", [])
            return features[0].get("attributes", {}) if features else {}
        except:
            return {}