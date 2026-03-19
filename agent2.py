import os
from dotenv import load_dotenv
from google import genai
from ddgs import DDGS
tools = [
    {
        "name": "calculate",
        "description": "Evaluates a math expression and returns the result",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate e.g. 2+2"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "search",
        "description": "Searches the web for current information on a given query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up"
                }
            },
            "required": ["query"]
        }
    }
]
load_dotenv()
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: invalid expression"
def search(query):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
    output = ""
    for r in results:
        output += f"Title: {r['title']}\nSummary: {r['body']}\nURL: {r['href']}\n\n"
    return output
def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)
    return f"File '{filename}' written successfully"
class Agent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.memory = []
        self.system_prompt = "You are a helpful assistant. Be concise and clear."
        print("Agent created!")

    def reset(self):
        self.memory = []
        print("Memory cleared!")
    def run(self, user_input):
        self.memory.append({"role": "user", "parts": [{"text": user_input}]})
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.memory,
            config={"system_instruction": self.system_prompt,
                    "tools": [{"function_declarations": tools}]
                    }
        )
        part = response.candidates[0].content.parts[0]
        if part.function_call:
            tool_name = part.function_call.name
            tool_args = dict(part.function_call.args)
            if tool_name == "calculate":
                tool_result = calculate(**tool_args)
            elif tool_name == "search":
                tool_result = search(**tool_args)
        else:
            reply = part.text
            self.memory.append({"role": "model", "parts": [{"text": reply}]})
            return reply
        self.memory.append({"role": "model", "parts": [{"function_call": {"name": tool_name, "args": tool_args}}]})
        self.memory.append({"role": "user", "parts": [{"function_response": {"name": tool_name, "response": {"result": tool_result}}}]})
        response2 = self.client.models.generate_content(
            model=self.model,
            contents=self.memory,
            config={"system_instruction": self.system_prompt}
        )
        reply = response2.candidates[0].content.parts[0].text
        self.memory.append({"role": "model", "parts": [{"text": reply}]})
        return reply

agent = Agent()
while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == "exit":
        break
    reply = agent.run(user_input)
    print(f"\nAgent: {reply}\n")