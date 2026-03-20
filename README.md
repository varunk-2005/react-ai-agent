# react-ai-agent
# ReAct AI Agent

A Python-based AI agent that connects an LLM to multiple tools to give optimal, efficient answers to any query.

## How It Works

When you run the agent, it:
1. Initializes a connection to Gemini (LLM) and creates a memory for the conversation
2. Takes your query as input
3. The LLM decides which tool to use based on the query
4. The tool is called and the result is sent back to the LLM
5. The LLM formats the result into a concise, presentable reply

This follows the **ReAct pattern** (Reason + Act) — the LLM reasons about what tool to call, acts by calling it, observes the result, and responds.

## Tools Available

| Tool | Description |
|------|-------------|
| Calculator | Evaluates math expressions |
| Web Search | Searches the web using DuckDuckGo |
| File Writer | Saves output to a file |

## Tech Stack

- **LLM:** Google Gemini (via `google-genai`)
- **Web Search:** DuckDuckGo (`ddgs`)
- **Environment Variables:** `python-dotenv`
- **Language:** Python 3.13

## Setup

1. Clone the repo
```bash
git clone https://github.com/varunk-2005/react-ai-agent.git
cd react-ai-agent
```

2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate
pip install google-genai ddgs python-dotenv
```

3. Create a `.env` file in the root directory
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the agent
```bash
python agent2.py
```

## Example Usage

```
You: what is 234 * 567?
Agent: 234 multiplied by 567 is 132,678.

You: search for the latest AI news and save it to news.txt
Agent: I have searched for the latest AI news and saved it to news.txt.
```

## Project Structure

```
react-ai-agent/
├── agent2.py       # Main agent code
├── .env            # API keys (not committed)
├── .gitignore
└── README.md
```
