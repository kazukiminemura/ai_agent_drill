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
            "content": {
                "tool_name": "search_faq",
                "arguments": {"query": user_input},
            },
        }


def ask_faq(user_input: str) -> str:
    response = FakeLLM().chat(user_input)
    call = response["content"]
    if call["tool_name"] != "search_faq":
        raise ValueError(f"unknown tool: {call['tool_name']}")
    return search_faq(**call["arguments"])


print(ask_faq("返金したい"))
print(ask_faq("配送にはどれくらいかかる？"))
print(ask_faq("パスワードを忘れた"))
print(ask_faq("営業時間は？"))
