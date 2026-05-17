def route(user_input: str) -> dict:
    if not user_input.strip():
        return {"status": "route", "content": {"target": "general_faq", "reason": "empty input"}}
    if "請求" in user_input:
        return {"status": "route", "content": {"target": "billing", "reason": "請求の問い合わせ"}}
    if "ログイン" in user_input:
        return {"status": "route", "content": {"target": "tech_support", "reason": "技術サポート"}}
    return {"status": "route", "content": {"target": "general_faq", "reason": "一般的な質問"}}


def handoff(user_input: str) -> dict:
    decision = route(user_input)
    return {
        "status": "final",
        "content": {
            "answer": f"{decision['content']['target']} に引き継ぎます。",
            "log": decision,
        },
    }


print(handoff("請求書を再発行したい"))
