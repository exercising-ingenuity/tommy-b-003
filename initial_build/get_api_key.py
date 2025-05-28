import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('/home/tommy_b/Downloads/.env')

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

# Access api key
#api_key = os.environ.get("OPEN_API_KEY")
api_key = os.environ.get("OPEN_API_KEY")

# Use api key
print(f"The API key is: {api_key}")
