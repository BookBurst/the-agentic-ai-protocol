from celery import Celery
import time

# We connect Celery to our Redis ticket rail running on the local server.
# The URL tells the background worker exactly where to look for new jobs.
app = Celery('agent_tasks', broker='redis://localhost:6379/0')

# We use this decorator to tell Celery this function belongs in the background.
@app.task
def run_deep_research(company_name: str):
    # We simulate a heavy AI reasoning process that takes twenty minutes.
    print(f"Starting deep research on {company_name}...")
    
    # The agent scrapes web pages, reads PDFs, and calls the language model.
    time.sleep(1200) 
    
    # The worker finishes the job and saves the file quietly to the hard drive.
    print(f"Finished. Saved {company_name}_report.pdf to the server.")
    return True

# ==========================================
# IN A DIFFERENT FILE (THE API FRONT DOOR)
# ==========================================

# When the Telegram command arrives, the API runs this single line.
# The ".delay()" command means: "Put the ticket on the rail and hang up the phone."
# run_deep_research.delay("TechCorp Inc.")
