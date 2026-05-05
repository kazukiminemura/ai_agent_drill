DOCS = {
    "refund.md": "返金は購入から30日以内に申請できます。",
    "shipping.md": "通常配送は3〜5営業日です。",
}


def answer_with_source(query: str) -> dict:
    for file, text in DOCS.items():
        if "返金" in query and "返金" in text:
            response = {
                "type": "final",
                "content": {
                "answer": "返金は購入から30日以内に申請できます。",
                "sources": [{"file": file, "quote": "購入から30日以内"}],
                },
            }
            validate_sources(response)
            return response
    return {"type": "final", "content": {"answer": "不明です。", "sources": []}}


def validate_sources(response: dict) -> None:
    for source in response["content"].get("sources", []):
        if source["quote"] not in DOCS[source["file"]]:
            raise ValueError("quote not found in document")


result = answer_with_source("返金期限は？")
print(result)
print(answer_with_source("営業時間は？"))
