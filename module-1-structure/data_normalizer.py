from pydantic import BaseModel, Field
from datetime import date
import json
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

# We build a rigid container for the data. 
# The agent absolutely must fit its findings into these exact slots.
class StandardHandoff(BaseModel):
    company_name: str
    revenue_usd: float = Field(description="Strictly converted to US Dollars")
    report_date: date = Field(description="Strictly ISO 8601 format YYYY-MM-DD")

def normalize_research_data(raw_text: str):
    # We instruct the model to act as a data translator.
    prompt = "Extract the financial data and format it exactly to the required schema."
    
    response = client.chat.completions.create(
        model="<LATEST_FAST_MODEL>",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": raw_text}
        ],
        # We force the model to respect our strict Pydantic contract.
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "financial_handoff",
                "schema": StandardHandoff.model_json_schema()
            }
        }
    )
    
    # We return a perfectly clean JSON object ready for the Analyst agent.
    return json.loads(response.choices[0].message.content)
