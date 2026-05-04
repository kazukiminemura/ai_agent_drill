from dataclasses import dataclass


@dataclass
class TaskPlan:
    goal: str
    steps: list[str]
    tools_needed: list[str]
    risk_level: str

    def validate(self) -> None:
        if len(self.steps) < 3:
            raise ValueError("steps must have at least 3 items")
        if self.risk_level not in ["low", "medium", "high"]:
            raise ValueError("invalid risk_level")


class FakeLLM:
    def chat(self, user_input: str) -> dict:
        return {
            "goal": user_input,
            "steps": ["調査する", "構成を作る", "下書きを作る"],
            "tools_needed": ["search", "writer"],
            "risk_level": "medium",
        }


data = FakeLLM().chat("ブログ記事を調査して、構成を作って、下書きまで作ってください")
plan = TaskPlan(**data)
plan.validate()
print(plan)
