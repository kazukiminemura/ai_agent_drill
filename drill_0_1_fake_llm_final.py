class FakeLLM:
    def chat(self, message: str) -> dict:
        if message != "こんにちは":
            return {
                "type": "final",
                "content": "対応していません。",
            }

        return {
            "type": "final",
            "content": "こんにちは！",
        }


llm = FakeLLM()
response = llm.chat("こんにちは")

print(response)
print(response["type"])
print(response["content"])
print(llm.chat("こんばんは")["content"])
