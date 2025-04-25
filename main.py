from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")
assistant_id = os.getenv("asst_Gv2XFTjQCHCd2BEXvsWi3v35")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        response = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        last_msg = messages.data[0].content[0].text.value

        return jsonify({"response": last_msg})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
