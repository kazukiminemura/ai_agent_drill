# Message Contract

このドキュメントは、AI Agent Drill で使う dict の定義です。

教材内の dict は、次の2種類を厳密に分けます。

1. LLM response: `FakeLLM.chat()` の返り値
2. message: `messages` に保存する会話履歴

## LLM response

LLM response は、FakeLLM が「次に何をするべきか」を返す dict です。

必ず `type` と `content` を持ちます。

```python
{"type": "final", "content": "答えです。"}
{"type": "tool_call", "content": {"tool_name": "calculator", "arguments": {"expression": "1 + 1"}}}
```

`type` は LLM response 専用のキーです。message dict には入れません。

使える `type`:

- `final`: LLM が最終回答を返した
- `tool_call`: LLM が tool 実行を依頼した

## tool call

tool call は、LLM response の `content` に入ります。

```python
response = {
    "type": "tool_call",
    "content": {
        "tool_name": "calculator",
        "arguments": {"expression": "1 + 1"},
    },
}
```

tool を実行するときは、`response["content"]` を `call` として取り出します。

```python
call = response["content"]
result = calculator(**call["arguments"])
```

tool call は、実行依頼です。tool 実行結果ではありません。

## message

message は、`messages` に保存する会話履歴です。

必ず `role` と `content` を持ちます。

```python
{"role": "user", "content": "1 + 1 は？"}
{"role": "assistant", "content": "答えは2です。"}
{"role": "tool", "content": {"tool_name": "calculator", "result": 2}}
{"role": "tool", "content": {"tool_name": "calculator", "error": "失敗理由"}}
```

`role` は message 専用のキーです。LLM response dict には入れません。

使える `role`:

- `user`: ユーザー入力
- `assistant`: Assistant の回答
- `tool`: tool の実行結果
- `system`: system message

## tool result message

tool result は、`role="tool"` の message として `messages` に保存します。

成功した場合:

```python
{"role": "tool", "content": {"tool_name": "calculator", "result": 2}}
```

失敗した場合:

```python
{"role": "tool", "content": {"tool_name": "calculator", "error": "unsupported expression"}}
```

tool が失敗しても、例外をそのまま外に出さず、まず tool message に `error` を残します。

## OK / NG

OK:

```python
response = {"type": "final", "content": "答えです。"}
messages.append({"role": "assistant", "content": response["content"]})
```

OK:

```python
response = {"type": "tool_call", "content": {"tool_name": "calculator", "arguments": {"expression": "1 + 1"}}}
call = response["content"]
result = calculator(**call["arguments"])
messages.append({"role": "tool", "content": {"tool_name": call["tool_name"], "result": result}})
```

NG:

```python
{"role": "assistant", "type": "final", "content": "答えです。"}
```

message dict に `type` が入っています。`type` は LLM response 専用です。

NG:

```python
{"role": "assistant", "content": {"type": "final", "content": "答えです。"}}
```

message の `content` に LLM response 全体を入れています。この形にすると、`content["content"]` という分かりにくい参照が必要になります。

## 判断ルール

迷ったら、次の質問で判断します。

- `FakeLLM.chat()` から返ってきたものか？
  - はい: LLM response。`type` を使う。
- `messages` に保存するものか？
  - はい: message。`role` を使う。
- Python 関数に渡す tool 実行依頼か？
  - はい: `response["content"]` から取り出した `call` を使う。
- tool の実行結果か？
  - はい: `role="tool"` の message に `result` または `error` を入れる。
