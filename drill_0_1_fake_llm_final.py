class FakeLLM:
    def chat(self, message: str) -> dict:
        if message != "こんにちは":
            return {
                "status": "final",
                "content": "対応していません。",
            }

        return {
            "status": "final",
            "content": "こんにちは！",
        }


llm = FakeLLM()
response = llm.chat("こんにちは")

print(response)
print(response["status"])
print(response["content"])
print(llm.chat("こんばんは")["content"])
