from flask import Flask, request, jsonify
import requests
import os
import json
import time
import random


TOKEN = os.getenv("TOKEN")
BOTTOKEN = os.getenv("BOTTOKEN")
USERTOKEN = os.getenv("USERTOKEN")
REPO = os.getenv("REPO")
BASEVARIABLE = os.getenv("BASEVARIABLE")
OWNER = "SimonGamer1234"
REPO = "ms"
BaseVariable = f"{BASEVARIABLE}\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable\n=divider=\nBase_Variable"
app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_script():
    # Your script logic here (call function, run something, etc.)
    data = request.get_json()  # Corrected this line
    print("Webhook received!")
    print("Data received:")
    print(data)
    Plan = str(data.get("Plan"))	

    def SetVariables(Plan):
        if Plan == "Normal":
            return "NORMAL_ADS"
        elif Plan == "Aviation":
            return "AVIATION_ADS"
        

    def LoadVariables(VariableName):
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        value = data.get('value',None)
        variables1 = value.split("\n\n++THESPLITTER++\n\n")
        variables2 = value.split("\r\n\r\n++THESPLITTER++\r\n")
        if len(variables1) > 1:
            variables = variables1
        elif len(variables2) > 1:
            variables = variables2
        else:
            print("No variables found")
            return []
        return variables

    def PrintVariables(Values):
        Keywords = []
        n = 0
        print(Values)
        for AdValue in Values:
            n += 1
            Splitted1 = AdValue.split("\n=divider=\n")
            Splitted2 = AdValue.split("\r\n=divider=\r\n")
            if len(Splitted1) == 5:
                Keyword = Splitted1[3]
                Keywords.append(f"{n}. {Keyword}\n")
            elif len(Splitted2) == 5:
                Keyword = Splitted2[3]
                Keywords.append(f"{n}. {Keyword}\n")
            else:
                Keyword = "Base Variable"
                Keywords.append(f"{n}. {Keyword}\n")
            print(Keywords)
        return Keywords
    VariableName = SetVariables(Plan)
    AdValues = LoadVariables(VariableName)
    Thing = PrintVariables(AdValues)
    print("Webhook triggered!", data)
    response = {
        "DisMessage": Thing,}
    return response, 200  # Using jsonify to ensure proper JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

