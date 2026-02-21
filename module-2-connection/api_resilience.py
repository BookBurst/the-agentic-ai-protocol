import requests # We use this to make web calls.
from tenacity import retry, wait_exponential, stop_after_attempt # We bring in the retry tools.

# We tell the script to retry automatically if it fails.
# It waits 2 seconds, then doubles the wait time, up to a maximum of 5 tries.
@retry(wait=wait_exponential(multiplier=2, min=2, max=10), stop=stop_after_attempt(5))
def fetch_client_data():
    print("Attempting to connect to the database...")
    response = requests.get("https://api.example.com/data")
    
    # We force the code to raise an error if the server returns a bad status.
    # This error triggers the tenacity retry loop automatically.
    response.raise_for_status() 
    
    return response.json()

# When we call this, it will automatically pace itself if the server is down.
# data = fetch_client_data()


def make_secure_api_call(access_token: str, refresh_token: str) -> str:
    # We try to get the data using our current wristband.
    response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {access_token}"})

    # We check if the server rejected our expired token.
    if response.status_code == 401:
        print("Token expired. Getting a new one secretly.")
        
        # We show our ID to the bouncer to get a new wristband.
        new_token_response = requests.post("https://api.example.com/refresh", data={"refresh": refresh_token})
        new_access_token = new_token_response.json()["access_token"]

        # We try the original request again with the new wristband.
        retry_response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {new_access_token}"})
        return retry_response.text

    # If the first try worked, we just return the data.
    return response.text
