from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Message:
    role: str
    content: Any


@dataclass
class Tool:
    name: str
    func: Callable[..., Any]


@dataclass
class Agent:
    name: str
    tools: list[Tool]


@dataclass
class RunResult:
    final_answer: str
    messages: list[Message]


def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    raise ValueError(f"unsupported expression: {expression}")


class FakeLLM:
    def chat(self, messages: list[Message], agent: Agent) -> dict:
        has_tool_result = any(message.role == "tool" for message in messages)
        if has_tool_result:
            return {"type": "final", "content": "答えは13です。"}
        return {
            "type": "tool_call",
            "tool_name": "calculator",
            "arguments": {"expression": "3 + 5 * 2"},
        }


class Runner:
    def __init__(self, llm: FakeLLM):
        self.llm = llm

    def run(self, agent: Agent, user_input: str) -> RunResult:
        messages = [Message("user", user_input)]

        while True:
            response = self.llm.chat(messages, agent)

            if response["type"] == "final":
                messages.append(Message("assistant", response["content"]))
                return RunResult(response["content"], messages)

            if response["type"] == "tool_call":
                tool = find_tool(agent, response["tool_name"])
                result = tool.func(**response["arguments"])
                messages.append(Message("assistant", response))
                messages.append(Message("tool", {"tool_name": tool.name, "result": result}))
                continue

            raise ValueError(f"unsupported response: {response}")


def find_tool(agent: Agent, name: str) -> Tool:
    for tool in agent.tools:
        if tool.name == name:
            return tool
    raise ValueError(f"tool not found: {name}")


agent = Agent("MathAgent", [Tool("calculator", calculator)])
result = Runner(FakeLLM()).run(agent, "3 + 5 * 2 は？")

print(result.final_answer)
for message in result.messages:
    print(message)
