import streamlit as st
import re
from fetcher import ArchitecturalFetcher
from auditor import confirm_parcel_id_stream, analyze_parcel

st.set_page_config(page_title="Pre Permit AI", page_icon="🏠")
st.title("🏠 Pre Permit AI")
addr = st.text_input("Property Address", value="11520 Roosevelt Way NE")

if st.button("Run Analysis"):
    full_response = ""
    pin = None
    
    with st.status("🤖 Gemini 3 Agent is reasoning...", expanded=True) as status:
        thought_placeholder = st.empty()
        try:
            stream = confirm_parcel_id_stream(addr)
            if stream:
                for chunk in stream:
                    if chunk.candidates:
                        for part in chunk.candidates[0].content.parts:
                            if part.text:
                                full_response += part.text
                            elif hasattr(part, 'thought'):
                                full_response += f"\n(Thinking: {part.thought})\n"
                            thought_placeholder.markdown(full_response)
                
                match = re.search(r'\b\d{10}\b', full_response)
                if match:
                    pin = match.group(0)
                    status.update(label=f"✅ Found PIN: {pin}", state="complete")
                else:
                    status.update(label="❌ PIN Not Found", state="error")
            else:
                st.error("Failed to initialize stream. Verify API Key.")
        except Exception as e:
            st.error(f"Stream Error: {str(e)}")

    if pin:
        fetcher = ArchitecturalFetcher()
        with st.spinner("📊 Pulling City Records..."):
            data = fetcher.fetch_architectural_data(pin)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("City Data")
            st.json(data)
        with col2:
            st.subheader("Gemini 3 Audit")
            st.write(analyze_parcel(data))

st.divider()
st.caption("🚀 Version: Pre Permit AI v2.2 (Agentic) | SDK: 1.47.0 | Model: Gemini 3 Flash")
