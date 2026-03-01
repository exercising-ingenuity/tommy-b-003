from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('/home/tommy_b/Downloads/.env')

# Load te h.env file
load_dotenv(dotenv_path=dotenv_path)

# Access api key
api_key = os.environ.get("OPEN_API_KEY")

client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def chat_with_gpt(prompt):
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply


if __name__ == "__main__":
    print("ChatGPT on Raspberry Pi (type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "quit":
            break

        try:
            reply = chat_with_gpt(user_input)
            print("\nGPT:", reply)
        except Exception as e:
            print("Error:", e)