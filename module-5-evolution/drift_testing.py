import json
import pytest
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE TEST ENGINE
# We set the temperature to absolute zero.
# This minimizes random text generation during our testing phase.
test_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.0)

def run_invoice_extraction(raw_text: str) -> str:
    # This function mirrors the exact agent logic running in production.
    messages = [
        SystemMessage(content="Extract the total amount. Return ONLY valid JSON with the key 'total'."),
        HumanMessage(content=raw_text)
    ]
    response = test_llm.invoke(messages)
    return response.content

# 2. THE DETERMINISTIC EVALUATION
# We prefix the function with 'test_' so the testing framework recognizes it.
def test_model_drift_json_format():
    print("Running automated drift evaluation...")
    
    # We define a controlled, unchanging input variable.
    mock_invoice = "Thank you for your business. Total due: $450.00. Please pay by Friday."
    
    # We fire the input at the agent.
    output = run_invoice_extraction(mock_invoice)
    
    # 3. THE GRADING LOGIC
    # We wrap the parsing step in a try-except block to catch formatting drift.
    try:
        parsed_data = json.loads(output)
    except json.JSONDecodeError:
        # If the provider added markdown ticks, the test fails immediately.
        pytest.fail(f"Drift Detected: Output is no longer valid JSON. Raw output: {output}")
    
    # 4. THE MATHEMATICAL CHECK
    # We verify the model still extracts the correct value.
    assert "total" in parsed_data, "Drift Detected: The 'total' key is missing."
    assert parsed_data["total"] == 450.00, "Drift Detected: Mathematical extraction failed."
    
    print("Test passed. Architecture is stable.")
