import os, json, datetime, requests
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "nova-secret-123"
CORS(app)
TELEGRAM_TOKEN = "9257134232:AAHunXuh9eoJnFYxvvU4tNKJuB1rxzH_6A8"
TELEGRAM_CHAT_ID = "8302598279"
def send_to_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except:
        pass

def save_pending(user_msg):
    try:
        with open("pending.json", "w") as f:
            json.dump({"user_msg": user_msg, "admin_reply": ""}, f)
    except:
        pass

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def server_file(filename):
    return send_from_directory(".", filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]
    message = message.lower().strip()
    # --- YAHAN HONA CHAHIYE - SABSE UPAR ---
    if "i am fine" in message or "i am good" in message:
        return jsonify({"response": "That's great to hear! What are you doing today?"})

    #if "how are you" in message:
        #return jsonify({"response": "I feel great. How about you?"})
# --- YAHAN HONA CHAHIYE - SABSE UPAR ---
    #if "i am fine" in message or "i am good" in message:
        #return jsonify({"response": "That's great to hear! What are you doing today?"})

    #if "how are you" in message:
        #return jsonify({"response": "I feel great. How about you?"})


    # STEP 1: Hello -> Greeting + Naam pucho
    if message in ["hello", "hii", "hi", "hey", "hlo", "namaste"]:
        session["step"] = "ask_name"
        response = "Hello! I'm Nova AI, your personal AI assistant. It's great to meet you! May I know your name?"

    # STEP 2: Naam bataya -> Introduce myself pucho
    # Ye tabhi chalega jab humne naam pucha ho
    elif session.get("step") == "ask_name":
        name = message.replace("my name is", "").replace("i am", "").replace("mera naam", "").strip()
        session["user_name"] = name
        session["step"] = "ask_intro"

        if "tanushka" in message:
            response = "It has a little magic in its words. Tanushka even the introduction sounds beautiful. I can't forget it! Tanushka - a name as delicate as its meaning, yet carrying a beauty that words cannot quite define. Shall I give you a nickname? Tanu??"
        else:
            response = f"That's a beautiful name, {name.title()}! It's a pleasure to know you. Can I introduce myself?"

    # STEP 3: Introduce myself -> Yes bola to nickname pucho (sirf Tanushka ke liye)
    elif session.get("step") == "ask_intro" and message in ["yes", "ha", "haan", "yeah", "sure", "ok"]:
        session["step"] = "ask_nickname"
        if "tanushka" in session.get("user_name", ""):
            response = "Glad to know that you are interested in me also. Myself Nova AI. I am a personal AI assistant made by Arjun. Can I give you a nickname Tanu?"
        else:
            session["step"] = "normal"
            response = "Glad to know that you are interested in me also. Myself Nova AI. I am a personal AI assistant made by Arjun. So, how are you?"

    # STEP 4: Nickname ke liye Yes -> Date pucho
    elif session.get("step") == "ask_nickname" and message in ["yes", "ha", "haan", "yeah", "sure", "ok"]:
        session["step"] = "ask_date"
        response = "Thanks Tanu, Now I will call you Tanu. Oops! Can you tell me today's date?"

    # STEP 4b: Nickname ke liye No bola
    elif session.get("step") == "ask_nickname" and message in ["no", "nahi", "na"]:
        session["step"] = "normal"
        response = "Okay, no problem! So Tanushka, how are you?"

    # STEP 5: Date batayi -> 18 hai to Birthday, nahi to Sorry
    elif session.get("step") == "ask_date":
        session["step"] = "normal"
        if "18" in message:
            response = "Happy Birthday! I don't know you much, but whenever I see you, my day becomes a little better. Wishing you a year full of happiness, success and lots of smiles."
        else:
            response = "Ooh I thought it's 18 November that's your Birthday."

    # STEP 6: Ab normal baatcheet
    else:
        if "how are you" in message or "kaise ho" in message:
            response = "I feel great. Just as Arjun stands strong, I am doing fine all along. How about you?"
        elif "good morning" in message:
            response = "Good Morning! Have a wonderful day."
        elif "good night" in message:
            response = "Good Night! Sweet dreams."
        elif "good evening" in message:
            response = "Good Evening! How was your day?"
        elif "your name" in message or "tumhara naam" in message:
            response = "My name is Nova AI, made by Arjun."
        elif "who made you" in message or "kisne banaya" in message:
            response = "Arjun made me."
        elif "joke" in message:
            response = "Why did the computer go to the doctor? Because it had a virus!"
        elif "thank" in message:
            response = "You're welcome!"
        elif "bye" in message:
            session.clear()
            response = "Bye! It was nice talking to you."
        elif "i am fine" in message or "i am good" in message:
            response = "That's great to hear! What are you doing today?"
        elif "bored" in message:
            response = "Don't be bored! Let's talk about something fun. Do you want to hear a joke?"
        else:
            response = "I can just answer to pre defined questions. So I am unable to answer any complex question."
            save_pending(message)
send_to_telegram(f"Nova fas gaya!\nUser ne pucha: {message}")

    return jsonify({"response": response})
@app.route("/admin")
def admin_page():
    try:
        with open("pending.json") as f:
            data = json.load(f)
        pending = data.get("user_msg", "Koi pending nahi")
    except:
        pending = "Koi pending nahi"
    return f"<h2>Nova Admin</h2><p>User ne pucha: {pending}</p><form action='/admin_reply' method='post'><input name='reply' placeholder='Jawab likho'><button>Send</button></form>"

@app.route("/admin_reply", methods=["POST"])
def admin_reply():
    reply = request.form.get("reply")
    with open("pending.json") as f:
        data = json.load(f)
    data["admin_reply"] = reply
    with open("pending.json", "w") as f:
        json.dump(data, f)
    return "Bhej diya! <a href='/admin'>Wapas</a>"

@app.route("/check_admin_reply")
def check_admin_reply():
    try:
        with open("pending.json") as f:
            data = json.load(f)
        reply = data.get("admin_reply", "")
        if reply:
            data["admin_reply"] = ""
            with open("pending.json", "w") as f:
                json.dump(data, f)
            return jsonify({"reply": reply})
    except:
        pass
    return jsonify({"reply": ""})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
