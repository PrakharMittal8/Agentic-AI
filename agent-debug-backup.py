import json
from models import client, MODEL
from tools import TOOLS, calculate

SYSTEM_PROMPT = (
 "You are a calculator assistant.\n"
 "You MUST use the calculate tool for ANY mathematical expression.\n"
 "DO NOT solve math yourself.\n"
 "If math is detected, always call the tool."
)

def run_agent(user_input):
 print("\n--- NEW QUERY ---")
 print("User Input:", user_input)

 # 🔹 First LLM call
 response = client.chat.completions.create(
 model=MODEL,
 messages=[
 {"role": "system", "content": SYSTEM_PROMPT},
 {"role": "user", "content": user_input}
 ],
 tools=TOOLS,
 tool_choice="auto"
 )

 msg = response.choices[0].message

 #  DEBUG 
 print("TOOL CALLS:", msg.tool_calls)

 #  If tool is called
 if msg.tool_calls:
    tool_call = msg.tool_calls[0]
 args = json.loads(tool_call.function.arguments)

 print("Tool Name:", tool_call.function.name)
 print("Tool Args:", args)

 result = calculate(args["expression"])

 print("Tool Result:", result)

 #  Second LLM call 
 final = client.chat.completions.create(
 model=MODEL,
 messages=[
 {"role": "system", "content": SYSTEM_PROMPT},
 {"role": "user", "content": user_input},
 msg,
 {
 "role": "tool",
 "tool_call_id": tool_call.id,
 "name": "calculate",
 "content": result
 }
 ],
 tools=TOOLS
 )

 return final.choices[0].message.content

 #  FALLBACK (force calculation if model skips tool)
 if any(char.isdigit() for char in user_input):
    print(" Model skipped tool → using fallback")
 return calculate(user_input)

 return msg.content

