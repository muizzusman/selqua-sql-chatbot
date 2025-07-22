import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import OllamaLLM

# Load Excel files
chat_df = pd.read_excel("chat.xlsx")
messages_df = pd.read_excel("messages.xlsx")

# Optional: Tag source
chat_df["__source__"] = "chat"
messages_df["__source__"] = "messages"

# Merge into one DataFrame
combined_df = pd.concat([chat_df, messages_df], ignore_index=True)

# Load Mistral via Ollama
llm = OllamaLLM(model="mistral")

# print("PREVIEW DATA:")
# print(combined_df.head())

print(f"✅ Loaded DataFrame with {combined_df.shape[0]} rows and {combined_df.shape[1]} columns")

# ✅ Must set allow_dangerous_code=True or it will throw an error
agent = create_pandas_dataframe_agent(
    llm,
    combined_df,
    verbose=False,
    allow_dangerous_code=True,
    return_intermediate_steps=True
)