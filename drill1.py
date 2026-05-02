from dataclasses import dataclass
from typing import Any, Callable

# single message
@dataclass
class Message:
    role: str
    content: Any

# definte tools
@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]

# definte agent
@dataclass
class Agent:
    name: str
    instructions: str
    tools: list[Tool]

# run results
@dataclass
class RunResult:
    final_answer: str
    messages: list[Message]

# calculator tool
def calculator(expression: str) -> int:
    if expression == "3 + 5 * 2":
        return 13
    
    raise ValueError(f"unsupporrted expression: {expression}")

# Fake LLM
class FakeLLM:
    def chat(self, messages: list[Message], agent: Agent) -> dict:
        has_tool_result = any(message.role == "tool" for message in messages)

        if not has_tool_result:
            return {
                "type": "tool_call",
                "tool_name": "calculator",
                "arguments": {
                    "expression": "3 + 5 * 2"
                }
            }
        # if tool result is present, return final answer
        return {
            "type": "final",
            "content": "The answer is 13."
        }
    
# Runner
class Runner:
    def __init__(self, llm: FakeLLM):
        self.llm = llm

    def run(self, agent: Agent, user_input: str) -> RunResult:
        messages: list[Message] = []

        # user message
        messages.append(
            Message(
                role="user",
                content=user_input
            )
        )

        while True:
            llm_response = self.llm.chat(messages, agent)

            if llm_response["type"] == "tool_call":
                messages.append(
                    Message(
                        role="assistant",
                        content="responnse"
                    )
                )

                tool_name =  llm_response["tool_name"]
                arguments = llm_response["arguments"]

                tool = self.find_tool(agent, tool_name)
                tool_result = tool.func(**arguments)

                # tool result
                messages.append(
                    Message(
                        role="tool",
                        content={
                            "tool_name": tool_name,
                            "result": tool_result
                        }
                    )
                )
                continue

            # assistant final
            if llm_response["type"] == "final":
                final_answer = llm_response["content"]

                messages.append(
                    Message(
                        role="assistant",
                        content=final_answer
                    )
                )

                return RunResult(
                    final_answer=final_answer,
                    messages=messages
                )
            
            raise ValueError(f"unsupported response: {llm_response}")
        
    def find_tool(self, agent: Agent, tool_name: str) -> Tool:
        for tool in agent.tools:
            if tool.name == tool_name:
                return tool
        raise ValueError(f"tool not found: {tool_name}")

# Create Tool
calculator_tool = Tool(
    name="calculator",
    description="A too for calculating mathematical expressions.",
    func = calculator
)

# Create agent
agent = Agent(
    name="MathAgent",
    instructions="you are a helpful assistant that can perform calculations using the caluculator",
    tools=[calculator_tool]
)

# Create runner
runner = Runner(
    llm=FakeLLM()
)

# Run
result = runner.run(agent, "3 + 5 * 2?")

# show results
print("=== Final Answer ===")
print(result.final_answer)

print("\n=== Log ===")
for i, message in enumerate(result.messages, start=1):
    print(f"{i}.role={message.role}")
    print(f"  content={message.content}")
