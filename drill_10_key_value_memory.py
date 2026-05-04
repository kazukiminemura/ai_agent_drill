memory_store: dict[str, str] = {}


def save_memory(key: str, value: str) -> str:
    memory_store[key] = value
    return "saved"


def read_memory(key: str) -> str:
    return memory_store.get(key, "保存されていません。")


def run(user_input: str) -> str:
    if "Pythonが好き" in user_input:
        save_memory("favorite_language", "Python")
        return "覚えました。"
    if "好きな言語" in user_input:
        return read_memory("favorite_language")
    return "まだ対応していません。"


print(run("私はPythonが好きです"))
print(run("前に言った好きな言語は？"))
