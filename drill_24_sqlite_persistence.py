import sqlite3


connection = sqlite3.connect(":memory:")
connection.execute("create table messages (session_id text, role text, content text)")


def save_message(session_id: str, role: str, content: str) -> None:
    connection.execute(
        "insert into messages values (?, ?, ?)",
        (session_id, role, content),
    )
    connection.commit()


def load_messages(session_id: str) -> list[tuple[str, str]]:
    rows = connection.execute(
        "select role, content from messages where session_id = ?",
        (session_id,),
    )
    return rows.fetchall()


save_message("s1", "user", "こんにちは")
save_message("s1", "assistant", "こんにちは！")
print(load_messages("s1"))
