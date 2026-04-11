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
   # First LLM call
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
   # Check if tool is requested
   if msg.tool_calls:
       tool_call = msg.tool_calls[0]
       args = json.loads(tool_call.function.arguments)
       result = calculate(args["expression"])
       # Send tool result back to LLM
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
   return msg.content