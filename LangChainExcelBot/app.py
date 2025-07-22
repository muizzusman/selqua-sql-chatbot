from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_setup import agent

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print("📨 Received data:", data)

    query = data.get("message")
    if not query:
        print("❌ No message received.")
        return jsonify({"answer": "No message received"}), 400

    try:
        print("🤖 Running agent with query:", query)
        result = agent.invoke(f"""
Ignore variable names like `unique_users`. 
JUST output the final list directly in plain English.
ONLY use Excel data. QUESTION: {query}
""")

        if isinstance(result, dict) and "output" in result:
            result = result["output"]
            # If result contains a list, convert to clean comma-separated string
            if isinstance(result, list):
                result = ', '.join(map(str, result))

# OR handle weird strings like "This includes: [...]"
        if "This includes:" in result:
            start = result.find("[")
            end = result.find("]") + 1
            if start != -1 and end != -1:
                try:
                    # Evaluate the list inside string
                    raw_list = eval(result[start:end])
                    result = ', '.join(map(str, raw_list))
                except:
                    pass

        else:
            result = str(result)

        if not result.strip():
            result = "❗ No answer found. Try rephrasing the question."

        print("✅ Response:", result)
        return jsonify({"answer": result})

    except Exception as e:
        print("❌ Exception:", e)

        if "Could not parse LLM output" in str(e) or "parsing error" in str(e).lower():
            return jsonify({"answer": "❗ I had trouble understanding the data. Please rephrase or ask a simpler question."})

        return jsonify({"answer": "❌ Something went wrong. Try again later."})

if __name__ == '__main__':
    app.run(debug=True)