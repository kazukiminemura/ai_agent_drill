from dataclasses import dataclass
from typing import Any, Callable


"""
Drill 2: max_turns を入れる

問題:
    Fake LLM が毎回 calculator tool_call を返し続ける。
    そのままだと Runner の while True が終わらない。

作るもの:
    1. LoopingFakeLLM
       - 毎回同じ tool_call を返す
    2. Runner(max_turns=3)
       - LLM に聞く回数を最大 3 回に制限する
    3. MaxTurnsExceededError
       - max_turns を超えたら "max_turns exceeded" を含む例外を出す
       - 例外からログを確認できるように messages を持たせる

合格条件:
    - max_turns=3 のとき、tool_call は 3 回まで
    - 4 回目の LLM 呼び出しには進まない
    - エラー内容に "max_turns exceeded" が含まれる
    - エラー時のログが残る
"""


@dataclass
class Message:
    role: str
    content: Any


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]


@dataclass
class Agent:
    name: str
    instructions: str
    tools: list[Tool]


@dataclass
class RunResult:
    final_answer: str
    messages: list[Message]


class MaxTurnsExceededError(RuntimeError):
    """max_turns で止まったとき、途中ログも一緒に渡すための例外。"""

    def __init__(self, messages: list[Message]):
        super().__init__("max_turns exceeded")
        self.messages = messages


def calculator(expression: str) -> int:
    if expression == "1 + 1":
        return 2

    raise ValueError(f"unsupported expression: {expression}")


class LoopingFakeLLM:
    def chat(self, messages: list[Message], agent: Agent) -> dict:
        # Drill 2 の問題設定:
        # tool result を見ても final を返さず、ずっと tool_call を返し続ける。
        return {
            "type": "tool_call",
            "tool_name": "calculator",
            "arguments": {
                "expression": "1 + 1",
            },
        }


class Runner:
    def __init__(self, llm: LoopingFakeLLM, max_turns: int = 3):
        self.llm = llm
        self.max_turns = max_turns

    def run(self, agent: Agent, user_input: str) -> RunResult:
        # Step 1: user message をログに入れる。
        messages: list[Message] = [
            Message(
                role="user",
                content=user_input,
            )
        ]

        # Step 2: while True ではなく、max_turns 回だけ LLM に聞く。
        # max_turns=3 なら、この loop は 3 回で必ず終わる。
        for turn in range(1, self.max_turns + 1):
            llm_response = self.llm.chat(messages, agent)

            if llm_response["type"] == "tool_call":
                # Step 3: assistant が tool_call したことをログに残す。
                messages.append(
                    Message(
                        role="assistant",
                        content={
                            **llm_response,
                            "turn": turn,
                        },
                    )
                )

                tool_name = llm_response["tool_name"]
                arguments = llm_response["arguments"]
                tool = self.find_tool(agent, tool_name)
                tool_result = tool.func(**arguments)

                # Step 4: tool の実行結果をログに残す。
                messages.append(
                    Message(
                        role="tool",
                        content={
                            "tool_name": tool_name,
                            "result": tool_result,
                        },
                    )
                )
                continue

            if llm_response["type"] == "final":
                # 今回の LoopingFakeLLM ではここには来ない。
                # ただし Runner としては final も処理できる形にしておく。
                final_answer = llm_response["content"]
                messages.append(
                    Message(
                        role="assistant",
                        content=final_answer,
                    )
                )
                return RunResult(final_answer=final_answer, messages=messages)

            raise ValueError(f"unsupported response: {llm_response}")

        # Step 5: max_turns 回やっても final にならなければ、ここで止める。
        # ここで止めるので、4 回目の LLM 呼び出しには進まない。
        messages.append(
            Message(
                role="error",
                content="max_turns exceeded",
            )
        )
        raise MaxTurnsExceededError(messages)

    def find_tool(self, agent: Agent, tool_name: str) -> Tool:
        for tool in agent.tools:
            if tool.name == tool_name:
                return tool
        raise ValueError(f"tool not found: {tool_name}")


calculator_tool = Tool(
    name="calculator",
    description="A tool for calculating mathematical expressions.",
    func=calculator,
)

agent = Agent(
    name="LoopAgent",
    instructions="You are a helpful assistant that can use tools.",
    tools=[calculator_tool],
)

runner = Runner(
    llm=LoopingFakeLLM(),
    max_turns=3,
)


def count_tool_calls(messages: list[Message]) -> int:
    return sum(
        1
        for message in messages
        if message.role == "assistant"
        and isinstance(message.content, dict)
        and message.content.get("type") == "tool_call"
    )


try:
    result = runner.run(agent, "何度も計算して")
    print("=== Final Answer ===")
    print(result.final_answer)
except MaxTurnsExceededError as error:
    print("=== Error ===")
    print(error)

    print("\n=== Log ===")
    for i, message in enumerate(error.messages, start=1):
        print(f"{i}. role={message.role}")
        print(f"   content={message.content}")

    print("\n=== Check ===")
    print(f"tool_call count: {count_tool_calls(error.messages)}")
    print(f"max_turns: {runner.max_turns}")
    print(f"passed: {'max_turns exceeded' in str(error)}")
