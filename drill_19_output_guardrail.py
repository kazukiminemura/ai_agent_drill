def output_guardrail(answer: dict) -> dict:
    content = answer.get("content", {})
    if "answer" not in content:
        return {"status": "guardrail", "content": {"passed": False, "reason": "answer required"}}
    if content["answer"] == "わかりません":
        return {"status": "guardrail", "content": {"passed": True, "reason": ""}}
    if not content.get("sources"):
        return {"status": "guardrail", "content": {"passed": False, "reason": "sources required"}}
    if content.get("grounded") is False:
        return {"status": "guardrail", "content": {"passed": False, "reason": "not grounded"}}
    return {"status": "guardrail", "content": {"passed": True, "reason": ""}}


answers = [
    {"status": "final", "content": {"answer": "返金は30日以内です。", "sources": ["refund.md"], "grounded": True}},
    {"status": "final", "content": {"answer": "根拠なしの断定です。", "sources": [], "grounded": False}},
    {"status": "final", "content": {"answer": "わかりません", "sources": []}},
]

for answer in answers:
    print(output_guardrail(answer))
