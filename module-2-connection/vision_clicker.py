import base64, pyautogui # We import libraries for image encoding and mouse control.
from openai import OpenAI
import json

client = OpenAI(api_key="your_api_key_here")

def get_button_coordinates(image_path: str) -> dict:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="<LATEST_REASONING_MODEL>",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Find the 'Save' button. Return ONLY valid JSON with 'x' and 'y' integer coordinates."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def click_save_button(screenshot_path: str):
    raw_response = get_button_coordinates(screenshot_path)
    coordinates = json.loads(raw_response)

    target_x = coordinates["x"]
    target_y = coordinates["y"]

    pyautogui.moveTo(target_x, target_y, duration=0.5)
    pyautogui.click()
    print("Physical click executed successfully.")
