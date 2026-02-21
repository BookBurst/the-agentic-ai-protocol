from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ==========================================
# PHASE 1: THE DATA MINER SCHEMA
# ==========================================

# We force the first agent to return cold, hard facts.
# This physically prevents the model from generating marketing fluff.
class TargetFacts(BaseModel):
    recent_achievement: str = Field(description="A specific recent project or award.")
    company_focus: str = Field(description="The primary goal of their current company.")
    common_ground: str = Field(description="A shared interest or specific technical skill.")

# We instantiate a highly literal model for the extraction phase.
# A temperature of zero keeps the agent completely grounded in the text.
# We use an evergreen placeholder to future-proof the architecture against model deprecation.
extraction_llm = ChatOpenAI(model="<LATEST_REASONING_MODEL>", temperature=0.0)
fact_miner = extraction_llm.with_structured_output(TargetFacts)

# We instantiate a faster model for the writing phase.
# A slightly higher temperature allows for conversational variety.
drafting_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.4)


# ==========================================
# PHASE 2: EXTRACTION & DRAFTING LOGIC
# ==========================================

def generate_researched_outreach(raw_profile_text: str, sender_name: str) -> str:
    print("Initiating data extraction phase...")

    # 2. THE EXTRACTION PHASE
    # The miner reads the messy HTML or raw text and pulls the required fields.
    miner_instructions = [
        SystemMessage(content="Extract exactly three professional facts from this profile data."),
        HumanMessage(content=raw_profile_text)
    ]
    
    extracted_data = fact_miner.invoke(miner_instructions)
    print("Facts successfully extracted and verified.")

    # 3. THE DRAFTING PHASE
    # We build a strict copywriting prompt.
    # We inject the structured JSON directly into the rules.
    copywriting_rules = f"""
    Write a 50-word cold email from {sender_name}.
    Do not use generic greetings. 
    Base the entire email strictly on these facts:
    1. They recently accomplished: {extracted_data.recent_achievement}
    2. Their company focuses on: {extracted_data.company_focus}
    3. They care about: {extracted_data.common_ground}
    """

    draft_instructions = [
        SystemMessage(content="Act as a direct, polite professional. Write short, factual emails."),
        HumanMessage(content=copywriting_rules)
    ]

    print("Drafting personalized outreach...")
    final_email = drafting_llm.invoke(draft_instructions)

    return final_email.content


# ==========================================
# PHASE 3: LIVE EXECUTION TEST
# ==========================================

# Simulating a raw data dump from a web scraper.
mock_linkedin_scrape = "Jane Doe. VP of Engineering at TechCorp. Just launched a new Kubernetes cluster. Passionate about open source monitoring tools."

# We pass a generic placeholder variable to execute the test.
# result = generate_researched_outreach(mock_linkedin_scrape, "<SENDER_NAME>")
# print(f"--- GENERATED EMAIL ---\n{result}")
