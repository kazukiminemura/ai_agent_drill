history: list[dict] = []


def chat(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    answer = f"echo: {user_input}"
    history.append({"role": "assistant", "content": answer})
    return answer


def handle_command(text: str) -> str:
    if text == "/exit":
        return "bye"
    if text == "/history":
        return str(history)
    if text == "/reset":
        history.clear()
        return "reset"
    return chat(text)


print(handle_command("こんにちは"))
print(handle_command("/history"))
