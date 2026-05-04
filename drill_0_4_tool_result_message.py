def make_tool_result_message(tool_name: str, result: object) -> dict:
    if not tool_name:
        raise ValueError("tool_name is required")

    return {
        "role": "tool",
        "content": {
            "tool_name": tool_name,
            "result": result,
        },
    }


tool_result_message = make_tool_result_message("calculator", 13)

print(tool_result_message["role"])
print(tool_result_message["content"]["tool_name"])
print(tool_result_message["content"]["result"])
