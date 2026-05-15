def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    raise ValueError(f"Unsupported expression: {expression}")


class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        tool_message_content = next(
            (message["content"] for message in messages if message["role"] == "tool"),
            None,
        )
        if tool_message_content is None:
            return {
                "type": "tool_call",
                "content": {
                    "tool_name": "calculator",
                    "arguments": {"expression": "3 + 5 * 2"},
                },
            }

        if "error" in tool_message_content:
            return {"type": "final", "content": "計算できませんでした。"}

        return {"type": "final", "content": f"答えは{tool_message_content['result']}です。"}


def run(user_input: str) -> str:
    llm = FakeLLM()
    messages = [{"role": "user", "content": user_input}]
    response = llm.chat(messages)

    if response["type"] == "final":
        return response["content"]
    if response["type"] != "tool_call":
        raise ValueError(f"Unsupported response: {response}")

    tool_call = response["content"]
    if tool_call["tool_name"] != "calculator":
        raise ValueError(f"Unknown tool: {tool_call['tool_name']}")

    tool_message_content = {"tool_name": tool_call["tool_name"]}
    try:
        tool_message_content["result"] = calculator(**tool_call["arguments"])
    except ValueError as error:
        tool_message_content["error"] = str(error)

    messages.append({"role": "tool", "content": tool_message_content})
    response = llm.chat(messages)

    if response["type"] != "final":
        raise ValueError(f"Unsupported response: {response}")
    return response["content"]


answer = run("What is 3 + 5 * 2?")
print(answer)
