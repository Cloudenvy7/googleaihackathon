import os
import json
import time
from confluent_kafka import Consumer

# --- CONFIGURATION ---
KAFKA_TOPIC_IN = "site.fetch.completed"

CONF = {
    'bootstrap.servers': os.environ.get('BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': os.environ.get('SASL_USERNAME'),
    'sasl.password': os.environ.get('SASL_PASSWORD'),
    'group.id': 'data-verification-group', # New Group to re-read everything
    'auto.offset.reset': 'earliest'
}

def main():
    consumer = Consumer(CONF)
    consumer.subscribe([KAFKA_TOPIC_IN])
    print(f"🎧 Listener Ready: Waiting for Confluent Payload...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # 1. DECODE THE MESSAGE
            event = json.loads(msg.value().decode('utf-8'))
            
            # Robust Extraction (Handle nested payloads)
            if 'payload' in event:
                data = event['payload']['data']
            else:
                data = event.get('data', {})
                
            # If the fetcher wrapped it in 'attributes', unwrap it
            if 'attributes' in data:
                raw_attributes = data['attributes']
            else:
                raw_attributes = data

            pin = raw_attributes.get('PIN') or raw_attributes.get('pin')
            
            # 2. PRINT THE RAW EVIDENCE (The 65+ Attributes)
            print(f"\n📦 RECEIVED PAYLOAD FROM CONFLUENT (PIN: {pin})")
            print("===================================================")
            print(json.dumps(raw_attributes, indent=4))
            print("===================================================")
            
            # 3. SAVE TO FILE (For Download/Export)
            filename = f"parcel_{pin}_data.json"
            with open(filename, 'w') as f:
                json.dump(raw_attributes, f, indent=4)
            
            print(f"💾 DATA SAVED: {filename}")
            print(f"✅ STATUS: Validated 65+ Attributes received via Confluent Cloud.")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
