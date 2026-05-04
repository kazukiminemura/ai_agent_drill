DOCS = {
    "refund.md": "返金は購入から30日以内に申請できます。",
    "shipping.md": "通常配送は3〜5営業日です。",
}


def answer_with_source(query: str) -> dict:
    for file, text in DOCS.items():
        if "返金" in query and "返金" in text:
            return {
                "answer": "返金は購入から30日以内に申請できます。",
                "sources": [{"file": file, "quote": "購入から30日以内"}],
            }
    return {"answer": "不明です。", "sources": []}


result = answer_with_source("返金期限は？")
assert result["sources"][0]["quote"] in DOCS[result["sources"][0]["file"]]
print(result)
