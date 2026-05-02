class FakeLLM:
    def chat(self, messages: str) -> dict:
        if messages == "Hello":
            return {
                "type": "final",
                "content": "Hello",
            }
        return {
            "type": "final",
            "content": "not found the answer",
        }
    
llm = FakeLLM()
response = llm.chat("Hello")

print(response)
print(response["type"])
print(response["content"])