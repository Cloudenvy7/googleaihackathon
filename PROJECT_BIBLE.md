# 📖 The Project Bible: Pre Permit AI (v2.0-Agentic)

**Repo:** https://github.com/Cloudenvy7/googleaihackathon  
**Status:** Active Build (Agentic Search Phase)  
**Maintainer:** Cloudenvy7

---

## 🏛️ Section 1: The Project Charter

**Mission:** Reduce Seattle’s $367M permit backlog by validating architectural plans against Live Municipal Code.  
**Strategy:** "Double Dip" - Use **Confluent Cloud** (Dec 31) for the immutable data pipeline and **Gemini 3 Flash** (Dec 17) as the autonomous reasoning agent.

---

## 📝 Change Log

* **[2025-12-25] Genesis:** Project initialized in Google Cloud Shell. Repo linked.
* **[2025-12-26] Nervous System:** Implemented `src/fetcher.py`. Connected Python to Confluent Cloud.
* **[2025-12-26] The Ghost Data Fix:** Forensic pivot to Seattle FeatureServer/2 (2016 Master Record).
* **[2025-12-26] Gemini 3 Integration:** Migration to `gemini-3-flash-preview` and agentic search logic.

---

## 🕰️ Chronological Session Log: Phase 2 (The Agentic Brain)

### 1. The "Ghost Data" Paradox & Forensic Reconstruction
* **Incident:** Valid properties (3304 7th Ave W, 11520 Roosevelt Way NE) were returning "No Data" or "Killed Parcel" errors.
* **Discovery:** A forensic comparison with the Oct 2025 ChatGPT POC logs revealed a targeting error. We were querying a "Redevelopment Site" layer instead of the **Master Tax Roll (FeatureServer/2)**.
* **Resolution:** Hardcoded the Fetcher to the **2016 Master Layer**. Implemented case-insensitive parsing to handle the lowercase JSON keys returned by this older API (e.g., `zoning` vs `Zoning`).

### 2. Gemini 3 Flash Integration (The "Action Era")
* **Model Pivot:** Transitioned from Pro to `gemini-3-flash-preview` to leverage its superior coding performance (78% on SWE-bench) and low latency.
* **Configuration:** * **SDK:** `google-genai` v1.47.0+.
    * **Thinking Level:** Set to `HIGH` to ensure deep reasoning on Major Institution Overlays (MIO).
    * **Grounding:** Enabled `Google Search` tool to solve the "Zillow Paradox."

### 3. The "Zillow Paradox" & Agentic Search
* **The Problem:** Government APIs frequently "kill" records during lot adjustments, leaving the app blind.
* **The Strategy:** "Search First, Query Second." 
* **Implementation:** Gemini 3 now acts as an agent. It searches Zillow/Redfin to verify the 10-digit PIN before the app ever touches a government database.
* **Success:** PIN `2044500090` (Roosevelt) successfully resolved via web-grounding after official API failures.

### 4. Technical Incident: The "Thinking" Buffer
* **Issue:** Cloud Run deployments initially failed to resolve PINs that worked in the terminal.
* **Root Cause:** Gemini 3's "Thinking" monologue was being read by the UI as the final answer.
* **Fix:** Implemented "Response Harvesting" in `src/auditor.py` to iterate through all response parts and extract the PIN using RegEx.

---

## 🏗️ Architecture Verification: The "Hybrid" Stack

| Layer | Component | Source of Truth |
| :--- | :--- | :--- |
| **Layer 1 (Identity)** | Gemini 3 Agent | Web Search (Zillow/Redfin) for PIN Discovery. |
| **Layer 2 (Attributes)** | Seattle GIS FS/2 | The 2016 Master Record for Zoning/FAR metrics. |
| **Layer 3 (Pipeline)** | Confluent Cloud | Kafka topic `site.fetch.completed` for auditing. |
| **Layer 4 (Verdict)** | Gemini 3 Flash | Reasoning Engine (High Thinking Level). |

---

## 🏁 Final System Validation
* **Test Case:** 11520 Roosevelt Way NE (A "Killed" Parcel).
* **Result:** **PASS**.
* **Execution:** Agent searched web -> Found PIN 2044500090 -> Fetched "SF 7200" zoning -> Gemini 3 performed DADU audit.
* **State:** **PRODUCTION READY.**

---
**Build Maintainer:** Cloudenvy7 | **AI Thought Partner:** Gemini
