state = {
    "goal": "返金ポリシーを短く説明する",
    "plan": ["検索する", "要約する"],
    "completed_steps": [],
    "observations": [],
    "final_answer": None,
}


def search_policy() -> str:
    return "返金は購入から30日以内に申請できます。"


def run(state: dict) -> dict:
    observation = search_policy()
    if not observation:
        state["error"] = "observation is empty"
        return {"status": "state", "content": state}

    state["completed_steps"].append("検索する")
    state["observations"].append(observation)

    state["completed_steps"].append("要約する")
    state["final_answer"] = "返金は購入から30日以内に申請できます。"
    return {"status": "state", "content": state}


print(run(state))
