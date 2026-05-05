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


llm = FakeLLM()

response = llm.chat([])
print(response)

messages = [
    {
        "role": "tool",
        "content": {
            "tool_name": "calculator",
            "result": 13,
        },
    }
]

response = llm.chat(messages)
print(response)
