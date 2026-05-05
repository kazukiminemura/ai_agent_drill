def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    raise ValueError(f"unsupported expression: {expression}")


def run_tool(call: dict, tools: dict) -> dict:
    tool_name = call["tool_name"]
    if tool_name not in tools:
        raise ValueError(f"unknown tool: {tool_name}")

    result = tools[tool_name](**call["arguments"])
    return {
        "role": "tool",
        "content": {
            "tool_name": tool_name,
            "result": result,
        },
    }


tools = {"calculator": calculator}
call = {
    "tool_name": "calculator",
    "arguments": {"expression": "3 + 5 * 2"},
}

message = run_tool(call, tools)

print(message["role"])
print(message["content"]["tool_name"])
print(message["content"]["result"])
