history: list[dict] = []


def chat(user_input: str) -> dict:
    history.append({"role": "user", "content": user_input})
    answer = f"echo: {user_input}"
    history.append({"role": "assistant", "content": answer})
    return {"type": "final", "content": {"answer": answer}}


def handle_command(text: str) -> dict:
    if text == "/exit":
        return {"type": "command", "content": {"answer": "bye"}}
    if text == "/history":
        return {"type": "command", "content": {"messages": history}}
    if text == "/reset":
        history.clear()
        return {"type": "command", "content": {"answer": "reset"}}
    if text.startswith("/"):
        return {"type": "command", "content": {"answer": "unknown command"}}
    return chat(text)


print(handle_command("こんにちは"))
print(handle_command("/history"))
