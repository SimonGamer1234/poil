import os
import random
import requests
import time
import json

# Retrieve the environment variables
AD1 = os.getenv("REPO_VAR_1")  
URLS = os.getenv("URLS")
TOKEN1 = os.getenv("TOKEN_SCRT_1")
Errors = []
urls = URLS.split(',')

header = {"Authorization": TOKEN1}
payload = {"content": AD1}




# Loop through the links and make POST requests
for link in urls:
    sleeptime = random.uniform(2, 3)
    try:
        res = requests.post(link, data=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        if res.status_code != 200:
          Errors.append(link)
    except requests.RequestException as e:
        print(f"Error posting to {link}: {e}")
    print(f"Waiting {sleeptime} seconds...")
    time.sleep(sleeptime)

print(Errors)
link1 = https://discord.com/api/v9/channels/1300080115945836696/messages
header1 = {"Authorization": TOKEN1}
payload1 = {"content": Errors}
res = requests.post(link1, data=payload1, headers=header1)
