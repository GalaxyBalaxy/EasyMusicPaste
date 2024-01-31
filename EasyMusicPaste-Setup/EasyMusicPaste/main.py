import re
import requests
import pyperclip
import logging
from requests.exceptions import RequestException
from easy_music_pastebin.config import (
    PASTEBIN_API_KEY,
    PASTEBIN_USER_KEY,
    GITHUB_TOKEN,
    LOG_FILENAME,
    PASTEBIN_API_URL as PASTEBIN_API_URL_CONFIG,
    GITHUB_GISTS_API_URL as GITHUB_GISTS_API_URL_CONFIG,
    ARTIST_TRACK_PATTERN as ARTIST_TRACK_PATTERN_CONFIG,
)

# Constants and Configuration
PASTEBIN_API_URL = 'https://pastebin.com/api/api_post.php'
GITHUB_GISTS_API_URL = 'https://api.github.com/gists'
ARTIST_TRACK_PATTERN = re.compile(r"^(.*?)( - )(.*?)$")
LOG_FILENAME = 'pastebin_upload.log'


def replace_artist_with_track_number(tracks):
    reformatted_tracks = []
    for track_number, track in enumerate(tracks, start=1):
        match = ARTIST_TRACK_PATTERN.match(track)
        if match:
            artist, separator, title = match.groups()
            formatted_track_number = f"{track_number:02d}"
            new_track = f"{formatted_track_number}{separator}{title}"
            reformatted_tracks.append(new_track)
        else:
            logging.warning(f"Track '{track}' does not match the expected format.")
    return reformatted_tracks


def upload_to_pastebin(api_key, user_key, title, text):
    data = {
        'api_dev_key': api_key,
        'api_user_key': user_key,
        'api_option': 'paste',
        'api_paste_code': text,
        'api_paste_private': '1',  # 0=public, 1=unlisted, 2=private
        'api_paste_expire_date': 'N',  # Never expires, 10M is ten minute, 24H or 1D should be one day and so on. API docs are down right now and I can't check 'em
        'api_paste_name': title,
    }
    try:
        response = requests.post(PASTEBIN_API_URL, data=data)
        if response.status_code == 200:
            logging.info("Pastebin upload successful.")
            return response.text  # Pastebin returns the URL of the paste as plain text
        else:
            logging.error(f"Pastebin upload failed with status code {response.status_code}. Response: {response.text}")
            return None
    except RequestException as e:
        logging.error(f"Pastebin upload failed with exception: {e}")
        return None


def upload_to_gist(token, title, text):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
    }
    data = {
        'description': title,
        'public': False,
        'files': {
            f'{title}.txt': {
                'content': text,
            },
        },
    }
    try:
        response = requests.post(GITHUB_GISTS_API_URL, headers=headers, json=data)
        if response.status_code == 201:
            gist_url = response.json()['html_url']
            logging.info(f"Gist upload successful. URL: {gist_url}")
            return gist_url
        else:
            logging.error(f"Gist upload failed with status code {response.status_code}. Response: {response.json()}")
            return None
    except RequestException as e:
        logging.error(f"Gist upload failed with exception: {e}")
        return None


def clear_clipboard():
    pyperclip.copy('')


def main():
    # Configure logging
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the tracklist from the clipboard
    input_tracks = pyperclip.paste()
    tracks = input_tracks.split('\n')

    # Replace artist names with track numbers
    reformatted_tracks = replace_artist_with_track_number(tracks)
    reformatted_text = '\n'.join(reformatted_tracks)

    # Prompt user for Pastebin title
    pastebin_title = input("Enter a title for your Pastebin upload: ")

    # Attempt Pastebin upload
    paste_url = upload_to_pastebin(PASTEBIN_API_KEY, PASTEBIN_USER_KEY, pastebin_title, reformatted_text)

    if paste_url:
        print(f"Reformatted tracks have been uploaded to Pastebin: {paste_url}")
        logging.info(f"Reformatted tracks uploaded to Pastebin: {paste_url}")
        pyperclip.copy(paste_url)
        print("The link has been copied to your clipboard.")
    else:
        print("Pastebin upload failed. Attempting to upload to Gist as a backup.")
        gist_url = upload_to_gist(GITHUB_TOKEN, pastebin_title, reformatted_text)
        if gist_url:
            print(f"Reformatted tracks have been uploaded to Gist: {gist_url}")
            logging.info(f"Reformatted tracks uploaded to Gist: {gist_url}")
            pyperclip.copy(gist_url)
            print("The link has been copied to your clipboard.")
        else:
            print("Gist upload failed. Clipboard will be cleared.")
            clear_clipboard()