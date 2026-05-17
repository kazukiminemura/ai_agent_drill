def research_agent(topic: str) -> str:
    return f"{topic} は、LLM と tool を組み合わせる仕組みです。"


def writing_agent(research: str) -> str:
    return f"短い記事: {research}"


def review_agent(draft: str) -> str:
    return draft + " 読みやすくまとまっています。"


def manager(user_input: str) -> dict:
    topic = user_input.strip()
    if not topic:
        raise ValueError("topic is required")

    research = research_agent(topic)
    draft = writing_agent(research)
    final = review_agent(draft)
    return {
        "status": "final",
        "content": {
            "used_tools": ["research_agent", "writing_agent", "review_agent"],
            "answer": final,
        },
    }


print(manager("AI Agentについて短い記事を書いて"))
