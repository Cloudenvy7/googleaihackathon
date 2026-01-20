## Hackathon Submission Snapshot and Development Notice

This repository’s main branch is intentionally maintained as a frozen snapshot of the project submitted to the **AI Partner Catalyst Hackathon (Google Cloud Partnerships)** prior to the December 31, 2025 submission deadline.

All functionality, architecture, and documentation on the main branch correspond to that submission and are preserved for judging and review purposes.

Subsequent exploratory and forward-looking development related to the **Gemini 3 API Hackathon** began only after the official start of that hackathon and is isolated to a separate branch. That work is not part of the AI Partner Catalyst Hackathon submission and does not modify this snapshot.

This structure ensures that the project remains eligible for both hackathons, with each submission evaluated strictly against its respective rules, timelines, and requirements.

**References to Gemini 3 in this README reflect the original architecture and submission scope of the AI Partner Catalyst Hackathon.**



## Links
Hosted app: [https://dadu-analyzer-app-617957523681.us-west1.run.app](https://dadu-analyzer-app-617957523681.us-west1.run.app)
Demo video: [https://www.loom.com/share/9efde995968d49838c600161d87286bd](https://www.loom.com/share/9efde995968d49838c600161d87286bd)
Code repo: https://github.com/Cloudenvy7/googleaihackathon

## One sentence summary
Pre Permit AI is a real time pre submission auditing system for Seattle DADU permits that uses Google Cloud Gemini for reasoning and Confluent Cloud for a verifiable audit ledger.

## Confluent Challenge Alignment
This project streams every data pull and AI audit event into Confluent Cloud as data in motion, enabling replay, governance, and traceability for high stakes permitting decisions.


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

## Data flow

User enters an address in Streamlit. Gemini 3 Flash runs agentic search to recover the parcel id when needed. The system queries Seattle ArcGIS datasets using the verified parcel id. Every raw response and audit result is published to Confluent Cloud as an immutable event stream so results can be replayed, verified, and traced back to original sources.

## Quickstart

1 Clone the repository

```bash
git clone https://github.com/Cloudenvy7/googleaihackathon.git
cd googleaihackathon

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3 Configure environment variables

Set environment variables for Google and Confluent access.

Required variables
GOOGLE api key or application default credentials
CONFLUENT bootstrap server
CONFLUENT api key
CONFLUENT api secret
CONFLUENT topic name

4 Run locally
streamlit run src/ui.py

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




