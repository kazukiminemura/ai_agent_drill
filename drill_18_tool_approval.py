APPROVAL_REQUIRED = {"delete_file", "send_email"}
KNOWN_TOOLS = {"read_file", "delete_file", "send_email"}


def request_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name not in KNOWN_TOOLS:
        return {
            "status": "rejected",
            "content": {"reason": f"unknown tool: {tool_name}"},
        }

    if tool_name in APPROVAL_REQUIRED:
        return {
            "status": "pending_approval",
            "content": {"tool_name": tool_name, "arguments": arguments},
        }
    return {"status": "tool_result", "content": {"tool_name": tool_name, "result": f"{tool_name} done"}}


def approve(pending: dict, allowed: bool) -> dict:
    if not allowed:
        return {"status": "rejected", "content": {"reason": "not approved"}}
    tool_name = pending["content"]["tool_name"]
    return {"status": "tool_result", "content": {"tool_name": tool_name, "result": f"{tool_name} done"}}


pending = request_tool("delete_file", {"path": "old.txt"})
print(pending)
print(approve(pending, allowed=False))
