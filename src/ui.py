import streamlit as st
from auditor import AuditorAgent
from fetcher import ArchitecturalFetcher

# Page Configuration for a Professional Dashboard
st.set_page_config(
    page_title="Pre-Permit AI v3.0 | Gemini 3",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for a clean Hackathon look
st.markdown("""
    <style>
    .metric-container { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
    .source-link { font-size: 0.8rem; color: #555; }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ Pre-Permit AI: Agentic Property Auditor")
st.caption("Powered by Gemini 3 Flash Preview & Google Search Grounding")

# Initialize Agents
# Note: auditor.py must now support .last_metadata for citations
auditor = AuditorAgent()
fetcher = ArchitecturalFetcher()

# Sidebar for Project Info (Judge Visibility)
with st.sidebar:
    st.header("Hackathon Stats")
    st.info("Model: gemini-3-flash-preview")
    st.write("---")
    st.write("### Technical Execution")
    st.write("- **Layer 0**: Current Zoning (NR3 Proof)")
    st.write("- **Layer 2**: Zoned Capacity (Lot Stats)")
    st.write("- **Ledger**: Confluent Kafka Audit")

# Main Input Section
address = st.text_input("Enter Property Address (Seattle area preferred)", "11520 Roosevelt Way NE")

if st.button("🚀 Run Major Audit"):
    with st.spinner("Gemini 3 is researching Zillow, Redfin, and King County..."):
        # Step 1: Research the PIN
        pin = auditor.find_pin(address)
        
        if pin and len(pin) == 10:
            # Step 2: Execute the Traceable Fetch
            res = fetcher.execute_major_pull(pin, address)
            data = res['ingestible_data']
            
            st.success(f"✅ Verified PIN via Research: {pin}")

            # SHOW THE RESEARCH CITATIONS (The "Wow Factor")
            if hasattr(auditor, 'last_metadata') and auditor.last_metadata:
                with st.expander("🌐 View Gemini 3 Research Sources"):
                    st.write("The AI verified this property using the following live sources:")
                    # Iterating through grounding metadata from the new SDK
                    for chunk in auditor.last_metadata.grounding_chunks:
                        if chunk.web:
                            st.markdown(f"* [{chunk.web.title}]({chunk.web.uri})")

            # MAIN METRICS DISPLAY
            st.write("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Zoning Designation", data['zoning_designation'])
                st.caption("Source: City of Seattle Layer 0")
            
            with col2:
                lot_area = data.get('lot_area_sqft')
                if lot_area:
                    st.metric("Lot Area", f"{int(lot_area):,} sqft")
                else:
                    st.metric("Lot Area", "N/A")
                st.caption("Source: City of Seattle Layer 2")
                
            with col3:
                st.metric("MHA Zone", data.get('mha_zone', 'None'))
                st.caption("Mandatory Housing Affordability")

            # AUDIT TRAIL FOR KEVIN
            st.write("---")
            with st.expander("🔍 Immutable Traceability Ledger (Kafka Audit)"):
                st.write("This JSON envelope was published to Confluent with a unique Trace ID.")
                st.json(res)
        else:
            st.error("❌ Research Failed. Gemini 3 could not verify a 10-digit PIN for this address. Please try a specific Seattle address.")

st.write("---")
st.caption("BlackFox Studios | Andrew Powers | 2026 Gemini 3 Hackathon Entry")