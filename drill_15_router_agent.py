def route(user_input: str) -> dict:
    if "請求" in user_input:
        return {"target_agent": "billing", "reason": "請求の問い合わせ"}
    if "ログイン" in user_input:
        return {"target_agent": "tech_support", "reason": "技術サポート"}
    return {"target_agent": "general_faq", "reason": "一般的な質問"}


def handoff(user_input: str) -> dict:
    decision = route(user_input)
    return {
        "answer": f"{decision['target_agent']} に引き継ぎます。",
        "handoff_log": decision,
    }


print(handoff("請求書を再発行したい"))
