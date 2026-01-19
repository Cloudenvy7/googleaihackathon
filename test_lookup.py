import os
from src.fetcher import ArchitecturalFetcher

# Initialize the fetcher
fetcher = ArchitecturalFetcher()

# Test the Roosevelt address that failed in the UI
test_address = "11520 Roosevelt Way NE"
print(f"🔎 Testing lookup for: {test_address}")

basic_info = fetcher.resolve_address(test_address)

if basic_info:
    print(f"✅ SUCCESS! Found Parcel:")
    print(f"   Address: {basic_info.get('ADDR_FULL')}")
    print(f"   PIN: {basic_info.get('PIN')}")
    
    # Now test the deep city data pull
    print(f"⛏️ Attempting deep data pull...")
    rich_data = fetcher.fetch_architectural_data(basic_info)
    print(f"   Zoning Found: {rich_data.get('ZONING') or rich_data.get('zoning')}")
    print(f"   Data Source: {rich_data.get('DATA_SOURCE')}")
else:
    print("❌ FAIL: Still could not find parcel. Checking King County Resolver direct response...")
