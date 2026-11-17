import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return send_from_directory(".","index.html")
@app.route("/<path:filename>")
def server_file(filename):
    return send_from_directory(".", filename)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]
    message = message.lower().strip()
    if "hello" in message:
        response = "Hello"
    else:
        response = "Sorry"
    return jsonify({"response":response})
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=True)