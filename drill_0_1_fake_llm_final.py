class FakeLLM:
    def chat(self, message: str) -> dict:
        return {
            "type": "final",
            "content": "こんにちは！",
        }


llm = FakeLLM()
response = llm.chat("こんにちは")

print(response)
print(response["type"])
print(response["content"])
