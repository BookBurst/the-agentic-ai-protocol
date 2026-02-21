# We import BaseModel from pydantic to define our strict data structure rules.
from pydantic import BaseModel
# We import the OpenAI client to communicate with the language model.
from openai import OpenAI

# We initialize the client using our secret API key.
client = OpenAI(api_key="your_api_key_here")

# We define a strict schema that the AI must follow exactly.
class RouteDecision(BaseModel):
    # We force the AI to pick one of these assigned strings for the category.
    category: str 
    # We ask the AI to rate its confidence from 1 to 10 for safety checks.
    confidence_score: int
    # We ask the AI to briefly explain its choice for our debugging logs.
    reasoning: str

def classify_user_intent(user_text: str) -> RouteDecision:
    # We use a fast and inexpensive model to save money on simple classification tasks.
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            # We provide the strict system instructions and the critical fallback option.
            {"role": "system", "content": "You are a routing switchboard. Classify the user intent into exactly one of these categories: TECHNICAL_SUPPORT, REFUND_REQUEST, SALES_INQUIRY. If the request does not fit these categories, you must output UNKNOWN."},
            # We insert the raw message from the user.
            {"role": "user", "content": user_text}
        ],
        # We enforce the rigid output format using our Pydantic class to block conversational text.
        response_format=RouteDecision,
    )
    
    # We extract and return the parsed, validated object.
    return response.choices[0].message.parsed

def execute_routing(user_text: str):
    # We run the classification function and store the result.
    decision = classify_user_intent(user_text)
    
    # We print the reasoning for our own monitoring purposes to see how the AI thinks.
    print(f"Log Reasoning: {decision.reasoning}")
    
    # We build a safety net to catch low-confidence guesses.
    if decision.confidence_score < 7:
        print("Confidence too low. Escalating to human manager.")
        # We stop the function early to prevent the AI from making a blind guess.
        return
        
    # We use classic Python logic to activate the correct worker agent.
    if decision.category == "TECHNICAL_SUPPORT":
        print("Activating Tech Support Worker...")
        # tech_worker.run(user_text)
    elif decision.category == "REFUND_REQUEST":
        print("Activating Billing Worker...")
        # billing_worker.run(user_text)
    elif decision.category == "SALES_INQUIRY":
        print("Activating Sales Worker...")
        # sales_worker.run(user_text)
    else:
        # We catch any weird requests and stop the process safely.
        print("Request Unknown. Sending polite fallback message.")

# We test the system with a tricky prompt.
execute_routing("My app keeps crashing on the login screen, please help!")
