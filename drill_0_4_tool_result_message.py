def make_message(tool_name: str, result: object) -> dict:
    if not tool_name:
        raise ValueError("tool_name is required")

    return {
        "role": "tool",
        "content": {
            "tool_name": tool_name,
            "result": result,
        },
    }


message = make_message("calculator", 13)

print(message["role"])
print(message["content"]["tool_name"])
print(message["content"]["result"])
