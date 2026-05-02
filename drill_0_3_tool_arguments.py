def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13

    raise ValueError(f"unsupported expression: {expression}")


tool_call = {
    "tool_name": "calculator",
    "arguments": {
        "expression": "3 + 5 * 2",
    },
}

result = calculator(**tool_call["arguments"])

print(result)
