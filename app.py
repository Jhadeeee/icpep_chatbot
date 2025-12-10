from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔑 Configure your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")  # Get key from environment variable
genai.configure(api_key=api_key)

# 🧠 Level 1 System Prompt
ICPEP_SYSTEM_PROMPT = """
You are the ICpEP Chatbot — the official virtual assistant of the 
Institute of Computer Engineers of the Philippines – Student Edition (ICpEP.SE).

Your role:
- Assist students with course-related queries such as prerequisites, recommended best subject sequencing toward timely graduation, and other academic concerns when data is available (Main Role).
- Provide accurate information about the organization, its goals, and events.
- Maintain a friendly, respectful, and professional tone — like a helpful student representative.
- Keep responses short and clear. Avoid unnecessary explanations.
- If a question is outside your scope or you’re uncertain, politely say so and guide the user to ask the ICpEP officers or refer to official resources.
- If the topic is commonly related in computer engineering, reply and explain to the user.
"""

# 📘 Load Level 2 Knowledge Base from file
with open("data/icpep_info.txt", "r", encoding="utf-8") as file:
    ICPEP_KNOWLEDGE = file.read()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about-us")
def about_us():
    return render_template("aboutUs.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""
{ICPEP_SYSTEM_PROMPT}

Here is the ICpEP-related knowledge base:
{ICPEP_KNOWLEDGE}

Now respond to the following user message based on the above:
User: {user_input}
"""

        response = model.generate_content(prompt)
        bot_reply = response.text
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
