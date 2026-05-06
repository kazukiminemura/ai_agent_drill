def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    raise ValueError(f"unsupported expression: {expression}")


class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        has_result = any(message["role"] == "tool" for message in messages)
        if has_result:
            return {"type": "final", "content": "答えは13です。"}
        return {
            "type": "tool_call",
            "content": {
                "tool_name": "calculator",
                "arguments": {"expression": "3 + 5 * 2"},
            },
        }


class Runner:
    def __init__(self, llm: FakeLLM, tools: dict):
        self.llm = llm
        self.tools = tools

    def run(self, user_input: str) -> dict:
        messages = [{"role": "user", "content": user_input}]

        response = self.llm.chat(messages)
        if response["type"] == "final":
            return {"type": "final", "content": {"answer": response["content"], "messages": messages}}
        if response["type"] != "tool_call":
            raise ValueError(f"unsupported response: {response}")

        call = response["content"]
        if call["tool_name"] not in self.tools:
            raise ValueError(f"unknown tool: {call['tool_name']}")

        result = self.tools[call["tool_name"]](**call["arguments"])
        messages.append({"role": "assistant", "content": call})
        messages.append({
            "role": "tool",
            "content": {
                "tool_name": call["tool_name"],
                "result": result,
            },
        })

        response = self.llm.chat(messages)
        return {"type": "final", "content": {"answer": response["content"], "messages": messages}}


tools = {"calculator": calculator}
result = Runner(FakeLLM(), tools).run("3 + 5 * 2 は？")

print(result["content"]["answer"])
print(result["content"]["messages"])
