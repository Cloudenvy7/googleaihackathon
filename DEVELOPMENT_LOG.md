# 📘 Development Log: Pre-Permit AI v3.0 (Master Audit)
**Project:** Pre-Permit AI | **Lead Engineer:** Andrew Powers (BlackFox Studios)
**Date:** January 19, 2026 | **Session Duration:** ~140 Minutes
**Status:** Architecture Locked (Final Deployment)

---

## 🚀 Executive Summary
This session focused on resolving the "NR3" data integrity issue identified by stakeholders (Kevin). We successfully transitioned from a legacy, hallucination-prone architecture to a **Gemini 3 Grounded Reasoning Agent**. 

## 🏗️ Major Architecture Shifts
| Component | Legacy (V2) | Hackathon (V3) |
| :--- | :--- | :--- |
| **Model** | gemini-1.5-flash | **gemini-3-flash-preview** |
| **SDK** | google-generativeai | **google-genai** (Unified Modern Client) |
| **Knowledge** | Static / Training Data | **Grounded Search** (Live Web Verification) |
| **Security** | Env Variables | **Google Secret Manager** |

---

## 🚧 Verbose Problem & Resolution Log (The "Build-in-Public" Journey)

### **Phase 1: The Data Integrity Gap (The "SF5000" Discrepancy)**
- **The Hurdle:** Stakeholders flagged that the system returned 'SF5000' (outdated) instead of 'NR3' (current zoning).
- **Resolution:** Implemented a **Multi-Layer Merge**. We now pull the definitive zoning label from **Layer 0** (Zoning Detail) and cross-reference physical parcel stats from **Layer 2** (Zoned Capacity).

### **Phase 2: DevOps Hardening & Secret Access**
- **The Hurdle:** Transitioning API keys to Google Secret Manager.
- **Fail 1:** Service Account permissions. The Cloud Run compute service could not read the secrets.
- **Pivot:** Manually executed IAM bindings via gcloud to grant `roles/secretmanager.secretAccessor` to the service account. Verified the secret payload size (39 bytes) to ensure data integrity.

### **Phase 3: The "Sub-Second" Crash (The Silent Killer)**
- **The Hurdle:** The app crashed instantly upon clicking "Run Audit."
- **Debug Path:** Used `gcloud logging read` to bypass `tail` restrictions in Cloud Shell.
- **Discovery:** Found a deprecation loop. The environment was rejecting the legacy `google-generativeai` package. 
- **Resolution:** Performed a full SDK migration to the unified `google-genai` library. This required a ground-up rewrite of the `AuditorAgent` to utilize the 2026 `Client` structure.

### **Phase 4: Hallucinations vs. Agentic Grounding**
- **The Hurdle:** The model was "hallucinating" PIN formats in milliseconds to avoid latency.
- **Fail 3:** `TypeError: unsupported format string passed to NoneType.__format__`.
- **Root Cause:** Fake PINs yielded empty ArcGIS results, causing UI formatting crashes.
- **The "Gemini 3" Pivot:** Enabled **Google Search Grounding**. The agent now visits Zillow, Redfin, and the King County Assessor's site to verify property data *before* fetching permit records.

---

## 🛠️ Technical Execution Details
- **Grounding Tool:** Integrated `Google Search` tool within the Gemini 3 Flash Preview config.
- **Infrastructure:** Google Cloud Run (US-Central1), Secret Manager, Confluent Kafka.
- **Audit Integrity:** Every search generates a unique `trace_id` and a full provenance ledger of sources.

---
*BlackFox Studios | Andrew Powers | 2026 Gemini 3 Hackathon*
