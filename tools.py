import json

# actual tool function

def calculate(expression: str):

    try:

        result = eval(expression)

        return str(result)

    except Exception as e:

        return f"Error: {str(e)}"


# tool schema (this is what LLM reads)

TOOLS = [

    {

        "type": "function",

        "function": {

            "name": "calculate",

            "description": "Perform mathematical calculations",

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {

                        "type": "string",

                        "description": "Math expression like 25*4 or (10+5)/3"

                    }

                },

                "required": ["expression"]

            }

        }

    }

]
 