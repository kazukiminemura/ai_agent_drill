DOCS = {
    "refund.md": "返金期限は購入から30日以内です。",
    "shipping.md": "配送日数は3〜5営業日です。",
    "account.md": "アカウント削除は設定画面から申請できます。",
}

KEYWORDS = {
    "refund.md": ["返金", "期限"],
    "shipping.md": ["配送", "日数"],
    "account.md": ["アカウント", "削除"],
}


def score(query: str, file: str) -> int:
    return sum(1 for keyword in KEYWORDS[file] if keyword in query)


def search_docs(query: str, top_k: int = 1) -> list[tuple[str, str]]:
    ranked = sorted(
        DOCS.items(),
        key=lambda item: score(query, item[0]),
        reverse=True,
    )
    return [
        (file, text)
        for file, text in ranked[:top_k]
        if score(query, file) > 0
    ]


def answer(query: str) -> dict:
    results = search_docs(query)
    if not results:
        return {"status": "final", "content": {"answer": "見つかりませんでした。", "source": None}}
    file, text = results[0]
    return {"status": "final", "content": {"answer": text, "source": file}}


print(answer("返金期限は？"))
print(answer("価格は？"))
