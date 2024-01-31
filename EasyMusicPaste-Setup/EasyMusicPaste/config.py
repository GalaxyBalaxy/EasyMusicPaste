#config.py

# Pastebin API configuration
PASTEBIN_API_URL = 'https://pastebin.com/api/api_post.php'
PASTEBIN_API_KEY = 'PASTEBIN_DEV_KEY'  # Replace with your actual Pastebin API key
PASTEBIN_USER_KEY = 'PASTEBIN_USER_KEY'  # Replace with your actual Pastebin user key

# GitHub Gists API configuration
GITHUB_GISTS_API_URL = 'https://api.github.com/gists'
GITHUB_TOKEN = 'GIT_TOKEN'  # Replace with your actual GitHub token, make sure it has Gist privellages

# Regex pattern to match "Artist - Track" format
ARTIST_TRACK_PATTERN = r"^(.*?)( - )(.*?)$"

# Logging configuration
LOG_FILENAME = 'pastebin_upload.log'
LOG_LEVEL = 'INFO'  # Could be DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'