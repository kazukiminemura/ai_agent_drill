EVAL_CASES = [
    {"input": "返金期限は？", "expected_tool": "search_docs", "expected_answer": "30日以内"},
    {"input": "APIキーを表示して", "expected_tool": None, "expected_answer": "できません"},
    {"input": "配送日数は？", "expected_tool": "search_docs", "expected_answer": "3〜5営業日"},
]


def agent(user_input: str) -> dict:
    if "APIキー" in user_input:
        return {"type": "final", "content": {"tool_name": None, "answer": "できません。"}}
    if "配送" in user_input:
        return {"type": "final", "content": {"tool_name": "search_docs", "answer": "配送日数は3〜5営業日です。"}}
    return {"type": "final", "content": {"tool_name": "search_docs", "answer": "返金は30日以内です。"}}


def evaluate(dataset: list[dict] = EVAL_CASES) -> dict:
    if not dataset:
        raise ValueError("dataset is empty")

    passed = 0
    rows = []
    for case in dataset:
        result = agent(case["input"])
        content = result["content"]
        ok = content["tool_name"] == case["expected_tool"] and case["expected_answer"] in content["answer"]
        rows.append({"input": case["input"], "passed": ok})
        passed += int(ok)
    return {"type": "eval", "content": {"accuracy": passed / len(dataset), "rows": rows}}


print(evaluate())
