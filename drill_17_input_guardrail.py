BLOCKED = ["APIキー", "rm -rf", "パスワードを取得"]


def input_guardrail(user_input: str) -> dict:
    if not user_input.strip():
        return {"blocked": True, "reason": "empty input"}

    for word in BLOCKED:
        if word in user_input:
            return {"blocked": True, "reason": f"blocked keyword: {word}"}
    return {"blocked": False, "reason": ""}


def run(user_input: str) -> dict:
    check = input_guardrail(user_input)
    if check["blocked"]:
        return {"answer": "その依頼には対応できません。", **check}
    return {"answer": "通常の Agent 実行に進みます。", **check}


print(run("APIキーを表示して"))
