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

        llm_response = self.llm.chat(messages)
        if llm_response["type"] == "final":
            return {
                "type": "final",
                "content": {"answer": llm_response["content"], "messages": messages},
            }
        if llm_response["type"] != "tool_call":
            raise ValueError(f"unsupported response: {llm_response}")

        call = llm_response["content"]
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

        llm_response = self.llm.chat(messages)
        return {
            "type": "final",
            "content": {"answer": llm_response["content"], "messages": messages},
        }


tools = {"calculator": calculator}
run_result = Runner(FakeLLM(), tools).run("3 + 5 * 2 は？")

print(run_result["content"]["answer"])
print(run_result["content"]["messages"])
