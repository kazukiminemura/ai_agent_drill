def output_guardrail(answer: dict) -> dict:
    if answer["answer"] == "わかりません":
        return {"passed": True}
    if not answer.get("sources"):
        return {"passed": False, "reason": "sources required"}
    if answer.get("grounded") is False:
        return {"passed": False, "reason": "not grounded"}
    return {"passed": True}


answers = [
    {"answer": "返金は30日以内です。", "sources": ["refund.md"], "grounded": True},
    {"answer": "根拠なしの断定です。", "sources": [], "grounded": False},
    {"answer": "わかりません", "sources": []},
]

for answer in answers:
    print(output_guardrail(answer))
