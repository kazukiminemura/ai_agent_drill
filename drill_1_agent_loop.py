from typing import Callable


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
    def __init__(self, llm: FakeLLM, tools: dict[str, Callable]):
        self.llm = llm
        self.tools = tools

    def run(self, user_input: str) -> dict:
        messages = [{"role": "user", "content": user_input}]

        while True:
            response = self.llm.chat(messages)

            if response["type"] == "final":
                messages.append({"role": "assistant", "content": response})
                return {
                    "type": "final",
                    "content": {
                        "answer": response["content"],
                        "messages": messages,
                    },
                }

            if response["type"] == "tool_call":
                messages.append({"role": "assistant", "content": response})
                call = response["content"]
                try:
                    tool = self.tools[call["tool_name"]]
                    result = tool(**call["arguments"])
                    content = {"tool_name": call["tool_name"], "result": result}
                except (KeyError, ValueError) as error:
                    content = {"tool_name": call["tool_name"], "error": str(error)}
                    messages.append({"role": "tool", "content": content})
                    answer = "ツール実行に失敗しました。"
                    messages.append({"role": "assistant", "content": {"type": "final", "content": answer}})
                    return {"type": "final", "content": {"answer": answer, "messages": messages}}

                messages.append({"role": "tool", "content": content})
                continue

            raise ValueError(f"unsupported response: {response}")


tools = {"calculator": calculator}
result = Runner(FakeLLM(), tools).run("3 + 5 * 2 は？")

print(result["content"]["answer"])
for message in result["content"]["messages"]:
    print(message)
