from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Add this
from agent_setup import agent

app = Flask(__name__)
CORS(app)  # ✅ Allow requests from anywhere

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print("📨 Received data:", data)

    query = data.get("message")
    if not query:
        print("❌ No message received.")
        return jsonify({"error": "No message received"}), 400

    try:
        print("🤖 Running agent with query:", query)
        result = agent.run("ONLY use Excel data. QUESTION: " + query)
        print("✅ Response:", result)
        return jsonify({"answer": result})
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
