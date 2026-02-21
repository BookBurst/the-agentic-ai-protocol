import json # We use standard JSON to format the output for our graph database.
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def extract_graph_relationships(raw_text: str):
    # We ask the model to act as a data extractor and find the red strings.
    prompt = """
    Read the text and extract relationships.
    Format exactly like this: {"subject": "X", "relation": "Y", "object": "Z"}
    """
    
    response = client.chat.completions.create(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": raw_text}
        ],
        response_format={"type": "json_object"}
    )
    
    # We parse the text into a clean data dictionary.
    return json.loads(response.choices[0].message.content)

# We feed it a messy sentence to see if it finds the connection.
messy_email = "Just letting you know that David took over the Marketing Department yesterday."
graph_data = extract_graph_relationships(messy_email)

# The output becomes a verified connection in our agent's long-term memory.
print(f"Node 1: {graph_data['subject']}")
print(f"Connection: {graph_data['relation']}")
print(f"Node 2: {graph_data['object']}")
