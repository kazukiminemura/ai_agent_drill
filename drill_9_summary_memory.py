class SummaryMemory:
    def __init__(self, keep_recent: int = 4):
        if keep_recent < 1:
            raise ValueError("keep_recent must be at least 1")
        self.keep_recent = keep_recent
        self.summary = ""
        self.messages: list[dict] = []

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > 10 or (self.summary and len(self.messages) > self.keep_recent):
            old = self.messages[:-self.keep_recent]
            old_summary = " / ".join(message["content"] for message in old)
            self.summary = f"{self.summary} / {old_summary}" if self.summary else old_summary
            self.messages = self.messages[-self.keep_recent :]

    def prompt_messages(self) -> list[dict]:
        if not self.summary:
            return self.messages
        return [{"role": "system", "content": f"summary: {self.summary}"}] + self.messages


memory = SummaryMemory()
for i in range(12):
    memory.add("user", f"message {i}")

print(memory.prompt_messages())
