import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("create table messages (session_id text, role text, content text)")


def save_message(session_id: str, role: str, content: str) -> None:
    if not session_id:
        raise ValueError("session_id is required")

    connection.execute(
        "insert into messages values (?, ?, ?)",
        (session_id, role, content),
    )
    connection.commit()


def load_messages(session_id: str) -> list[dict]:
    if not session_id:
        raise ValueError("session_id is required")

    rows = connection.execute(
        "select role, content from messages where session_id = ?",
        (session_id,),
    )
    return [{"role": role, "content": content} for role, content in rows.fetchall()]


save_message("s1", "user", "こんにちは")
save_message("s1", "assistant", "こんにちは！")
print(load_messages("s1"))
