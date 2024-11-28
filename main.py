import pyautogui
import time
import requests
import pyperclip
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
AI_URL = "REPLACE-WITH-YOUR-OPENAI-URL" # I only tested on LM Studio so no key required
# KEY = ""
WHITE_RGB = (255, 255, 255)  # RGB for message indicator (white)
GRAY_RGB = (200, 200, 200)   # RGB for empty state (gray)
CHECK_INTERVAL = 1  # Interval to check for new messages
BOT_PROMPT = "你是一名风趣幽默的私人助理，总能以意想不到地方式回答我的问题，并提出独具创意的想法。所有的回答都非常诚实，能够保证回复内容的准确性。"
START_WITH = "@robot" #Change it to your robot WeChat nickname 

# Function Definitions
def select_location():
    """
    Allows the user to click on the screen to select a location.
    Returns the (x, y) coordinates of the clicked point.
    """
    try:
        logging.info("Starting location selection")
        print("Move your mouse to the desired location and press Enter.")
        input("Press Enter to confirm location...")
        location = pyautogui.position()
        logging.info(f"Location selected: {location}")
        return location
    except ImportError as e:
        logging.error(f"Module import error: {e}")
        raise RuntimeError("PyAutoGUI dependencies are not properly installed. Please check your setup.")
    except Exception as e:
        logging.error(f"Unexpected error during location selection: {e}")
        raise

def detect_color(location):
    """
    Detects the color of the pixel at the given screen location.
    Args:
        location (tuple): (x, y) coordinates of the pixel to check.
    Returns:
        tuple: RGB color of the pixel.
    """
    logging.info(f"Detecting color at location: {location}")
    screenshot = pyautogui.screenshot()
    color = screenshot.getpixel(location)
    logging.info(f"Detected color: {color}")
    return color

def call_ai(url, question):
    """
    Sends a question to the AI chatbot via URL and retrieves the response.
    Args:
        url (str): The URL of the chatbot API.
        question (str): The question to send.
    Returns:
        str: The response text from the chatbot.
    """
    logging.info(f"Calling AI with question: {question}")
    try:
        payload = {
            "model": "lm-models/qwen-1.5-gguf",
            "messages": [
                {"role": "system", "content": BOT_PROMPT}, # Replace with your own prompt
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response provided.")
        logging.info(f"Received AI response: {answer}")
        return answer
    except Exception as e:
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return error_message

def copy_question(location):
    """
    Copies text from the chat message at the given location.
    Args:
        location (tuple): (x, y) coordinates of the chat message.
    Returns:
        None
    """
    logging.info(f"Copying question from location: {location}")
    pyautogui.moveTo(location)
    pyautogui.rightClick()
    time.sleep(1) # Slow down, slow down
    pyautogui.moveRel(10, 10)
    time.sleep(1)
    pyautogui.click()
    logging.info("Question copied to clipboard")

def paste_answer(answer, input_box_location):
    """
    Pastes the AI response into the chat input box and sends it.
    Args:
        answer (str): The response text to paste.
        input_box_location (tuple): Coordinates of the chat input box.
    Returns:
        None
    """
    logging.info(f"Pasting answer: {answer}")
    pyperclip.copy(answer)
    pyautogui.click(input_box_location)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(1)
    logging.info("Answer pasted and sent")

# Main Function
def main():
    logging.info("=== Chatbot Automation Configuration ===")
    print("Select the chat message location:")
    chat_location = select_location()
    print("Select the chat input box location:")
    input_box_location = select_location()
    last_message = ""
    logging.info("Starting monitoring...")
    while True:
        try:
            # Detect color at the chat message location
            current_color = detect_color(chat_location)
            if current_color == WHITE_RGB:
                logging.info("New message detected")

                # Copy new message
                copy_question(chat_location)
                time.sleep(0.5)  # Allow clipboard to update

                # Get copied message
                question = pyperclip.paste().strip()
                logging.info(f"Copied question: {question}")

                # Check for new content and @Libot prefix
                if question != last_message and question.startswith(START_WITH):
                    logging.info(f"Processing new question: {question}")
                    last_message = question

                    # Send to AI and get response
                    answer = call_ai(AI_URL, question)

                    # Paste and send response
                    paste_answer(answer, input_box_location)

            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error during monitoring: {e}")

if __name__ == "__main__":
    main()
