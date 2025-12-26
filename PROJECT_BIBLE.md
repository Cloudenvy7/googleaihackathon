# 📖 The Project Bible: Seattle AI Pre-Permit Analyzer
**Repo:** https://github.com/Cloudenvy7/googleaihackathon
**Status:** Active Build
**Maintainer:** Cloudenvy7

## 🏛️ Section 1: The Project Charter
**Mission:** Reduce Seattle’s $367M permit backlog by validating architectural plans against *Live* Municipal Code.
**Strategy:** "Double Dip" - Use Confluent (Dec 31) for the data pipeline and Gemini 3 (Feb 9) for the reasoning engine.

## 📝 Change Log
* **[2025-12-25] Genesis:** Project initialized in Google Cloud Shell. Repo linked
* **[2025-12-26] Update:** Implemented 'Nervous System' (src/fetcher.py). Successfully connected Python to Confluent Cloud.

## 🕰️ chronological Session Log: Phase 1 (The Nervous System)
**Date:** 2025-12-26

**1. Infrastructure & Identity Crisis**
* **Action:** Initialized Google Cloud Shell and attempted to clone the repository.
* **Friction:** Attempted `git push` using standard password authentication. Failed due to GitHub's 2021 security depreciation of passwords.
* **Resolution:** Pivoted to `gh auth login` (GitHub CLI), utilizing browser-based OAuth to establish a secure, password-less link between Google Cloud and GitHub.

**2. The "Nervous System" Construction**
* **Action:** Drafted `src/fetcher.py` to act as the bridge between Seattle GIS (Source) and Confluent Cloud (Sink).
* **Action:** Generated Confluent Cloud API Keys under the identifier "Google AI Partner Hackathon".
* **Friction:** Cloud Shell session timed out/disconnected. Upon reconnection, environment variables (API Secrets) were purged from RAM, causing the Python script to crash with "Auth Failed" and "File Not Found" errors.
* **Resolution:** Established a strict "Atomic Execution" protocol—exporting keys and running the script in a single command block to prevent memory loss.

**3. The Data Validity Test (The "Empty Pipe")**
* **Action:** Executed the first live fire test against Parcel PIN `1975700575`.
* **Observation:** The pipeline connected successfully (HTTP 200), and Confluent auth passed, BUT the Seattle GIS returned zero records. The pipe was working, but the water was dry.
* **Correction:** We did not change the code logic; we changed the target. Pivoted to PIN `8804900985` (Capitol Hill/Derby Apt area) to force a positive data collision.

**4. Current Status**
* **State:** Ready for final validation of the Capitol Hill PIN.
* **[2025-12-26] Strategy Alignment:** Selected Target Property **3304 7th Avenue W** (PIN 3613600165).
    * **Reasoning:** Maintains consistency with prior "Architect" persona and ChatGPT POC.
    * **Objective:** Validate pipeline against **Residential Zoning** rules (e.g., NR1/NR3) rather than Commercial, to match the homebuilder/renovation use case.
* **[2025-12-26] SESSION END:** Code updated to 'ArchitecturalFetcher' (PRD Aligned).
* **[2025-12-26] State:** Repo synced. Ready to integrate Gemini 3 API on next login.

### **[2025-12-26 05:39] ⚠️ Engineering Pivot: The "Robust Pipeline" Logic**
* **The Failure (The "Snob" Bug):**
    * *Issue 1 (The Typos):* We assumed strict address matching would work. It failed because King County is pedantic ("Ave" vs "Avenue").
    * *Issue 2 (The Data Gap):* The code logic was: *"If Seattle Capacity Database returns NULL, stop."* This was a **Critical Logical Error**.
    * *Reality:* Many valid houses (like 3304 7th Ave W) exist physically but are not flagged as "Redevelopment Sites" by the City. The code was falsely claiming they didn't exist.
* **The Fix (Robust Fallback Strategy):**
    * **Logic Change:** "Rich Data if possible, Basic Data if necessary."
    * **Implementation:** The Fetcher now attempts to get the 'Gold' (65 Attributes). If it fails, it **does not stop**. It tags the data as `KING_COUNTY_BASIC` and forces it through to the Auditor.
    * **Gemini's Role:** Gemini 3 is now responsible for handling the ambiguity ("I see the house, but I lack zoning metrics") rather than the Fetcher killing the process.

### **[2025-12-26 05:39] Compliance Check: Gemini 3**
* **Verification:** Confirmed `src/auditor.py` is using `MODEL_ID = "gemini-3-pro"` and the new `google-genai` SDK.
* **Status:** Compliant with Hackathon "Action Era" rules.

### **[2025-12-26] Ancestral Knowledge: The ChatGPT POC (Oct 2025)**
* **Source Material:** "Chatgpt Model Seattle Parcel Extractions Agent - Development Logs.pdf"
* **The "Zillow Paradox":**
    * *Theory:* The strict rules said "Denylist Zillow/Redfin" to avoid bad data.
    * *Practice:* The logs reveal the system *did* use Redfin/Compass as a **"Desperation Fallback"** when the official City GIS failed to return attributes.
    * *Lesson:* The system MUST have a fallback layer. "No Data" is an unacceptable state for a user standing in front of a house.
* **The "FeatureServer/0" Trap:**
    * The logs confirm we moved away from FeatureServer/0 (Address Only) to FeatureServer/2 (Rich Data) because FS/0 lacked critical metrics (FAR, Lot Coverage).
    * *Current Architecture:* We respect this decision but use FS/0 (via King County) as the **Bridge**, not the **Source**.

### **[2025-12-26] Architecture Verification: The "Hybrid" Stack**
* **The New Pipeline (Dec 2025):**
    * **Layer 1 (The Bridge):** King County GIS acts as the "Phonebook." It resolves *any* fuzzy address (e.g., "3304 7th") to a PIN.
    * **Layer 2 (The Gold Mine):** We query Seattle FeatureServer/2 for the 65 Attributes.
    * **Layer 3 (The Safety Net):** If Layer 2 fails (house exists but no capacity data), we **FALLBACK** to Layer 1 data and pass it to Gemini.
    * *Status:* This mirrors the *intent* of the POC's Zillow fallback but keeps data authoritative (County vs Commercial).
