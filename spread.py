import pandas as pd

# Define the data
data = {
    "Query Number": list(range(1, 11)),
    "Query Description": [
        "Total number of chats",
        "Total number of messages",
        "Distinct users with chats",
        "Top 5 chats with most messages",
        "Chats that have been exported",
        "Messages from users only",
        "Messages from assistants only",
        "Most active user (by chat count)",
        "Chat with the most messages",
        "Most common message role"
    ],
    "Result": [
        "29",
        "178",
        "25+ users (e.g., Abdullah Mughal, Amna Hayat, Zuha Kamal)",
        "'SQL DML Operations Explained' has 18 messages, etc.",
        "29 chats were exported (see detailed list above)",
        "No records (role names might be labeled differently)",
        "No records (same as above)",
        "Anonymous with 6 chats",
        "'SQL DML Operations Explained' with 18 messages",
        "Prompt and Response, each 89 messages"
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("SQL_Queries_and_Results.xlsx", index=False)