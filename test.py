from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
database_url = os.getenv('DB_NAME')


print(f"Database URL: {database_url}")

