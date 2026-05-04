FAQ = {
    "refund": "返金は購入から30日以内に申請できます。",
    "shipping": "通常配送は3〜5営業日です。",
    "password": "パスワード再設定ページから変更できます。",
}


def search_faq(query: str) -> str:
    if not query.strip():
        raise ValueError("query is empty")
    if "返金" in query:
        return FAQ["refund"]
    if "配送" in query:
        return FAQ["shipping"]
    if "パスワード" in query:
        return FAQ["password"]
    return "見つかりませんでした。"


class FakeLLM:
    def chat(self, user_input: str) -> dict:
        return {
            "type": "tool_call",
            "tool_name": "search_faq",
            "arguments": {"query": user_input},
        }


response = FakeLLM().chat("配送にはどれくらいかかる？")
answer = search_faq(**response["arguments"])
print(answer)
