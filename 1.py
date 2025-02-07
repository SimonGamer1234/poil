import os
import random
import requests
import time
import json

# Retrieve the environment variables
AD1 = os.getenv("REPO_VAR_1")
AD2 = os.getenv("REPO_VAR_2")
AD3 = os.getenv("REPO_VAR_3")
AD4 = os.getenv("REPO_VAR_4")
AD5 = os.getenv("REPO_VAR_5")
AD6 = os.getenv("REPO_VAR_6")
AD7 = os.getenv("REPO_VAR_7")
AD8 = os.getenv("REPO_VAR_8")
AD9 = os.getenv("REPO_VAR_9")
AD10 = os.getenv("REPO_VAR_10")
AD11 = os.getenv("REPO_VAR_11")
AD12 = os.getenv("REPO_VAR_12")
URLS = os.getenv("URLS")
TOKEN1 = os.getenv("TOKEN_SCRT_1")
TOKEN2 = os.getenv("TOKEN_SCRT_2")
TOKEN3 = os.getenv("TOKEN_SCRT_3")
TOKEN4 = os.getenv("TOKEN_SCRT_4")

urls = URLS.split(',')
Errors = []
Ads = [AD1, AD2, AD3, AD4, AD5, AD6, AD7, AD8, AD9, AD10, AD11, AD12]
Tokens = [TOKEN1, TOKEN2, TOKEN3, TOKEN4]
tracker_file = "ad_tracker.txt"

if not os.path.exists(tracker_file):
    with open(tracker_file, "w") as file:
        file.write("0")  # Initialize with 0
with open(tracker_file, "r") as file:
    current_ad = int(file.read().strip())

token_index = current_ad % 4  # Use a descriptive variable name
print(current_ad)
print(token_index)
Token = Tokens[token_index]
CurrentAd = Ads[current_ad]


header = {"Authorization": Token}
payload = {"content": CurrentAd}
unauthorized = 0
# Loop through the links and make POST requests
for link in urls:
    sleeptime = random.uniform(2, 3)
    try:
        res = requests.post(link, data=payload, headers=header)
        print(f"Posted to {link} : {res.status_code}")  # Print response status
        print(res.text)
        if res.status_code != 200:
            Errors.append((link,res.status_code,token_index,"Normal"))
        if res.status_code == 401:
            unauthorized = 1
    except requests.RequestException as e:
        print(f"Error posting to {link}: {e}")
    print(f"Waiting {sleeptime} seconds...")
    time.sleep(sleeptime)

print(unauthorized)
if unauthorized == 1:
    CONTENT = f"TOKEN {token_index} UNAUTHORIZED - Normal - <@1148657062599983237>"
else:
    CONTENT = str(Errors)
print(CONTENT)
link1 = "https://discord.com/api/v9/channels/1300080115945836696/messages"
header1 = {"Authorization": TOKEN1}
payload1 = {"content": str(Errors)}
res1 = requests.post(link1, data=payload1, headers=header1)
print(f"Posted to {link1} : {res1.status_code}")  # Print response status
