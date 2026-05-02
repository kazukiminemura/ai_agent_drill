class FakeLLM:
    def chat(self, messages: str) -> dict:
        if "3 + 5 * 2" in messages:
            return {
                "type": "tool_call",
                "tool_name": "calculator",
                "arguments": {
                    "expression": "3 + 5 * 2",
                },
            }

        return {
            "type" : "final",
            "content": "not found the answer",
        }

llm = FakeLLM()
response = llm.chat("what is 3 + 5 * 2?")

print(response["type"])
print(response["tool_name"])
print(response["arguments"]["expression"])
