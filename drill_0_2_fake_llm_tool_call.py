class FakeLLM:
    def chat(self, message: str) -> dict:
        if "3 + 5 * 2" in message:
            return {
                "status": "tool_call",
                "content": {
                    "tool_name": "calculator",
                    "arguments": {
                        "expression": "3 + 5 * 2",
                    },
                },
            }

        return {
            "status": "final",
            "content": "計算できません。",
        }

llm = FakeLLM()
response = llm.chat("what is 3 + 5 * 2?")

print(response["status"])
print(response["content"]["tool_name"])
print(response["content"]["arguments"]["expression"])
print(llm.chat("今日の天気は？")["content"])
