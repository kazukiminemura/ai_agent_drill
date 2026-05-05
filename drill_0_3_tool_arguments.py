def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    

    raise ValueError(f"Unsupported expression: {expression}")

call = {
    "type": "tool_call",
    "content": {
        "tool_name": "calculator",
        "arguments": {
            "expression": "3 + 5 * 2",
        },
    },
}

result = calculator(**call["content"]["arguments"])
print(result)
