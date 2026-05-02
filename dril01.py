class FakeLLM:
    def chat(self, messages: str) -> dict:
        return {
            "type": "final",
            "content": "Hello",
        }
    
llm = FakeLLM()
response = llm.chat("Hello")

print(response)
print(response["content"])