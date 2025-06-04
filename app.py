from flask import Flask, request, jsonify
import requests
import os
import json
import time
import random

OWNER = os.getenv("OWNER")
TOKEN = os.getenv("TOKEN")
BOTTOKEN = os.getenv("BOTTOKEN")
USERTOKEN = os.getenv("USERTOKEN")
NormalREPO = os.getenv("NormalREPO")
AviationREPO = os.getenv("AviationREPO")
BASEVARIABLE = os.getenv("BASEVARIABLE")
BaseVariable = f"{BASEVARIABLE}\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable"

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_script():
    # Your script logic here (call function, run something, etc.)
    data = request.get_json()  # Corrected this line
    print("Webhook received!")
    print("Data received:")
    print(data)
    Plan = str(data.get("Plan"))	


    def ChooseREPO():
        if Plan == "Normal":
            return NormalREPO
        elif Plan == "Aviation":
            return AviationREPO
        else:
            print("Wrong input")
            exit()    

    def LoadVariables(REPO):
        V_Names = []
        V_Values = []
        newtable = []
        Scheduler_Value = 0
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        page = 1
        while True:
            response = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables?page={page}&per_page=100', headers=headers)
            print(response.status_code)
            vgd = response.json()
            if 'variables' not in vgd or not vgd['variables']:
              break
            variables = vgd['variables']
            for v in variables:
                V_Name = str(v["name"])
                if V_Name.startswith("AD"):
                    V_Names.append(str(v["name"]))
                    V_Values.append(v["value"])
                elif V_Name == "SCHEDULER":
                    Scheduler_Value = v["value"]
                elif V_Name == "DISCORD_URLS":
                    v = v["value"]
                    table = v.split(",")
                    for t in table:
                        newtable.append(int(t.strip()))
            page += 1
            print(f"V_Names: {V_Names}")
        return V_Names, V_Values, Scheduler_Value, newtable

    def PrintVariables():
        AdNames, AdValues, No, Ze = LoadVariables(ChooseREPO())
        Keywords = []
        for AdValue in AdValues:
            Splitted1 = AdValue.split("\n=divider=\n")
            Splitted2 = AdValue.split("\r\n=divider=\r\n")
            if len(Splitted1) == 5:
                Keyword = Splitted1[3]
                Keywords.append(Keyword)
            elif len(Splitted2) == 5:
                Keyword = Splitted2[3]
                Keywords.append(Keyword)
            else:
                Keyword = "Base Variable"
                Keywords.append(Keyword)
        return Keywords

    Thing = PrintVariables()
    print("Webhook triggered!", data)
    response = {
        "DisMessage": Thing,}
    return response, 200  # Using jsonify to ensure proper JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # Corrected this line
    print("Webhook received!")
    print("Data received:")
    print(data)
    TicketID = str(data.get("TicketID"))     
    Plan = str(data.get("Plan"))
    PostedBefore = str(data.get("PostedBefore"))
    MessageID = int(data.get("MessageID"))
    Variation = str(data.get("Variation"))
    Keywords = str(data.get("Keywords"))    
    WhichVar = data.get("WhichVariables")

    def ChooseREPO():
        print("Choosing repository based on plan")
        if Plan == "Normal":
            return NormalREPO
        elif Plan == "Aviation":
            return AviationREPO
        else:
            print("Wrong input")
            exit()
    REPO = ChooseREPO()

    def LoadVariables(REPO):
        print("Loading variables from GitHub Actions")
        print(f"Using repository: {REPO}")
        V_Names = []
        V_Values = []
        newtable = []
        Scheduler_Value = 0
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        page = 1
        while True:
            response = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables?page={page}&per_page=100', headers=headers)
            print(response.status_code)
            vgd = response.json()
            if 'variables' not in vgd or not vgd['variables']:
              break
            variables = vgd['variables']
            for v in variables:
                V_Name = str(v["name"])
                if V_Name.startswith("AD"):
                    V_Names.append(str(v["name"]))
                    V_Values.append(v["value"])
                elif V_Name == "SCHEDULER":
                    Scheduler_Value = v["value"]
                elif V_Name == "DISCORD_URLS":
                    v = v["value"]
                    table = v.split(",")
                    for t in table:
                        newtable.append(int(t.strip()))
            page += 1
        print(f"V_Names: {V_Names}")
        return V_Names, V_Values, Scheduler_Value, newtable
    Names, Values, Scheduler_Value, IDS = LoadVariables(REPO)

    def CreateMessage(MessageID):
        headers = {
            'Authorization': f"Bot {BOTTOKEN}",
            'User-Agent': 'DiscordBot (https://example.com, v1)',
            'Content-Type': 'application/json'
        }
        url = f'https://discord.com/api/v10/channels/1370801657675251843/messages/{MessageID}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            message_data = response.json()
            content = message_data.get('content', '')
            return content
        else:
            print("Failed to fetch message.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    Message = CreateMessage(MessageID)

    if str(PostedBefore) == "Yes":

        def GetGuildIds(IDS):
            print("Getting Guild IDs from Advertising Channels")
            ids = [id.strip() for id in str(IDS).split(",")]
            GuildIds = []
            IdsWithoutErrors = ids.copy()
            Errors = []
            header = {"Authorization": USERTOKEN}
            for AdId in ids:
                response = requests.get(f"https://discord.com/api/v10/channels/{AdId}", headers=header)
                if response.status_code == 200:
                    data = response.json()
                    guildId = int(data["guild_id"])
                    GuildIds.append(guildId)
                else:
                    Errors.append(AdId)
                    IdsWithoutErrors.remove(AdId)
                    print(f"Error with AdvertisingChannel Id: {response.status_code}")
            print(f"GuildIds: {GuildIds}")
            return GuildIds, IdsWithoutErrors

        GuildIds, IdsWithoutErrors = GetGuildIds(IDS)

        def SearchForPosts(GuildIDs, Keywords):
            print("Searching for posts with Keywords:", Keywords)
            totalposts = 0
            author_ids = [1148657062599983237,841925129323020298, 1285602869638070304, 1303383091468963841, 1338561709228687443]
            for Id in GuildIDs:
                print(f"KeyWords: {Keywords}")
                header = {"Authorization":USERTOKEN}
                params = {"content": Keywords, "author_id": author_ids, "limit": 25}
                link = f"https://discord.com/api/v9/guilds/{Id}/messages/search"
                time.sleep(random.uniform(5,7))
                response = requests.get(link, headers=header, params=params)
                if response.status_code == 200:
                    data =response.json()
                    total_results = data["total_results"]
                    totalposts += total_results
                    print(f"Total results: {total_results}")
                else:
                    print(f"Error with Guild Id: {Id} with status code: {response.status_code}")
            return totalposts 

        totalposts = SearchForPosts(GuildIds, Keywords)

        def CreateVariable(totalposts, Keywords):
            print("Creating variable with totalposts:", totalposts, "and Keywords:", Keywords)
            if Variation == "Free":
                Days = 3
            else:
                Days = 7
            if Variation == "Free":
                Posts = 450
            elif Variation == "Basic":
                Posts = 700
            elif Variation == "Advanced":
                Posts = 900
            elif Variation == "Pro":
                Posts = 1400
            elif Variation == "God's":
                Posts = 2100
            TotalPosts = Posts + int(totalposts)
            Final_Variable = f"{Message}\n=divider=\n{TotalPosts}\n=divider=\n{Days}\n=divider=\n{Keywords}\n=divider=\n{TicketID}"
            return Final_Variable

        Final_Variable = CreateVariable(totalposts, Keywords)

        def UpdateVariables(Text, Names, WhichVariable, REPO):
            print("Updating variables with Text:", Text)
            print("Names of variables:", Names)
            Varaibles = WhichVariable.split(",")
            for Var in Varaibles:
                print(int(Var) - 1)
                NAME = Names[int(Var) - 1]
                headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json',}
                data = {"value": Text}
                response = requests.patch(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{NAME}',
                headers=headers, json=data)
                print(f" Updating status code: {response.status_code}, Updating text: {response.text}")
        UpdateVariables(Final_Variable, Names, WhichVar, REPO)
        print("Webhook triggered!", data)

    elif str(PostedBefore) == "No":

        def CreateVariable(Keywords):
            print("Creating variable with Keywords:", Keywords)
            
            if Variation == "Free":
                Days = 3
            else:
                Days = 7
            if Variation == "Free":
                Posts = 450
            elif Variation == "Basic":
                Posts = 700
            elif Variation == "Advanced":
                Posts = 900
            elif Variation == "Pro":
                Posts = 1400
            elif Variation == "God's":
                Posts = 2100
            Final_Variable = f"{Message}\n=divider=\n{Posts}\n=divider=\n{Days}\n=divider=\n{Keywords}\n=divider=\n{TicketID}"
            print("Final Variable created:", Final_Variable)
            return Final_Variable
        
        Final_Variable = CreateVariable(Keywords)

        def UpdateVariables(Text, Names, WhichVariable, REPO):
            print("Updating variables with Text:", Text)
            print("Names of variables:", Names)
            Varaibles = WhichVariable.split(",")
            for Var in Varaibles:
                print(int(Var) - 1)
                NAME = Names[int(Var) - 1]
                headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json',}
                data = {"value": Text}
                response = requests.patch(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{NAME}',
                headers=headers, json=data)
                print(f" Updating status code: {response.status_code}, Updating text: {response.text}")
                response = response.status_code, response.text
            return "b"

        response = UpdateVariables(Final_Variable, Names, WhichVar, REPO)
        print("Webhook triggered!", data)
    else:
        print("Something with postedbefore")
    return response

@app.route('/variables', methods=['POST'])
def variables():
    data = request.get_json()
    print(data)
    Variables = str(data.get("Variables"))
    print(Variables)
    Repository = str(Variables.split("<=divid=>")[0])
    WhichVar = str(Variables.split("<=divid=>")[1])
    def ChooseREPO():
        if Repository == "Normal":
            return NormalREPO
        elif Repository == "Aviation":
            return AviationREPO
        else:
            print("Wrong input")
            exit()
    def LoadVariables(REPO):
        V_Names = []
        V_Values = []
        newtable = []
        Scheduler_Value = 0
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        page = 1
        while True:
            response = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables?page={page}&per_page=100', headers=headers)
            print(response.status_code)
            vgd = response.json()
            if 'variables' not in vgd or not vgd['variables']:
              break
            variables = vgd['variables']
            for v in variables:
                V_Name = str(v["name"])
                if V_Name.startswith("AD"):
                    V_Names.append(str(v["name"]))
                    V_Values.append(v["value"])
                elif V_Name == "SCHEDULER":
                    Scheduler_Value = v["value"]
                elif V_Name == "DISCORD_URLS":
                    v = v["value"]
                    table = v.split(",")
                    for t in table:
                        newtable.append(int(t.strip()))
            page += 1
        print(f"V_Names: {V_Names}")
        return V_Names, V_Values, Scheduler_Value, newtable
    V_Names, V_Values, Scheduler_Value, IDS = LoadVariables(ChooseREPO())
    def UpdateVariables(Text, WhichVariable, REPO, V_Names):
        Varaibles = WhichVariable.split(",")
        for Var in Varaibles:
                NAME = V_Names[int(Var) - 1]
                headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json',}
                data = {"value": Text}
                response = requests.patch(f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{NAME}',
                headers=headers, json=data)
                print(f" Updating status code: {response.status_code}, Updating text: {response.text}")
    UpdateVariables(BaseVariable, WhichVar, ChooseREPO(), V_Names)
    print("Webhook triggered!", data)
    return "Webhook received!", 200

@app.route('/cron', methods=['GET'])
def cron():
    return "Cron job is running!"
