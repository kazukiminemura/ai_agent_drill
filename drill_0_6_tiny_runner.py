def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    raise ValueError(f"Unsupported expression: {expression}")


class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        result = next((message["content"] for message in messages if message["role"] == "tool"), None)
        if result is None:
            return {
                "type": "tool_call",
                "content": {
                    "tool_name": "calculator",
                    "arguments": {"expression": "3 + 5 * 2"},
                },
            }

        if "error" in result:
            return {"type": "final", "content": "計算できませんでした。"}

        return {"type": "final", "content": f"答えは{result['result']}です。"}


def run(user_input: str) -> str:
    llm = FakeLLM()
    messages = [{"role": "user", "content": user_input}]
    response = llm.chat(messages)

    if response["type"] == "final":
        return response["content"]
    if response["type"] != "tool_call":
        raise ValueError(f"Unsupported response: {response}")

    call = response["content"]
    if call["tool_name"] != "calculator":
        raise ValueError(f"Unknown tool: {call['tool_name']}")

    content = {"tool_name": call["tool_name"]}
    try:
        content["result"] = calculator(**call["arguments"])
    except ValueError as error:
        content["error"] = str(error)

    messages.append({"role": "tool", "content": content})
    response = llm.chat(messages)

    if response["type"] != "final":
        raise ValueError(f"Unsupported response: {response}")
    return response["content"]


answer = run("What is 3 + 5 * 2?")
print(answer)
