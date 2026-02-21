import json
from typing import Protocol
# We isolate the provider imports inside their respective adapter classes.
# The main agent script will never see these libraries directly.
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

# 1. THE UNIVERSAL INTERFACE
# This Protocol dictates exactly how any future model must behave.
# Every adapter must accept a prompt and return a string.
class LanguageModelAdapter(Protocol):
    def generate_text(self, system_rules: str, user_input: str) -> str:
        pass

# 2. THE FIRST ADAPTER
# We wrap the first commercial provider in our standardized rules.
class OpenAIAdapter:
    def __init__(self, model_name: str):
        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def generate_text(self, system_rules: str, user_input: str) -> str:
        messages = [
            SystemMessage(content=system_rules),
            HumanMessage(content=user_input)
        ]
        return self.llm.invoke(messages).content

# 3. THE SECOND ADAPTER
# We wrap a completely different provider using the exact same required structure.
class AnthropicAdapter:
    def __init__(self, model_name: str):
        self.llm = ChatAnthropic(model=model_name, temperature=0.0)

    def generate_text(self, system_rules: str, user_input: str) -> str:
        messages = [
            SystemMessage(content=system_rules),
            HumanMessage(content=user_input)
        ]
        return self.llm.invoke(messages).content

# 4. THE PROTECTED LOGIC
# The agent logic only accepts objects that match our universal interface.
# It genuinely does not know or care which company is providing the intelligence.
def execute_business_logic(ai_engine: LanguageModelAdapter, task: str) -> str:
    print("Initiating abstract logic sequence...")
    rules = "Act as a financial analyst. Keep answers under ten words."
    
    # The logic leans on the standard method we defined, totally ignoring the external tools.
    decision = ai_engine.generate_text(rules, task)
    return decision

# 5. THE HOT SWAP
# We can switch the entire intelligence engine by changing one line of configuration.
# The business logic executes perfectly regardless of the underlying machine.
primary_engine = OpenAIAdapter("<LATEST_REASONING_MODEL>")
backup_engine = AnthropicAdapter("<LATEST_FAST_MODEL>")

print("Testing primary engine execution:")
print(execute_business_logic(primary_engine, "Should we buy tech stocks?"))

print("\nTesting backup engine execution:")
print(execute_business_logic(backup_engine, "Should we buy tech stocks?"))
