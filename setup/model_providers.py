# THE OPENAI BASELINE
# The string inside the model parameter expires every few months.
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# THE ANTHROPIC SWAP
# A builder preferring Claude changes exactly two lines of code.
# from langchain_anthropic import ChatAnthropic
# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

# THE GOOGLE SWAP
# A builder heavily invested in the Google Cloud environment uses Gemini.
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
