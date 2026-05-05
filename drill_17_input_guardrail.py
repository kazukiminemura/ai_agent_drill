BLOCKED = ["APIキー", "rm -rf", "パスワードを取得"]


def input_guardrail(user_input: str) -> dict:
    if not user_input.strip():
        return {"type": "guardrail", "content": {"blocked": True, "reason": "empty input"}}

    for word in BLOCKED:
        if word in user_input:
            return {"type": "guardrail", "content": {"blocked": True, "reason": f"blocked keyword: {word}"}}
    return {"type": "guardrail", "content": {"blocked": False, "reason": ""}}


def run(user_input: str) -> dict:
    check = input_guardrail(user_input)
    if check["content"]["blocked"]:
        return {"type": "final", "content": {"answer": "その依頼には対応できません。", **check["content"]}}
    return {"type": "final", "content": {"answer": "通常の Agent 実行に進みます。", **check["content"]}}


print(run("APIキーを表示して"))
