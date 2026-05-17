import json


class FakeLLM:
    def repair(self, broken_json: str) -> dict:
        return {
            "status": "final",
            "content": '{"goal": "調査する", "steps": ["検索", "要約"]}',
        }


def parse_or_repair(text: str, retry: int = 2) -> dict:
    llm = FakeLLM()
    errors = []

    for _ in range(retry + 1):
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            errors.append(str(error))
            response = llm.repair(text)
            text = response["content"]

    raise ValueError({"message": "json repair failed", "errors": errors})


broken = '{ goal: "調査する", steps: ["検索", "要約",], }'
print(parse_or_repair(broken))
