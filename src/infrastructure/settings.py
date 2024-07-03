import os

from dotenv import load_dotenv

load_dotenv(".env")
WEBSITE_URL = "https://apnews.com/"
SEARCH_TEXT = os.environ.get("SEARCH_TEXT")
FILTER_TO_SELECT = os.environ.get("FILTER_TO_SELECT")
# WEBSITE_URL = "https://www.latimes.com/"
# SEARCH_TEXT = os.environ.get("SEARCH_TEXT")
# FILTER_TO_SELECT = os.environ.get("FILTER_TO_SELECT")

