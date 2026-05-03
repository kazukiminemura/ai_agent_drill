tool_result_message = {
    "role": "tool",
    "content": {
        "tool_name": "calculator",
        "result": 13,
    },
}

print(tool_result_message["role"])
print(tool_result_message["content"]["tool_name"])
print(tool_result_message["content"]["result"])

