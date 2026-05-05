def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13

    raise ValueError(f"Unsupported expression: {expression}")

class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        tool_results = [message for message in messages if message.get("role") == "tool"]

        if not tool_results:
            return {
                "type": "tool_call",
                "content": {
                    "tool_name": "calculator",
                    "arguments": {
                        "expression": "3 + 5 * 2",
                    },
                },
            }

        if "error" in tool_results[-1]["content"]:
            return {
                "type": "final",
                "content": "計算できませんでした。",
            }

        return {
            "type": "final",
            "content": "答えは13です。",
        }
        
def run(user_input: str) -> str:
    llm = FakeLLM()
    messages = [
        {
            "role": "user",
            "content": user_input,
        }
    ]

    response = llm.chat(messages)

    if response["type"] == "tool_call":
        call = response["content"]
        if call["tool_name"] != "calculator":
            raise ValueError(f"Unknown tool: {call['tool_name']}")

        try:
            result = calculator(**call["arguments"])
            content = {
                "tool_name": call["tool_name"],
                "result": result,
            }
        except ValueError as error:
            content = {
                "tool_name": call["tool_name"],
                "error": str(error),
            }

        messages.append({
            "role": "tool",
            "content": content,
        })
    elif response["type"] == "final":
        return response["content"]
    else:
        raise ValueError(f"Unsupported response: {response}")

    response = llm.chat(messages)

    if response["type"] == "final":
        return response["content"]
    
    raise ValueError(f"Unsupported response: {response}")

answer = run("What is 3 + 5 * 2?")
print(answer)
