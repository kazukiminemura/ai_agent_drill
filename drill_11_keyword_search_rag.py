DOCS = {
    "refund.md": "返金期限は購入から30日以内です。",
    "shipping.md": "配送日数は3〜5営業日です。",
    "account.md": "アカウント削除は設定画面から申請できます。",
}


def score(query: str, text: str) -> int:
    return sum(1 for char in query if char in text)


def search_docs(query: str, top_k: int = 1) -> list[tuple[str, str]]:
    ranked = sorted(
        DOCS.items(),
        key=lambda item: score(query, item[1]),
        reverse=True,
    )
    return ranked[:top_k]


def answer(query: str) -> str:
    file, text = search_docs(query)[0]
    return f"{text} source={file}"


print(answer("返金期限は？"))
