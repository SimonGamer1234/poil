import os
import random
import requests
import time
import json

# Retrieve the environment variables
AD1 = os.getenv("REPO_VAR_1")  
IDSlist = os.getenv("URLS")
TOKEN1 = os.getenv("TOKEN_SCRT_1")
Errors = []
IDS = IDSlist.split(',')
Successful = 0

header = {"Authorization": TOKEN1}
payload = {"content": AD1}
unauthorized = 0
# Loop through the links and make POST requests
for ID in IDS:
    link = f"https://discord.com/api/v9/channels/{ID}/messages"
    sleeptime = random.uniform(2, 3)
    try:
        res = requests.post(link, data=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        print(res.text)
        if res.status_code != 200:
            Errors.append((link,res.status_code,token_index,"Normal"))
        if res.status_code == 401:
            unauthorized = 1
        if res.status_code == 200:
            Successful += 1
    except requests.RequestException as e:
        print(f"Error posting to {link}: {e}")
    print(f"Waiting {sleeptime} seconds...")
    time.sleep(sleeptime)

print(unauthorized)
if unauthorized == 1:
    CONTENT = f"TOKEN 1 UNAUTHORIZED - Normal - <@1148657062599983237>"
else:
    CONTENT = f"Succesfully posted: {Successful}, Errors: {str(Errors)}"
print(CONTENT)
link1 = "https://discord.com/api/v9/channels/1300080115945836696/messages"
header1 = {"Authorization": TOKEN1}
payload1 = {"content": str(Errors)}
res1 = requests.post(link1, data=payload1, headers=header1)
print(f"Posted to {link1} : {res1.status_code}")  # Print response status
