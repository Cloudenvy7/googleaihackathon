import requests

class AuditorAgent:
    def __init__(self):
        self.verification_url = ""
        self.last_metadata = None 

    def find_pin(self, address_input):
        try:
            # 1. Clean and Split as per the ChatGPT POC
            # Removes 'Seattle', commas, and extra spaces
            clean_addr = address_input.upper().replace('SEATTLE', '').replace(',', '').strip()
            parts = clean_addr.split()
            if len(parts) < 2:
                return "ERROR: Enter both house number and street (e.g., 11520 Roosevelt)"
                
            house_num = parts[0]
            street_keyword = parts[1] # e.g., 'ROOSEVELT'
            
            resolver_url = "https://gismaps.kingcounty.gov/arcgis/rest/services/Districts/KingCo_Parcels/MapServer/0/query"
            
            # The 'Victory' logic: HouseNum%StreetKeyword%
            # This matches '11520 ROOSEVELT WAY NE' perfectly in the King County index
            where_clause = f"ADDR_FULL LIKE '{house_num}%{street_keyword}%'"
            
            params = {
                'where': where_clause,
                'outFields': 'PIN, ADDR_FULL',
                'f': 'json',
                'returnGeometry': 'false'
            }

            response = requests.get(resolver_url, params=params, timeout=10)
            data = response.json()

            if data.get("features") and len(data["features"]) > 0:
                attr = data["features"][0]["attributes"]
                pin = attr["PIN"]
                self.verification_url = f"http://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={pin}"
                return pin
            
            return f"ERROR: No parcel match for '{house_num}%{street_keyword}%'"
        except Exception as e:
            return f"ERROR: GIS Connection Failure ({str(e)})"