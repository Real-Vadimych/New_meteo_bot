import os

from dotenv import load_dotenv

load_dotenv()



token = os.getenv('TELEGRAM_TEST_TOKEN')
print(token)
