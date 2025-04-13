from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_script():
    # Your script logic here (call function, run something, etc.)
    data = request.get_json()  # Corrected this line
    Plan = data.get("Plan")
    Variation = data.get("Variation")
    Keywords = data.get("Keywords")
    Message = data.get("Message")
    print("Webhook triggered!", data)
    return str(f"Plan: {Plan}. Variation: {Variation}, {Message}, {Keywords}"), 200  # Using jsonify to ensure proper JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
