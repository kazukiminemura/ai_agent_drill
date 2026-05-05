def output_guardrail(answer: dict) -> dict:
    content = answer.get("content", {})
    if "answer" not in content:
        return {"type": "guardrail", "content": {"passed": False, "reason": "answer required"}}
    if content["answer"] == "わかりません":
        return {"type": "guardrail", "content": {"passed": True, "reason": ""}}
    if not content.get("sources"):
        return {"type": "guardrail", "content": {"passed": False, "reason": "sources required"}}
    if content.get("grounded") is False:
        return {"type": "guardrail", "content": {"passed": False, "reason": "not grounded"}}
    return {"type": "guardrail", "content": {"passed": True, "reason": ""}}


answers = [
    {"type": "final", "content": {"answer": "返金は30日以内です。", "sources": ["refund.md"], "grounded": True}},
    {"type": "final", "content": {"answer": "根拠なしの断定です。", "sources": [], "grounded": False}},
    {"type": "final", "content": {"answer": "わかりません", "sources": []}},
]

for answer in answers:
    print(output_guardrail(answer))
