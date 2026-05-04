class FakeLLM:
    def chat(self, message: str) -> dict:
        if "3 + 5 * 2" in message:
            return {
                "type": "tool_call",
                "tool_name": "calculator",
                "arguments": {
                    "expression": "3 + 5 * 2",
                },
            }

        return {
            "type": "final",
            "content": "計算できません。",
        }

llm = FakeLLM()
response = llm.chat("what is 3 + 5 * 2?")

print(response["type"])
print(response["tool_name"])
print(response["arguments"]["expression"])
print(llm.chat("今日の天気は？")["content"])
