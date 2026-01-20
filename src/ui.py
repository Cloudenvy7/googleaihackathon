import streamlit as st
from auditor import AuditorAgent
from fetcher import ArchitecturalFetcher

# VERSION CONTROL
APP_VERSION = "3.4"

st.set_page_config(page_title=f"Pre-Permit AI v{APP_VERSION}", page_icon="🏗️", layout="wide")

# SIDEBAR PANEL
with st.sidebar:
    st.title("🛡️ Project Shield")
    st.write(f"**Version:** {APP_VERSION}")
    st.write("**Mode:** Success-Path Resolution")
    st.divider()
    st.info("Locked to the HouseNum%Street% wildcard pattern proven in the POC.")

st.title("🏗️ Pre-Permit AI: Agentic Property Auditor")
st.caption("Deterministic GIS Resolution & Traceable Ingestion")

# Instance Management
if 'auditor' not in st.session_state:
    st.session_state.auditor = AuditorAgent()
if 'fetcher' not in st.session_state:
    st.session_state.fetcher = ArchitecturalFetcher()

address = st.text_input("Property Address", "11520 Roosevelt Way NE")

if st.button("🚀 Run Major Audit"):
    with st.spinner(f"v{APP_VERSION} performing GIS Handshake..."):
        # STEP 1: RESOLVE PIN
        result = st.session_state.auditor.find_pin(address)
        
        if isinstance(result, str) and not result.startswith("ERROR"):
            pin = result
            # STEP 2: FETCH DATA
            res = st.session_state.fetcher.execute_major_pull(pin, address)
            data = res['ingestible_data']
            
            st.success(f"✅ Verified PIN: {pin}")

            # MAIN METRICS
            st.write("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Zoning", data['zoning_designation'])
                st.caption("Source: City of Seattle Layer 0")
            with col2:
                st.metric("Lot Area", f"{int(data.get('lot_area_sqft', 0)):,} sqft")
                st.caption("Source: City of Seattle Layer 2")
            with col3:
                st.metric("MHA Zone", data.get('mha_zone', 'None'))

            # AUDIT TRAIL
            with st.expander("🔍 Immutable Traceability Ledger"):
                st.write(f"Verified via King County eRealProperty: {st.session_state.auditor.verification_url}")
                st.json(res)
        else:
            st.error(f"❌ {result if result else 'Resolution Failed'}")