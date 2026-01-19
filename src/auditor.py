import os
from google import genai
from google.genai import types

class AuditorAgent:
    def __init__(self):
        # The new SDK automatically picks up GEMINI_API_KEY from the env
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_id = 'gemini-3-flash-preview'
        else:
            self.client = None
        self.last_metadata = None

    def find_pin(self, address):
        if not self.client:
            return None
            
        # Agentic Instruction: Force a multi-site search
        prompt = f"""
        Research the property at: {address}. 
        1. Use Google Search to find the 10-digit King County PIN (Parcel Number) on Zillow, Redfin, or the King County Assessor's site.
        2. Verify that the address and PIN match.
        3. Respond with 'FINAL_PIN: [10-digits]' and a brief research summary.
        """
        
        try:
            # Enable Google Search Tool for Grounding
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            
            # Extract PIN and save metadata for the UI to display citations
            if response.text and "FINAL_PIN:" in response.text:
                self.last_metadata = response.candidates[0].grounding_metadata
                pin_part = response.text.split("FINAL_PIN:")[-1].strip()
                # Clean up everything except digits
                verified_pin = "".join(filter(str.isdigit, pin_part))[:10]
                return verified_pin
            return None
        except Exception as e:
            print(f"Gemini 3 Research Error: {e}")
            return None