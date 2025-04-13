from flask import Flask, request

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_script():
    # Your script logic here (call function, run something, etc.)
    data = request.json  # optional
    print("Webhook triggered!", data)
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
