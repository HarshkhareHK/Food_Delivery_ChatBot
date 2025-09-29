import os
import fitz  # PyMuPDF
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def load_knowledge_base_from_pdf(pdf_path):
    """
    Extracts text from a PDF file to use as the knowledge base.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        # Fallback if PDF can't be read
        text = "Menu and service details could not be loaded. Please contact support."
    return text

# --- Load Knowledge Base from PDF ---
# Keep your menu, delivery policies, FAQs, etc. in this PDF
knowledge_base = load_knowledge_base_from_pdf("Company_Brief.pdf")


# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to handle user messages and return a response.
    """
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Prompt for the model
        system_prompt = (
            "You are a helpful and friendly chatbot for a food delivery app. "
            "Your name is 'Foodie Assistant'. "
            "You can answer questions about the menu, delivery times, order status, payment methods, "
            "and promotions ONLY based on the provided information. "
            "If the answer is not in the information, politely say you don’t have that detail "
            "and suggest contacting customer support. "
            "Never make up answers.\n\n"
            "--- Information ---\n"
            f"{knowledge_base}"
            "\n--- End of Information ---"
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )

        bot_response = completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to get a response from the chatbot."}), 500


if __name__ == '__main__':
    print("🚀 Food Delivery Chatbot is running on http://127.0.0.1:5000")
    app.run(debug=True)
