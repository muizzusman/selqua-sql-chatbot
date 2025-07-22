import json
import sqlite3
import pandas as pd
import os

# Setup database
conn = sqlite3.connect("chatbot_data.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    user_name TEXT,
    user_email TEXT,
    created_at TEXT,
    updated_at TEXT,
    exported_at TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    role TEXT,
    say TEXT,
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
)
''')

# Folder with JSON files
json_folder = "data"

# Loop through all JSON files
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract metadata
        meta = data["metadata"]
        user = meta["user"]
        dates = meta["dates"]

        # Insert into chats table
        cursor.execute('''
        INSERT INTO chats (title, user_name, user_email, created_at, updated_at, exported_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get("title", "No Title"),
            user.get("name", ""),
            user.get("email", ""),
            dates.get("created", ""),
            dates.get("updated", ""),
            dates.get("exported", "")
        ))

        chat_id = cursor.lastrowid

        # Insert messages
        for msg in data["messages"]:
            cursor.execute('''
            INSERT INTO messages (chat_id, role, say)
            VALUES (?, ?, ?)
            ''', (chat_id, msg["role"], msg["say"]))

# Commit and close DB connection
conn.commit()

# Export to Excel
df_chats = pd.read_sql_query("SELECT * FROM chats", conn)
df_chats.to_excel("chats.xlsx", index=False)

df_messages = pd.read_sql_query("SELECT * FROM messages", conn)
df_messages.to_excel("messages.xlsx", index=False)

conn.close()
print("✅ All chats processed and saved into chatbot_data.db, chats.xlsx, and messages.xlsx")