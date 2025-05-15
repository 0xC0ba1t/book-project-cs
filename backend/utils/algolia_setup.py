# run only once / if db updated

import requests
from algoliasearch.search.client import SearchClientSync
import os

# Load API password from environment variable
API_PASSWORD = os.environ.get("API_PASSWORD")
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")

# Fetch data
url = "https://8000-01jtrkrgvb5brn7hg3gkn1gyv1.cloudspaces.litng.ai/dump-db"
headers = {
    "Authorization": f"Bearer {API_PASSWORD}"
}
response = requests.get(url, headers=headers)
books = response.json()["books"]  # Extract just the list

# Connect and authenticate with your Algolia app
_client = SearchClientSync(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

# Save records in Algolia index
_client.save_objects(
    index_name="books_db_index",
    objects=books,
)
