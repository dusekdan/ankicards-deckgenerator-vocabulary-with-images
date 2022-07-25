import os
import sys
import json
import secrets
import string
import requests

from time import sleep

SCRIPT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
API_TOKEN_FILE = os.path.join(SCRIPT_DIR_PATH, ".pexels_api_token")

API_TOKEN_NOT_FOUND_BLURB = """
API token for Pexels API not found. To fix this:
\t 1. Go to https://www.pexels.com/ and register for a free account
\t 2. Confirm your email address and navigate under Images & Video API from your profile picture menu.
\t 3. Create a project, add a description and click generate API key.
"""

PEXELS_API_SEARCH = "https://api.pexels.com/v1/search?query={prompt}&per_page=1&size=small"
ANKI_MEDIA_DIRECTORY = "C:\\Users\\$USERNAME$\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\"

def main():
    api_key = None

    """If token does not exist, instruct user to provide it."""
    if not os.path.exists(API_TOKEN_FILE):
        while not api_key: 
            print(API_TOKEN_NOT_FOUND_BLURB)
            api_key = input("Paste the API key here: ")

        print("Thank you. If this was not the actual API key, you can always update this in `.pexels_api_token` file, or run this again after deleting it.")
        with open(API_TOKEN_FILE, 'w') as f:
            f.write(f"token={api_key.strip()}")

    if not api_key:
        api_key = retrieve_api_key(API_TOKEN_FILE)

    print(f"Huraaay API key found {api_key}")

    #output_deck_filename = input("Provide name for the import package that will be created: ")
    #output_deck_filename = output_deck_filename.strip()

    """
    And here we can start implementing the logic.
    """
    # 1. Load a list of words to get pics for
    words = load_words()
    generate_deck_import_package(words)#, output_deck_filename)

    print(get_image_for_prompt("ladder", api_key))

def generate_deck_import_package(words, import_package_file_name="import-me.txt"):
    with open(os.path.join(SCRIPT_DIR_PATH, import_package_file_name), 'w', encoding="utf-8") as f:
        for original, translated in words.items():
            f.write(generate_card(original, translated, "paste-8c3e288676cb808211bf6420c0161e92401f3a85.jpg"))

def get_image_for_prompt(prompt, api_key):
    prompt_search_url = PEXELS_API_SEARCH.replace("{prompt}", prompt)
    r = requests.get(prompt_search_url, headers={"Authorization": api_key})

    print(r.status_code)
    print(r.text)

    if r.status_code != 200:
        print(f"Non-200 response received for URL: {prompt_search_url}")
        print("This image will possibly not be downloaded properly.")

    data = json.loads(r.text)
    small_image_url = data["photos"][0]["src"]["tiny"]

    # Download image and place into anki directory
    image_filename = f"prompt-{random_string()}.jpg"
    blob = requests.get(small_image_url).content
    with open(os.path.join(ANKI_MEDIA_DIRECTORY, f"{image_filename}"), 'wb') as img_file:
        img_file.write(blob)

def generate_card(front, back, image_path):
    return f'"{front}"\t"{back}<img src=""{image_path}"">"\n'

def load_words(wordlist_file="wordlist.csv"):
    with open(wordlist_file, 'r', encoding='utf-8') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    
    words = {}
    for line in lines:
        parts = line.split(";")
        words[parts[0]] = parts[1]
    
    return words

def retrieve_api_key(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        contents = f.read()
    
    parts = contents.split("token=")
    
    if len(parts) != 2:
        print("API Token provided in `.pexels_api_token` does not seem to be correct. Delete the token file and run the script again.")
        sys.exit(1)
    
    return parts[1]

def random_string(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


if __name__ == '__main__':
    main()