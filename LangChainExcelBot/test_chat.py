import requests

url = "http://127.0.0.1:5000/chat"
message = input("You: ")

while message.lower() not in ["exit", "quit"]:
    response = requests.post(url, json={"message": message})
    print("Bot:", response.json().get("answer", "Error"))
    message = input("You: ")
