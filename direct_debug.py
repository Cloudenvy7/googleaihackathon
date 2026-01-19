import requests

# 1. The exact address we want
address = "11520 ROOSEVELT WAY NE"
# 2. The logic that worked in the ChatGPT POC
where = "ADDR_FULL LIKE '11520%ROOSEVELT%'"
url = "https://gismaps.kingcounty.gov/arcgis/rest/services/Districts/KingCo_Parcels/MapServer/0/query"

params = {
    "where": where,
    "outFields": "PIN,ADDR_FULL",
    "f": "json",
    "returnGeometry": "false"
}

print(f"📡 Sending Request to King County...")
resp = requests.get(url, params=params)
print(f"🌍 Status Code: {resp.status_code}")

data = resp.json()
if "features" in data and len(data["features"]) > 0:
    print("✅ DATA FOUND!")
    print(data["features"][0])
else:
    print("❌ NOTHING FOUND.")
    print("Full Response from Server:", data)