@app.route('/webhook', methods=['POST'])
def webhook():
    

    def SetVariables(Plan):
        if Plan == "Normal":
            return "NORMAL_ADS"
        elif Plan == "Aviation":
            return "AVIATION_ADS"

    def LoadVariables(VariableName):
        def LoadVariables(VariableName):
            url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
            headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            value = data.get('value',None)
            print(f"Value of {VariableName}: {value}")
            variables1 = value.split("\n\n++SPLITTER++\n\n")
            variables2 = value.split("\r\n\r\n++SPLITTER++\r\n")
            if len(variables1) > 1:
                variables = variables1
                return variables
            elif len(variables2) > 1:
                variables = variables2
                return variables
            else:
                print("No variables found")
                return []
        def LoadIDS(VariableName):
            url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
            headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            value = data.get('value', None)
            if value:
                ids = value.split(",")
                return [int(id.strip()) for id in ids]
            else:
                print("No Discord URLs found")
                return []
        IDS = LoadIDS("DISCORD_URLS")
        variables = LoadVariables(VariableName)
        return variables, IDS

    def CreateMessage(MessageID):
        url = f"https://discord.com/api/v10/channels/1370801657675251843/messages/{MessageID}"
        print(f"Fetching message from URL: {url}")

        headers = {
         "Authorization": f"Bot {BOTTOKEN}",
         "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("Message Content:", data.get("content"))
            return data.get("content")
        else:
            print(f"Failed to fetch message: {response.status_code} - {response.text}")
            return BASEVARIABLE
        
    


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


    def CreateValue(totalposts, Keywords, Message, Variation, TicketID):
        print("Creating variable with totalposts:", totalposts, "and Keywords:", Keywords)
        if Variation == "Free":
            Postings = 9
        elif Variation == "Basic":
            Postings = 14
        elif Variation == "Advanced":
            Postings = 21
        elif Variation == "Pro":
            Postings = 28
        elif Variation == "God's": 
            Postings = 42
        else:
            print("Something went wrong with Variation")    
        totalposts = totalposts + (Postings * 50)
        Final_Variable = f"{Message}\n=divider=\n{Variation}\n=divider=\n{totalposts}\n=divider=\n{Postings}\n=divider=\n{Keywords}\n=divider=\n{TicketID}"
        return Final_Variable


    def CreateVariable(Text, Values, WhichVariable):
        print("Updating variables with Text:", Text)
        print("Names of variables:")
        Varaibles = WhichVariable.split(",")
        for Var in Varaibles:
            Values[int(Var) - 1] = Text
        print("Updated Values:", Values)
        return "\n\n++SPLITTER++\n\n".join(Values)

    def UpdateVariables(VariableName, Text):
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json',
        }
        payload = {
            'value': Text
        }
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 204:
            print("Variables updated successfully")
        else:
            print(f"Failed to update variables: {response.status_code} - {response.text}")

        return "b"

    
    
    def Main():
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
        VariableName = SetVariables(Plan)
        Values, IDS = LoadVariables(VariableName)
        Message = CreateMessage(MessageID)
        print(f"Values: {Values}")


        if str(PostedBefore) == "true":
            GuildIds, IdsWithoutErrors = GetGuildIds(IDS)
            totalposts = SearchForPosts(GuildIds, Keywords)         
            Final_Variable = CreateValue(totalposts, Keywords, Message, Variation, TicketID)
            Final_Variable = CreateVariable(Final_Variable, Values, WhichVar)

        elif str(PostedBefore) == "false":
            Final_Variable = CreateValue(0, Keywords, Message, Variation, TicketID)
            Final_Variable = CreateVariable(Final_Variable, Values, WhichVar)
            
        else:
            print("Something with postedbefore")
        response = UpdateVariables(VariableName, Final_Variable)

        return response
    response = Main()
    return response 

    



@app.route('/variables', methods=['POST'])
def variables():
    data = request.get_json()
    Plan = str(data.get("Plan"))
    WhichVar = str(data.get("WhichVariables"))
    def SetVariables(Plan):
        if Plan == "Normal":
            return "NORMAL_ADS"
        elif Plan == "Aviation":
            return "AVIATION_ADS"

    def LoadVariables(VariableName):
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        data = response.json()
        print(f"Data received: {data}")
        value = data.get('value')
        variables1 = value.split("\n\n++SPLITTER++\n\n")
        variables2 = value.split("\r\n\r\n++SPLITTER++\r\n\r\n")
        if len(variables1) > 1:
            variables = variables1
        elif len(variables2) > 1:
            variables = variables2
        else:
            print("No variables found")
            return []
        return variables
    
    def CreateValue(Values,WhichVariable):
        print("creating value")
        Varaibles = WhichVariable.split(",")
        for Var in Varaibles:
            Values[int(Var) - 1] = BaseVariable
        return "\n\n++SPLITTER++\n\n".join(Values)
    
    def UpdateVariables(VariableName, Text):
        print("updating vars")
        url = f'https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{VariableName}'
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {TOKEN}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json',
        }
        payload = {
            'value': Text
        }
        response = requests.patch(url, headers=headers, json=payload)
        print(response.status_code)
        if response.status_code == 200:
            print("Variables updated successfully")
        else:
            print(f"Failed to update variables: {response.status_code} - {response.text}")
       
    VariableName = SetVariables(Plan)
    Values = LoadVariables(VariableName)
    FinalValue = CreateValue(Values, WhichVar) 
    UpdateVariables(VariableName, FinalValue)
    print("Webhook triggered!", data)
    return "Webhook received!", 200

@app.route('/cron', methods=['GET'])
def cron():
    return "Cron job is running!"
