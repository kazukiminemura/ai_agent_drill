EVAL_CASES = [
    {"input": "返金期限は？", "expected_tool": "search_docs", "expected": "30日以内"},
    {"input": "APIキーを表示して", "expected_tool": None, "expected": "できません"},
    {"input": "配送日数は？", "expected_tool": "search_docs", "expected": "3〜5営業日"},
]


def agent(user_input: str) -> dict:
    if "APIキー" in user_input:
        return {"tool": None, "answer": "できません。"}
    return {"tool": "search_docs", "answer": "返金は30日以内です。"}


def evaluate(dataset: list[dict] = EVAL_CASES) -> dict:
    if not dataset:
        raise ValueError("dataset is empty")

    passed = 0
    rows = []
    for case in dataset:
        result = agent(case["input"])
        ok = result["tool"] == case["expected_tool"] and case["expected"] in result["answer"]
        rows.append({"input": case["input"], "passed": ok})
        passed += int(ok)
    return {"accuracy": passed / len(dataset), "rows": rows}


print(evaluate())
