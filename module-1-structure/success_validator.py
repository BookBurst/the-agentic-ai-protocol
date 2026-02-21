import re

def evaluate_success_criteria(drafted_email: str) -> bool:
    # Rule 1: The email must be short. We count the words.
    if len(drafted_email.split()) > 100:
        print("Failure: Email is too long.")
        return False
        
    # Rule 2: The agent must include the exact booking link.
    if "calendly.com/our-team" not in drafted_email:
        print("Failure: Missing the correct booking link.")
        return False
        
    # Rule 3: The agent must never mention the competitor.
    # We use a quick scan to block the competitor's name.
    if re.search("TechCorp", drafted_email, re.IGNORECASE):
        print("Failure: Mentioned the competitor.")
        return False
        
    # The output meets all criteria.
    print("Success: The draft is approved.")
    return True

# We test the manager with a bad draft from the AI.
bad_draft = "Hello, we are better than TechCorp. Please reply."
is_ready = evaluate_success_criteria(bad_draft)

# The script returns 'False'. The agent must rewrite the email.
