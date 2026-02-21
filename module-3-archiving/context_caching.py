import datetime # We use this to set a time limit for the memory.
import google.generativeai as genai
from google.generativeai import caching # We bring in the specific caching tools.

# We upload the heavy technical manual to the server exactly once.
document_file = genai.upload_file("massive_technical_manual.pdf")

# We create a temporary storage zone in the server's RAM.
# We tell the system to hold this exact document ready for the next 60 minutes.
document_cache = caching.CachedContent.create(
    model='<LATEST_REASONING_MODEL>',
    system_instruction="Base all your answers entirely on this manual.",
    contents=[document_file],
    ttl=datetime.timedelta(minutes=60)
)

# We connect our agent directly to the active cache, completely skipping the upload phase.
support_agent = genai.GenerativeModel.from_cached_content(cached_content=document_cache)

# We ask a question. The agent answers instantly because the manual is already in its head.
user_question = "How do I reset the main router?"
response = support_agent.generate_content(user_question)

print(response.text)
