class ShortTermMemory:
    def __init__(self, limit: int = 4):
        self.limit = limit
        self.messages: list[dict] = []

    def add(self, role: str, content: str | dict) -> None:
        self.messages.append({"role": role, "content": content})

    def recent(self) -> list[dict]:
        return self.messages[-self.limit :]


memory = ShortTermMemory(limit=4)
memory.add("user", "1つめ")
memory.add("assistant", "返答1")
memory.add("tool", {"result": 13})
memory.add("user", "2つめ")
memory.add("assistant", "返答2")

print(memory.recent())
