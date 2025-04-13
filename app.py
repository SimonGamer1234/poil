from flask import Flask, request, jsonify
import requests
import os
import json

OWNER = os.getenv("OWNER")
TOKEN = os.getenv("TOKEN")
NormalREPO = os.getenv("NormalREPO")
AviationREPO = os.getenv("AviationREPO")



app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_script():
    # Your script logic here (call function, run something, etc.)
    data = request.get_json()  # Corrected this line
    Plan = data.get("Plan")
    Variation = data.get("Variation")
    Keywords = data.get("Keywords")
    Message = data.get("Message")

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
            print(response.url)
            print(response.status_code)
            vgd = response.json()
            if 'variables' not in vgd or not vgd['variables']:
              break
            variables = vgd['variables']
            for v in variables:
                V_Name = v["name"]
                if V_Name.startswith("AD"):
                    V_Names.append(v["name"])
                    V_Values.append(v["value"])
                elif V_Name == "SCHEDULER":
                    Scheduler_Value = v["value"]
                elif V_Name == "DISCORD_URLS":
                    v = v["value"]
                    table = v.split(",")
                    for t in table:
                        newtable.append(int(t.strip()))
            page += 1
        return V_Names, V_Values, Scheduler_Value, newtable
    def PrintVariables():
        AdNames, AdValues, No, Ze = LoadVariables(ChooseREPO())
        Keywords = []
        for AdValue in AdValues:
            Splitted1 = AdValue.split("\n=divider=\n")
            Splitted2 = AdValue.split("\r\n=divider=\r\n")
            print(Splitted1)
            print(Splitted2)
            if len(Splitted1) == 4:
                Keyword = Splitted1[3]
                Keywords.append(Keyword)
            elif len(Splitted2) == 4:
                Keyword = Splitted2[3]
                Keywords.append(Keyword)
            else:
                Keyword = "Base Variable"
                Keywords.append(Keyword)
        return Keywords
    Thing = PrintVariables()
    print("Webhook triggered!", data)
    response = {
        "Plan": Plan,
        "Variation": Variation,
        "Message": Message,
        "Keywords": Keywords,
        "Variables": Thing,
        "DisMessage": f"Your Choices:\nPlan: {Plan}\nVariation: {Variation}\nKeywords: {Keywords}\nMessage: {Message}\n\nPick the variables you want to replace:\n{Thing}",
    }
    return jsonify(response), 200  # Using jsonify to ensure proper JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Webhook triggered!", data)
    return str(data), 200


