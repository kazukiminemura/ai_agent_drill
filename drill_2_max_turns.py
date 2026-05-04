"""
Drill 2: max_turns を入れる

お題:
FakeLLM は毎回 calculator tool_call を返します。
run に max_turns を入れて、終わらない処理を止めてください。

合格条件:
- max_turns=3 なら tool_call は 3 回まで
- エラー文に "max_turns exceeded" が含まれる
- エラー時の messages を確認できる
"""


class MaxTurnsExceededError(ValueError):
    def __init__(self, messages: list[dict]):
        super().__init__("max_turns exceeded")
        self.messages = messages


class FakeLLM:
    def chat(self, messages: list[dict]) -> dict:
        return {
            "type": "tool_call",
            "tool_name": "calculator",
            "arguments": {"expression": "1 + 1"},
        }


def calculator(expression: str) -> int:
    if expression == "1 + 1":
        return 2
    raise ValueError(f"unsupported expression: {expression}")


def run(user_input: str, max_turns: int = 3) -> list[dict]:
    if max_turns < 1:
        raise ValueError("max_turns must be at least 1")

    llm = FakeLLM()
    messages = [{"role": "user", "content": user_input}]

    for _ in range(max_turns):
        response = llm.chat(messages)
        result = calculator(**response["arguments"])
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "tool", "content": result})

    messages.append({"role": "error", "content": "max_turns exceeded"})
    raise MaxTurnsExceededError(messages)


try:
    run("何度も計算して", max_turns=3)
except MaxTurnsExceededError as error:
    print(error)
    print(error.messages)
