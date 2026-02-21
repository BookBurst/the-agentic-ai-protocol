import base64, pyautogui # We import libraries for image encoding and mouse control.
from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

def get_button_coordinates(image_path: str) -> dict:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # We ask the vision model to find the Save button and return math coordinates.
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
        response_format={"type": "json_object"} # We force a strict JSON return.
    )
    return response.choices[0].message.content
import json # We import json to parse the model's coordinate reply.

def click_save_button(screenshot_path: str):
    raw_response = get_button_coordinates(screenshot_path)
    coordinates = json.loads(raw_response) # We convert the text into a data dictionary.

    target_x = coordinates["x"] # We extract the specific X position.
    target_y = coordinates["y"] # We extract the specific Y position.

    # We command the local machine to physically move the mouse and click.
    pyautogui.moveTo(target_x, target_y, duration=0.5)
    pyautogui.click()
    print("Physical click executed successfully.")

# We take a picture of the screen and run the sequence.
pyautogui.screenshot("current_screen.jpg")
click_save_button("current_screen.jpg")
