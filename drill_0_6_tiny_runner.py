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
                "tool_name": "calculator",
                "arguments": {
                    "expression": "3 + 5 * 2",
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

    first_response = llm.chat(messages)

    if first_response["type"] == "tool_call":
        if first_response["tool_name"] != "calculator":
            raise ValueError(f"Unknown tool: {first_response['tool_name']}")

        try:
            tool_result = calculator(**first_response["arguments"])
            content = {
                "tool_name": first_response["tool_name"],
                "result": tool_result,
            }
        except ValueError as error:
            content = {
                "tool_name": first_response["tool_name"],
                "error": str(error),
            }

        messages.append({
            "role": "tool",
            "content": content,
        })
    elif first_response["type"] == "final":
        return first_response["content"]
    else:
        raise ValueError(f"Unsupported response: {first_response}")

    second_response = llm.chat(messages)

    if second_response["type"] == "final":
        return second_response["content"]
    
    raise ValueError(f"Unsupported response: {second_response}")

answer = run("What is 3 + 5 * 2?")
print(answer)
