# 🏠 Pre Permit AI (v2.0-Agentic)

**Pre Permit AI** is an autonomous architectural auditing tool that uses **Gemini 3 Flash** to resolve complex property data for ADU/DADU development in Seattle.

---

## 🚀 The Gemini 3 "Agentic" Solution
The project moved from a static database lookup to an **Agentic Search** model to solve the "Killed Parcel" issue (where government records are retired or moved).

### 🧠 System Intelligence
* **Model:** `gemini-3-flash-preview`
* **Feature:** **Google Search Grounding** enabled.
* **Logic:** When an address like `11520 Roosevelt Way NE` is entered, the AI acts as an agent to search Zillow, Redfin, and the King County Assessor to find the 10-digit Parcel ID (PIN) before querying the city dataset.

---

## 🏗️ Technical Architecture

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | User Interface & Real-time Spinner |
| **Agent** | Gemini 3 Flash | Web Search & Thinking Reasoning (Level: High) |
| **API** | Seattle ArcGIS | Zoned Development Capacity Data |
| **Audit Log** | Confluent Kafka | Immutable event recording of every search |

---

## 🛠️ Repository Manifest

* **`src/auditor.py`**: The "Brain." Contains the Gemini 3 logic that harvests PINs from web search results.
* **`src/fetcher.py`**: The "Data Gatherer." Queries the Seattle GIS FeatureServer using the AI-verified PIN.
* **`src/ui.py`**: The "Portal." Branded as **Pre Permit AI** with agentic status indicators.
* **`requirements.txt`**: Locked to `google-genai>=1.2.0` for Gemini 3 support.

---

## 🚦 Deployment Status
- **Terminal Verification:** ✅ Success (PIN 2044500090 resolved via Search).
- **Cloud Run Deployment:** ⚠️ Active (Optimizing for "Thinking" response buffers).
- **Environment:** `us-west1` | Cloud Run | Dockerized Python 3.9-slim.

---

## 📝 Next Steps for Maintenance
1. **Logs Analysis:** Monitor Google Cloud Logging for "Thinking" part extraction.
2. **Timeout Buffering:** Ensure Cloud Run timeout remains at 300s to allow Agentic Search to complete.
3. **Data Refresh:** Update the ArcGIS URL if the Seattle 2016 Snapshot is deprecated.

**Project Lead:** Andrew | **AI Thought Partner:** Gemini
