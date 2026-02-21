import requests
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=2, min=2, max=10), stop=stop_after_attempt(5))
def fetch_client_data():
    print("Attempting to connect to the database...")
    response = requests.get("https://api.example.com/data")
    response.raise_for_status() 
    return response.json()

def make_secure_api_call(access_token: str, refresh_token: str) -> str:
    response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {access_token}"})

    if response.status_code == 401:
        print("Token expired. Getting a new one secretly.")
        new_token_response = requests.post("https://api.example.com/refresh", data={"refresh": refresh_token})
        new_access_token = new_token_response.json()["access_token"]

        retry_response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {new_access_token}"})
        return retry_response.text

    return response.text
