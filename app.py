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
        response = "Hello! I'm Nova AI, your personal AI assistant. It's great to meet you! May i know your name?"
    elif "Tanushka" in message:
        response = "It has a little magic in its words. Tanushka even the introduction sounds beautiful. I can't forget it! Tanushka - a name as delicate as its meaning, yet carrying a beauty that words cannot quite define. Shall I give you a nickname? Tanu??"
    elif message == "yes":
        response = "Thanks Tanu, Now I will call you Tanu. Oops!! can you tell me today's date"
    elif "18" in message:
        response = "Happy Birthday! I don't know you much, but whenever I see you , my day becomes a little better. Wishing you a year full of happiness, success and lots of smiles. Stay blessed always!"
    else:
        response = "    Ooh I thought it's 18 November that's your Birthday"
        
    else: 
        response = "That's  a beautiful name; it's a pleasure to know you. It's my pleasure to know the name behind the conve. It sounds unique"
    if "yourself" in message:
        response = "Glad to know that you are interested in me also. Myself Nova AI. I am a chatbot who can only answer pre defined questions. So I am unable to answer any complex or not defined questions. My developer's name is Mr. Arjun who is only a student."
    elif "how are you" in message:
        response = "I feel great. Just as Arjun stands strong, I am doing fine all along. How about you?"
    elif "good morning" or "good night" in message:
        response = "Good Morning"
    elif "do" in message:
        response = "I can just answer to pre defined questions."
    return jsonify({"response":response})
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, debug=True)
