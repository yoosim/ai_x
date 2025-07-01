from dotenv import load_dotenv
from decouple import config
import os

# 방법1
load_dotenv()
client_id = os.getenv('CLIENT_ID')
print('방법 1:', client_id)

# 방법2
client_id = config('CLIENT_ID')
print('방법 2:',client_id)