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
