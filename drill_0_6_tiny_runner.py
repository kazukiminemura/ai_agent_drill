def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13

    raise ValueError(f"unsupported expression: {expression}")


class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        has_tool_result = any(message.get("role") == "tool" for message in messages)

        if not has_tool_result:
            return {
                "type": "tool_call",
                "tool_name": "calculator",
                "arguments": {
                    "expression": "3 + 5 * 2",
                },
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
        tool_result = calculator(**first_response["arguments"])

        messages.append({
            "role": "tool",
            "content": {
                "tool_name": first_response["tool_name"],
                "result": tool_result,
            },
        })

    second_response = llm.chat(messages)

    if second_response["type"] == "final":
        return second_response["content"]

    raise ValueError(f"unsupported response: {second_response}")


answer = run("3 + 5 * 2 は？")
print(answer)
