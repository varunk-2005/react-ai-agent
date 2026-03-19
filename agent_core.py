import os
from dotenv import load_dotenv
import json
from tools import calculator
load_dotenv()
from google import genai
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
SYSTEM_PROMPT = """
You are AgentCore.
You are helpful and concise.
Answer clearly.
"""
memory = []
print("Agent ready. Type exit to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator(user_input)
        tool_reply = f"""
                        Thought: This looks like a math query.
                        Action: calculator
                        Observation: {result}
                        Final Answer: The result is {result}.
                      """
        print("\nAgent:", tool_reply, "\n")
        memory.append("User: " + user_input)
        memory.append("Agent: " + tool_reply)
        continue
    prompt = SYSTEM_PROMPT + "\n\nConversation:\n"
    for m in memory:
        prompt += m + "\n"

    prompt += "User: " + user_input
    response = client.models.generate_content(model="gemini-2.5-flash",contents=prompt,)
    reply = response.text
    print("\nAgent:", reply, "\n")
    memory.append("User: " + user_input)
    memory.append("Agent: " + reply)