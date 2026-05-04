APPROVAL_REQUIRED = {"delete_file", "send_email"}
KNOWN_TOOLS = {"read_file", "delete_file", "send_email"}


def request_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name not in KNOWN_TOOLS:
        return {
            "status": "rejected",
            "reason": f"unknown tool: {tool_name}",
        }

    if tool_name in APPROVAL_REQUIRED:
        return {
            "status": "pending_approval",
            "tool_name": tool_name,
            "arguments": arguments,
        }
    return {"status": "executed", "result": f"{tool_name} done"}


def approve(pending: dict, allowed: bool) -> dict:
    if not allowed:
        return {"status": "rejected"}
    return {"status": "executed", "result": f"{pending['tool_name']} done"}


pending = request_tool("delete_file", {"path": "old.txt"})
print(pending)
print(approve(pending, allowed=False))
