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


llm = FakeLLM()

first_response = llm.chat([])
print(first_response)

messages = [
    {
        "role": "tool",
        "content": {
            "tool_name": "calculator",
            "result": 13,
        },
    }
]

second_response = llm.chat(messages)
print(second_response)
