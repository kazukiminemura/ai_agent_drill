# AI Agent Drill

Python は書けるけれど、AI Agent はまだよく分からない人のための実装ドリルです。

この教材では、本物の LLM API は使わず、まず FakeLLM と小さい Python 関数だけで Agent の制御フローを練習します。

## 進め方

1. README のお題を読む
2. 30行前後で自分の回答を書く
3. 対応する回答例ファイルを見る
4. `python ファイル名.py` で動かす
5. 何も見ずにもう一度書く

最初から大きな Agent framework を作る必要はありません。各 Drill は、ひとつの考え方だけを小さく練習する問題です。

## 基本の流れ

Agent の中心は、この繰り返しです。

```text
user input
  -> FakeLLM
  -> tool_call なら Python 関数を実行
  -> tool result を messages に追加
  -> FakeLLM
  -> final なら終了
```

dict の正式な定義は [docs/message_contract.md](docs/message_contract.md) にまとめています。迷ったら README より先にこの定義を見てください。

この教材では、LLM response と message dict を次の形に分けます。

```python
{"type": "final", "content": "答えです。"}
{"type": "tool_call", "content": {"tool_name": "calculator", "arguments": {"expression": "1 + 1"}}}
{"role": "user", "content": "1 + 1 は？"}
{"role": "assistant", "content": "答えは2です。"}
{"role": "tool", "content": {"tool_name": "calculator", "result": 2}}
{"role": "tool", "content": {"tool_name": "calculator", "error": "失敗理由"}}
```

よく出る名前は次の通りです。最初はこの少ない語彙だけを使い、ドリルが進むごとに必要な名前だけ増やします。

- `type`: LLM の返答の種類。`final` または `tool_call`
- `role`: messages の発言者。`user` / `assistant` / `tool` / `system`
- `response`: LLM や関数から返る dict
- `call`: `response["content"]` に入る tool 実行依頼
- `result`: tool 実行結果
- `arguments`: tool に渡す引数 dict
- `messages`: user、assistant、tool の履歴
- `max_turns`: 終わらない Agent を止める上限

### `type` と `role` の違い

この教材では、`type` と `role` は別の種類の dict で使います。ひとつの dict に `type` と `role` を同時に入れません。

`type` は `FakeLLM.chat()` が返す dict の種類です。

```python
{"type": "tool_call", "content": {...}}
{"type": "final", "content": "..."}
```

- `tool_call`: LLM が「tool を実行してほしい」と返した
- `final`: LLM が「これが最終回答」と返した

`role` は `messages` に保存する会話履歴の発言者です。message dict には `role` を入れ、`type` は入れません。

```python
{"role": "user", "content": "..."}
{"role": "assistant", "content": "答えです。"}
{"role": "tool", "content": {"tool_name": "calculator", "result": 2}}
```

- `user`: ユーザー入力
- `tool`: tool を実行した結果
- `assistant`: LLM の返答を履歴に残す場合に使う

### dict の厳密なルール

この教材では、dict を次の2種類に分けます。

1. LLM response: `FakeLLM.chat()` の返り値。`type` と `content` を持つ。
2. message: `messages` に保存する履歴。`role` と `content` を持つ。

OK:

```python
response = {"type": "tool_call", "content": {"tool_name": "calculator", "arguments": {"expression": "1 + 1"}}}
messages.append({"role": "user", "content": "1 + 1 は？"})
messages.append({"role": "tool", "content": {"tool_name": "calculator", "result": 2}})
messages.append({"role": "assistant", "content": "答えは2です。"})
```

NG:

```python
message = {"role": "assistant", "type": "final", "content": "答えです。"}
message = {"role": "assistant", "content": {"type": "final", "content": "答えです。"}}
```

1つ目は、message dict に `type` が入っています。2つ目は、message の `content` に LLM response 全体を入れているため、`content["content"]` という分かりにくい形になります。

tool_call を実行するときは、`response` から `call` を取り出して使います。tool_call のために assistant message を必ず保存する必要はありません。

```python
response = llm.chat(messages)
call = response["content"]
result = calculator(**call["arguments"])
messages.append({"role": "tool", "content": {"tool_name": call["tool_name"], "result": result}})
```

たとえば、次のコードは `type` を見ていません。`messages` の中から、`role` が `tool` の履歴だけを取り出しています。

```python
tool_results = [message for message in messages if message.get("role") == "tool"]
```

## Drill 一覧

各回答例は、学習しやすいように小さく書いてあります。高度な章でも、まずは概念が動く最小実装を優先しています。

「作るクラス・関数」に名前がある Drill は、その名前で作ってください。`なし` の Drill は、まずは dict だけで書いて大丈夫です。
`FakeLLM` は本物の LLM の代わりをする練習用クラスです。Runner や Memory など、状態を持つものだけを少しずつクラスにします。

| Drill | お題 | 作るクラス・関数 | 回答例 |
| --- | --- | --- | --- |
| [0.1](#drill-0-1) | FakeLLM が final を返す | `FakeLLM.chat` | [drill_0_1_fake_llm_final.py](drill_0_1_fake_llm_final.py) |
| [0.2](#drill-0-2) | FakeLLM が tool_call を返す | `FakeLLM.chat` | [drill_0_2_fake_llm_tool_call.py](drill_0_2_fake_llm_tool_call.py) |
| [0.3](#drill-0-3) | arguments で関数を呼ぶ | `calculator` | [drill_0_3_tool_arguments.py](drill_0_3_tool_arguments.py) |
| [0.4](#drill-0-4) | tool result を message にする | `make_message` | [drill_0_4_tool_result_message.py](drill_0_4_tool_result_message.py) |
| [0.5](#drill-0-5) | FakeLLM を2回呼ぶ | `FakeLLM.chat` | [drill_0_5_fake_llm_two_turns.py](drill_0_5_fake_llm_two_turns.py) |
| [0.6](#drill-0-6) | 小さい Runner を関数で作る | `calculator`, `FakeLLM.chat`, `run` | [drill_0_6_tiny_runner.py](drill_0_6_tiny_runner.py) |
| [0.7](#drill-0-7) | tools dict で tool を探す | `calculator`, `run_tool` | [drill_0_7_tool_table.py](drill_0_7_tool_table.py) |
| [0.8](#drill-0-8) | Runner をクラスにする | `calculator`, `FakeLLM.chat`, `Runner.run` | [drill_0_8_runner_class.py](drill_0_8_runner_class.py) |
| [1](#drill-1) | FakeLLM で Agent ループを書く | `calculator`, `FakeLLM.chat`, `Runner.run` | [drill_1_agent_loop.py](drill_1_agent_loop.py) |
| [2](#drill-2) | max_turns で止める | `MaxTurnsExceededError`, `FakeLLM.chat`, `calculator`, `run` | [drill_2_max_turns.py](drill_2_max_turns.py) |
| [3](#drill-3) | calculator tool | `validate_expression`, `evaluate`, `calculator`, `FakeLLM.chat` | [drill_3_calculator_tool.py](drill_3_calculator_tool.py) |
| [4](#drill-4) | dictionary search tool | `search_faq`, `FakeLLM.chat` | [drill_4_dictionary_search_tool.py](drill_4_dictionary_search_tool.py) |
| [5](#drill-5) | tool error handling | `get_weather`, `run` | [drill_5_tool_error_handling.py](drill_5_tool_error_handling.py) |
| [6](#drill-6) | TaskPlan を返す | `TaskPlan.validate`, `FakeLLM.chat` | [drill_6_task_plan.py](drill_6_task_plan.py) |
| [7](#drill-7) | 壊れた JSON を repair する | `FakeLLM.repair`, `parse_or_repair` | [drill_7_json_repair.py](drill_7_json_repair.py) |
| [8](#drill-8) | short-term memory | `ShortTermMemory` | [drill_8_short_term_memory.py](drill_8_short_term_memory.py) |
| [9](#drill-9) | summary memory | `SummaryMemory` | [drill_9_summary_memory.py](drill_9_summary_memory.py) |
| [10](#drill-10) | key-value memory | `save_memory`, `read_memory`, `run` | [drill_10_key_value_memory.py](drill_10_key_value_memory.py) |
| [11](#drill-11) | keyword search RAG | `score`, `search_docs`, `answer` | [drill_11_keyword_search_rag.py](drill_11_keyword_search_rag.py) |
| [12](#drill-12) | citation 付き回答 | `answer_with_source`, `validate_sources` | [drill_12_citation_answer.py](drill_12_citation_answer.py) |
| [13](#drill-13) | plan -> act -> observe | `search_policy`, `run` | [drill_13_plan_act_observe.py](drill_13_plan_act_observe.py) |
| [14](#drill-14) | stop condition | `run` | [drill_14_stop_condition.py](drill_14_stop_condition.py) |
| [15](#drill-15) | router agent | `route`, `handoff` | [drill_15_router_agent.py](drill_15_router_agent.py) |
| [16](#drill-16) | agents as tools | `research_agent`, `writing_agent`, `review_agent`, `manager` | [drill_16_agents_as_tools.py](drill_16_agents_as_tools.py) |
| [17](#drill-17) | input guardrail | `input_guardrail`, `run` | [drill_17_input_guardrail.py](drill_17_input_guardrail.py) |
| [18](#drill-18) | tool approval | `request_tool`, `approve` | [drill_18_tool_approval.py](drill_18_tool_approval.py) |
| [19](#drill-19) | output guardrail | `output_guardrail` | [drill_19_output_guardrail.py](drill_19_output_guardrail.py) |
| [20](#drill-20) | trace logger | `TraceLogger.log`, `TraceLogger.jsonl` | [drill_20_trace_logger.py](drill_20_trace_logger.py) |
| [21](#drill-21) | eval dataset | `agent`, `evaluate` | [drill_21_eval_dataset.py](drill_21_eval_dataset.py) |
| [22](#drill-22) | CLI Agent | `chat`, `handle_command` | [drill_22_cli_agent.py](drill_22_cli_agent.py) |
| [23](#drill-23) | FastAPI endpoint | `agent`, `chat`, `trace` | [drill_23_fastapi_endpoint.py](drill_23_fastapi_endpoint.py) |
| [24](#drill-24) | SQLite persistence | `save_message`, `load_messages` | [drill_24_sqlite_persistence.py](drill_24_sqlite_persistence.py) |

---

## Level 0: Agent の材料

この Level では、Agent を作る前に必要な部品を1つずつ作ります。

- `FakeLLM.chat(...)` は、本物の LLM API の代わりに dict を返すだけの練習用メソッドです。
- `tool_call` は「この Python 関数を、この引数で呼んでください」という依頼です。
- `tool result` は、Python 関数を実行した結果を `messages` に残すための dict です。
- `Runner` は、user input、LLM、tool、messages の流れをまとめて動かすものです。

### <a id="drill-0-1"></a>Drill 0.1: FakeLLM が final を返す

作るもの: `FakeLLM.chat(message: str) -> dict`

FakeLLM に `こんにちは` と渡したら、次の dict を返してください。

```python
{"type": "final", "content": "こんにちは！"}
```

合格条件:

- `response["type"] == "final"`
- `response["content"]` を表示できる

条件を満たさない場合:

- `こんにちは` 以外の入力では、`type` は `final` のまま、`content` に `対応していません。` を返す

回答例: [drill_0_1_fake_llm_final.py](drill_0_1_fake_llm_final.py)

### <a id="drill-0-2"></a>Drill 0.2: FakeLLM が tool_call を返す

作るもの: `FakeLLM.chat(message: str) -> dict`

FakeLLM に `3 + 5 * 2 は？` と渡したら、calculator の tool_call を返してください。

`tool_call` の `content` には、tool 名と引数を入れます。

```python
{
    "tool_name": "calculator",
    "arguments": {"expression": "3 + 5 * 2"},
}
```

合格条件:

- `type` が `tool_call`
- `content["tool_name"]` が `calculator`
- `content["arguments"]["expression"]` が `3 + 5 * 2`

条件を満たさない場合:

- 対応していない入力では、tool_call せず `final` で `計算できません。` を返す

回答例: [drill_0_2_fake_llm_tool_call.py](drill_0_2_fake_llm_tool_call.py)

### <a id="drill-0-3"></a>Drill 0.3: arguments で関数を呼ぶ

作るもの: `calculator(expression: str) -> int`

`calculator(expression: str)` を作り、tool_call の `content["arguments"]` を `calculator(**arguments)` で渡してください。

`**arguments` は、dict をキーワード引数として関数に渡す Python の書き方です。

```python
arguments = {"expression": "3 + 5 * 2"}
calculator(**arguments)
```

これは次と同じ意味です。

```python
calculator(expression="3 + 5 * 2")
```

合格条件:

- `3 + 5 * 2` の結果が `13`
- 引数名は `expression`

条件を満たさない場合:

- 未対応の式では `ValueError` を出す

回答例: [drill_0_3_tool_arguments.py](drill_0_3_tool_arguments.py)

### <a id="drill-0-4"></a>Drill 0.4: tool result を message にする

作るもの: `make_message(tool_name: str, result: object) -> dict`

tool の結果を messages に入れる dict にしてください。

```python
{"role": "tool", "content": {"tool_name": "calculator", "result": 13}}
```

合格条件:

- `role` が `tool`
- `content` に tool 名と結果が入る

条件を満たさない場合:

- tool 名が空なら `ValueError` を出す

回答例: [drill_0_4_tool_result_message.py](drill_0_4_tool_result_message.py)

### <a id="drill-0-5"></a>Drill 0.5: FakeLLM を2回呼ぶ

作るもの: `FakeLLM.chat(messages: list[dict]) -> dict`

messages に tool result がなければ `tool_call`、あれば `final` を返す FakeLLM を作ってください。

`messages` は会話履歴の list です。tool result があるかどうかは、`role` が `tool` の message を探して判定します。

```python
tool_results = [message for message in messages if message.get("role") == "tool"]
```

合格条件:

- 1回目は `tool_call`
- 2回目は `final`

条件を満たさない場合:

- tool result に `error` が入っている場合は、`final` で `計算できませんでした。` を返す

回答例: [drill_0_5_fake_llm_two_turns.py](drill_0_5_fake_llm_two_turns.py)

### <a id="drill-0-6"></a>Drill 0.6: 小さい Runner を関数で作る

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `run(user_input: str) -> str`

`run(user_input: str) -> str` を作り、user message、tool_call、tool result、final までを1つの関数で動かしてください。

`run` の中では、次の順番で処理します。

1. `messages` に user message を入れる
2. `FakeLLM.chat(messages)` を呼ぶ
3. `tool_call` なら tool を実行する
4. tool result を `messages` に追加する
5. もう一度 `FakeLLM.chat(messages)` を呼ぶ
6. `final` の `content` を返す

合格条件:

- 出力が `答えは13です。`
- FakeLLM を2回呼ぶ
- tool result を messages に追加する

条件を満たさない場合:

- 未知の tool 名や未対応の LLM 応答では `ValueError` を出す
- tool 実行が失敗したら tool error を messages に追加し、`計算できませんでした。` を返す

回答例: [drill_0_6_tiny_runner.py](drill_0_6_tiny_runner.py)

### <a id="drill-0-7"></a>Drill 0.7: tools dict で tool を探す

作るもの: `calculator(expression: str) -> int`, `run_tool(call: dict, tools: dict) -> dict`

`tools = {"calculator": calculator}` を作り、`call["tool_name"]` で関数を探して実行してください。

`tools` は tool 名から関数を引くための dict です。

```python
tools = {"calculator": calculator}
tool = tools[call["tool_name"]]
result = tool(**call["arguments"])
```

合格条件:

- `tools["calculator"]` から calculator を呼べる
- tool result message の形は `{"role": "tool", "content": {"tool_name": ..., "result": ...}}`
- 引数は `call["arguments"]` から渡す

条件を満たさない場合:

- 未知の tool 名では `ValueError` を出す

回答例: [drill_0_7_tool_table.py](drill_0_7_tool_table.py)

### <a id="drill-0-8"></a>Drill 0.8: Runner をクラスにする

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `Runner.run(user_input: str) -> dict`

Drill 0.6 の `run` 関数を `Runner` クラスに移してください。まだ while ループは使わず、FakeLLM を2回呼ぶだけで大丈夫です。

`Runner` には `__init__` で `llm` と `tools` を渡して保存します。

```python
class Runner:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools
```

合格条件:

- `Runner(FakeLLM(), tools).run(user_input)` で動く
- `Runner` が `llm` と `tools` を持つ
- 返り値は `{"type": "final", "content": {"answer": ..., "messages": ...}}`

条件を満たさない場合:

- 未知の tool 名や未対応の LLM 応答では `ValueError` を出す

回答例: [drill_0_8_runner_class.py](drill_0_8_runner_class.py)

---

## Level 1: Agent の骨格

この Level では、0.x で作った固定の2回呼び出しを、終わるまで回す Agent loop にします。

- `while` で `FakeLLM.chat(messages)` を繰り返します。
- `response["type"] == "tool_call"` なら tool を実行して `messages` に足します。
- `response["type"] == "final"` ならそこで終了します。
- 終わらない Agent に備えて、`max_turns` で上限を作ります。

### <a id="drill-1"></a>Drill 1: FakeLLM で Agent ループを書く

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `Runner.run(user_input: str) -> dict`

Drill 0.8 の Runner に while ループを入れて、`final` が返るまで tool_call を処理してください。message や tool はまだクラスにせず、dict のまま扱います。

assistant の tool_call も履歴に残す場合は、`response` 全体ではなく `response["content"]` だけを message の `content` に入れます。`type` は LLM response のキーなので、`role` を持つ message には入れません。

```python
{"role": "assistant", "content": {"tool_name": "calculator", "arguments": {"expression": "3 + 5 * 2"}}}
```

合格条件:

- `Runner(FakeLLM(), tools).run(user_input)` で動く
- ログが user、assistant tool_call、tool、assistant final の順に残る
- 最終回答が `答えは13です。`

条件を満たさない場合:

- tool が見つからない場合は tool error を messages に残し、最終回答で失敗を伝える
- 未対応の LLM 応答では `ValueError` を出す

回答例: [drill_1_agent_loop.py](drill_1_agent_loop.py)

### <a id="drill-2"></a>Drill 2: max_turns を入れる

作るもの: `MaxTurnsExceededError`, `FakeLLM.chat(messages: list[dict]) -> dict`, `calculator(expression: str) -> int`, `run(user_input: str, max_turns: int = 3) -> list[dict]`

FakeLLM が毎回 calculator の `tool_call` を返すようにします。`run(user_input, max_turns=3)` で、終わらない処理を止めてください。

独自エラーは普通の class として作れます。

```python
class MaxTurnsExceededError(Exception):
    def __init__(self, message: str, messages: list[dict]):
        super().__init__(message)
        self.messages = messages
```

loop の中では、tool_call を処理した回数が `max_turns` を超えないようにします。

合格条件:

- `max_turns=3` なら tool_call は3回まで
- エラー文に `max_turns exceeded` が含まれる
- エラー時の messages を確認できる

条件を満たさない場合:

- `max_turns` が 1 未満なら `ValueError` を出す
- max_turns 内に `final` が返らない場合は `MaxTurnsExceededError` を出し、途中の messages を保持する

回答例: [drill_2_max_turns.py](drill_2_max_turns.py)

---

## Level 2: Tool Calling

この Level では、tool を少し実用寄りにします。

- tool は入力を必ず検査します。
- 成功したら `{"role": "tool", "content": {"result": ...}}` を残します。
- 失敗したら例外をそのまま外に出さず、`{"error": ...}` を tool message に入れます。
- LLM は、tool が不要な入力では `tool_call` ではなく `final` を返します。

### <a id="drill-3"></a>Drill 3: calculator tool

作るもの: `validate_expression(expression: str) -> None`, `evaluate(node)`, `calculator(expression: str)`, `FakeLLM.chat(user_input: str) -> dict`

式を受け取って計算する `calculator(expression)` を作ってください。

この Drill では、`eval()` は使わず、Python 標準ライブラリの `ast` で式を木として読みます。対応する node だけを許可すると、危険なコードを実行せずに計算できます。

```python
import ast

tree = ast.parse("12 * 8", mode="eval")
```

最初は `+`、`-`、`*`、`/`、数値だけ対応すれば十分です。

合格条件:

- `12 * 8` が `96`
- 危険な文字列は拒否する
- `import`、`open`、`exec`、`eval`、`__` を拒否する

条件を満たさない場合:

- 危険な文字列や未対応の構文では `ValueError` を出す
- calculator が不要な入力では tool_call せず `final` を返す

回答例: [drill_3_calculator_tool.py](drill_3_calculator_tool.py)

### <a id="drill-4"></a>Drill 4: dictionary search tool

作るもの: `search_faq(query: str) -> str`, `FakeLLM.chat(user_input: str) -> dict`

小さな FAQ dict を検索する `search_faq(query)` を作ってください。

この Drill で使う FAQ data は次の形にします。

```python
FAQ = {
    "refund": "返金は購入から30日以内に申請できます。",
    "shipping": "通常配送は3〜5営業日です。",
    "password": "パスワード再設定ページから変更できます。",
}
```

検索はまだシンプルで大丈夫です。`query` に `"返金"` が含まれていたら `FAQ["refund"]`、`"配送"` が含まれていたら `FAQ["shipping"]`、`"パスワード"` が含まれていたら `FAQ["password"]` を返してください。

`FakeLLM.chat(user_input)` は、必ず次の形の tool_call を返します。この Drill では Runner はまだ作らず、返ってきた `arguments` を自分で `search_faq(**arguments)` に渡します。

```python
{
    "type": "tool_call",
    "content": {
        "tool_name": "search_faq",
        "arguments": {"query": user_input},
    },
}
```

呼び出し例:

```python
response = FakeLLM().chat("配送にはどれくらいかかる？")
call = response["content"]
answer = search_faq(**call["arguments"])
```

合格条件:

- `search_faq("返金したい")` が `返金は購入から30日以内に申請できます。`
- `search_faq("配送にはどれくらいかかる？")` が `通常配送は3〜5営業日です。`
- `search_faq("パスワードを忘れた")` が `パスワード再設定ページから変更できます。`
- `search_faq("営業時間は？")` が `見つかりませんでした。`
- `FakeLLM.chat(...)` の `content["arguments"]["query"]` に元の user_input が入る

条件を満たさない場合:

- 空の query では `ValueError` を出す
- FAQ にない query では例外にせず `見つかりませんでした。` を返す

回答例: [drill_4_dictionary_search_tool.py](drill_4_dictionary_search_tool.py)

### <a id="drill-5"></a>Drill 5: tool error handling

作るもの: `get_weather(city: str) -> dict`, `run(city: str) -> list[dict]`

天気 tool が `ValueError` を出したとき、落とさず tool error と final response を messages に残してください。

この Drill で使う weather data は次の形にします。

```python
WEATHER = {
    "Tokyo": {"city": "Tokyo", "weather": "sunny", "temp": 22},
    "Osaka": {"city": "Osaka", "weather": "cloudy", "temp": 20},
}
```

`get_weather(city)` は、city が data にあればその dict を返し、なければ `ValueError(f"unknown city: {city}")` を出します。

`run(city)` は Runner の小さい版です。次の順で `messages` を作ります。

1. user message: `{"role": "user", "content": f"{city} の天気は？"}`
2. `response` として tool_call dict を作る
3. tool message。成功なら `result`、失敗なら `error` を入れる
4. assistant message に最終回答を入れる

tool_call は `messages` に入れず、実行用の `response` として扱います。`type` は LLM response のキーなので、`role` を持つ message と同じ階層には置きません。

```python
response = {
    "type": "tool_call",
    "content": {
        "tool_name": "get_weather",
        "arguments": {"city": city},
    },
}
```

final の assistant message は次の形です。

```python
{"role": "assistant", "content": "Tokyo は sunny です。"}
{"role": "assistant", "content": "天気を取得できませんでした。"}
```

tool の例外は `try` / `except` で受け取ります。

```python
try:
    result = get_weather(city)
    messages.append({"role": "tool", "content": {"tool_name": "weather", "result": result}})
except ValueError as error:
    messages.append({"role": "tool", "content": {"tool_name": "weather", "error": str(error)}})
```

合格条件:

- `run("Tokyo")` では tool message に `result` が入り、final が `Tokyo は sunny です。`
- `run("Unknown")` では tool message に `error` が入り、例外が外へ出ない
- `run("Unknown")` の最後の assistant message に `天気を取得できませんでした。` が入る

条件を満たさない場合:

- 天気を取得できない city では例外を外へ出さず、tool message に `error` を入れる
- 最終回答では `天気を取得できませんでした。` を返す

回答例: [drill_5_tool_error_handling.py](drill_5_tool_error_handling.py)

---

## Level 3: Structured Output

この Level では、文字列の回答ではなく、決まった形の dict を返す練習をします。

- structured output は、`content` の中身を決まったキーにそろえる考え方です。
- validate は「必要なキーや値が正しいか」を確認する処理です。
- JSON は文字列なので、Python の dict にするには `json.loads(text)` を使います。

### <a id="drill-6"></a>Drill 6: TaskPlan を返す

作るもの: `TaskPlan.validate() -> None`, `FakeLLM.chat(user_input: str) -> dict`

ユーザー依頼から `goal`、`steps`、`tools_needed`、`risk_level` を持つ TaskPlan を作ってください。
このドリルでは本物の LLM 呼び出しは使わず、`FakeLLM.chat()` が固定の structured output を返す最小実装で大丈夫です。
`FakeLLM.chat()` の返り値は、[docs/message_contract.md](docs/message_contract.md) の LLM response に従い、必ず `type` と `content` を持つ dict にします。

`TaskPlan` は `dataclass` で作ると、dict から作りやすくなります。

```python
from dataclasses import dataclass

@dataclass
class TaskPlan:
    goal: str
    steps: list[str]
    tools_needed: list[str]
    risk_level: str
```

`TaskPlan(**response["content"])` のように、dict をまとめて渡せます。

`FakeLLM.chat()` は、次の形の dict を返してください。

```python
{
    "type": "final",
    "content": {
        "goal": user_input,
        "steps": ["調査する", "構成を作る", "下書きを作る"],
        "tools_needed": ["search", "writer"],
        "risk_level": "medium",
    },
}
```

最後に、次のように `TaskPlan` に変換して validate してください。

```python
response = FakeLLM().chat("ブログ記事を調査して、構成を作って、下書きまで作ってください")
plan = TaskPlan(**response["content"])
plan.validate()
print(plan)
```

合格条件:

- `steps` が3個以上
- `risk_level` は `low` / `medium` / `high`
- validation できる

条件を満たさない場合:

- `steps` が3個未満、または `risk_level` が許可値以外なら `ValueError` を出す

回答例: [drill_6_task_plan.py](drill_6_task_plan.py)

### <a id="drill-7"></a>Drill 7: 壊れた JSON を repair する

作るもの: `FakeLLM.repair(broken_json: str) -> dict`, `parse_or_repair(text: str, retry: int = 2) -> dict`

壊れた JSON を parse し、失敗したら FakeLLM に repair させて再試行してください。
このドリルでも本物の LLM 呼び出しは使わず、`FakeLLM.repair()` が修正済み JSON 文字列を `content` に入れた LLM response を固定で返す実装で大丈夫です。
`FakeLLM.repair()` の返り値も、[docs/message_contract.md](docs/message_contract.md) に従い、必ず `type` と `content` を持つ dict にします。

JSON parse は `json.loads(text)` で行います。失敗すると `json.JSONDecodeError` が出るので、`except` で受け取り、エラー文を list に保存します。

```python
import json

try:
    data = json.loads(text)
except json.JSONDecodeError as error:
    errors.append(str(error))
```

`FakeLLM.repair()` は、たとえば次のような LLM response を返してください。

```python
class FakeLLM:
    def repair(self, broken_json: str) -> dict:
        return {
            "type": "final",
            "content": '{"goal": "調査する", "steps": ["検索", "要約"]}',
        }
```

`parse_or_repair()` では `FakeLLM()` を作り、最初の parse も含めて最大 `retry + 1` 回試してください。
parse に失敗したら `errors` にエラー文を追加し、`response = llm.repair(text)` で LLM response を受け取り、`text = response["content"]` で次の試行に進みます。

動作確認には、次のような壊れた JSON 文字列を使ってください。
これは Python の文字列としては正しいですが、JSON としてはキーに `"` がなく、末尾カンマもあるので `json.loads()` に失敗します。

```python
broken = '{ goal: "調査する", steps: ["検索", "要約",], }'
print(parse_or_repair(broken))
```

合格条件:

- retry 回数を持つ
- parse error を記録する
- valid JSON を dict にできる

条件を満たさない場合:

- retry 後も JSON にできなければ `ValueError` を出し、parse error の一覧を含める

回答例: [drill_7_json_repair.py](drill_7_json_repair.py)

---

## Level 4: Memory

この Level では、`messages` を毎回捨てずに保存します。

- short-term memory は、直近 N 件だけを残す memory です。
- summary memory は、古い messages を短い summary にまとめる memory です。
- key-value memory は、`key -> value` の dict として情報を保存する memory です。

### <a id="drill-8"></a>Drill 8: short-term memory

作るもの: `ShortTermMemory.add(role: str, content) -> None`, `ShortTermMemory.recent() -> list[dict]`

messages を保存し、直近 N 件だけ取り出す Memory を作ってください。
この Drill では、`add()` のたびに古い message を削除しなくても大丈夫です。
`self.messages` には追加された message を保存しておき、`recent()` が呼ばれたときだけ最新 `limit` 件を返してください。

この Drill では、Memory は内部に `self.messages` という list を持ちます。
`add()` が呼ばれるたびに、次の形の dict を list に追加してください。

```python
{"role": role, "content": content}
```

`role` は `"user"` / `"assistant"` / `"tool"` などの文字列です。
`content` は文字列だけでなく、tool result のような dict も受け取れるようにします。

直近 N 件は list の slice で取り出せます。

```python
self.messages[-self.limit:]
```

実装の流れ:

1. `__init__` で `limit` を受け取り、`self.messages = []` を作る
2. `limit < 1` なら `ValueError` を出す
3. `add()` で `{"role": role, "content": content}` を `self.messages` に追加する
4. `recent()` で `self.messages[-self.limit:]` を返す

動作確認例:

```python
memory = ShortTermMemory(limit=4)
memory.add("user", "1つめ")
memory.add("assistant", "返答1")
memory.add("tool", {"tool_name": "calculator", "result": 13})
memory.add("user", "2つめ")
memory.add("assistant", "返答2")

print(memory.recent())
# 先頭の user message は落ち、最新4件だけが返る
```

期待される戻り値は次の形です。

```python
[
    {"role": "assistant", "content": "返答1"},
    {"role": "tool", "content": {"tool_name": "calculator", "result": 13}},
    {"role": "user", "content": "2つめ"},
    {"role": "assistant", "content": "返答2"},
]
```

合格条件:

- `limit=4` なら最新4件だけ返す
- tool message も保存できる

条件を満たさない場合:

- `limit` が 1 未満なら `ValueError` を出す
- messages が limit 未満なら、ある分だけ返す

回答例: [drill_8_short_term_memory.py](drill_8_short_term_memory.py)

### <a id="drill-9"></a>Drill 9: summary memory

作るもの: `SummaryMemory.add(role: str, content: str) -> None`, `SummaryMemory.prompt_messages() -> list[dict]`

messages が増えたら古いものを summary にまとめ、prompt には summary と最新 messages だけ入れてください。

この Drill の summary は、本物の要約でなくて大丈夫です。古い message の `content` を `" / "` などでつなげた短い文字列として扱います。

この Drill では、最初は `messages` をそのまま貯めます。
ただし、`messages` が 10 件を超えたら、古い messages を `summary` に移し、`messages` 側には最新 `keep_recent` 件だけを残してください。

たとえば `keep_recent=4` で 12 件追加した場合は、`summary` に古い 8 件分の `content` が入り、`messages` には最新 4 件だけが残ります。

prompt に入れる summary は、system message として保存します。

```python
{"role": "system", "content": "summary: ..."}
```

実装の流れ:

1. `__init__` で `keep_recent`, `summary`, `messages` を用意する
2. `keep_recent < 1` なら `ValueError` を出す
3. `add()` で `{"role": role, "content": content}` を `messages` に追加する
4. 10件を超えたら、`messages[:-keep_recent]` を古い messages として取り出す
5. 古い messages の `content` を `" / "` でつなぎ、`summary` に保存または追記する
6. `messages` は `messages[-keep_recent:]` に入れ替える
7. すでに `summary` がある状態でさらに message が増えたら、`messages` が `keep_recent` 件だけになるように古い分を追加で `summary` に移す

`prompt_messages()` は、summary がまだ空なら `messages` をそのまま返します。
summary があるなら、先頭に system message を付けて返します。

```python
def prompt_messages(self) -> list[dict]:
    if not self.summary:
        return self.messages
    return [{"role": "system", "content": f"summary: {self.summary}"}] + self.messages
```

合格条件:

- 10件を超えたら summary ができる
- prompt が summary + 最新 `keep_recent` 件になる

条件を満たさない場合:

- 10件以下なら summary を作らず、messages をそのまま prompt に使う
- `keep_recent` が 1 未満なら `ValueError` を出す

回答例: [drill_9_summary_memory.py](drill_9_summary_memory.py)

### <a id="drill-10"></a>Drill 10: key-value memory

作るもの: `save_memory(key: str, value: str) -> str`, `read_memory(key: str) -> str`, `run(user_input: str) -> dict`

ユーザーの好みを保存・読み出しできる小さな memory store を作ってください。

memory store は普通の dict で大丈夫です。

```python
store = {}
store["favorite_language"] = "Python"
```

合格条件:

- `Pythonが好き` を保存する
- 後続質問で `content` に `Python` を返す
- 未保存の情報は作らない

条件を満たさない場合:

- 未保存の情報を聞かれたら `content` に `保存されていません。` を返す
- 対応していない入力では `content` に `まだ対応していません。` を返す

回答例: [drill_10_key_value_memory.py](drill_10_key_value_memory.py)

---

## Level 5: RAG

RAG は Retrieval Augmented Generation の略です。この教材では、まず「小さな docs dict から根拠を探し、その根拠を使って答える」だけにします。

- `docs` は file 名から本文を引く dict です。
- `score` は query と document がどれくらい合っているかを数値にします。
- `source` や `sources` は、どの document を根拠にしたかを残すための情報です。
- quote は、document からそのまま抜き出した根拠文です。

### <a id="drill-11"></a>Drill 11: keyword search RAG

作るもの: `score(query: str, file: str) -> int`, `search_docs(query: str, top_k: int = 1) -> list[tuple[str, str]]`, `answer(query: str) -> dict`

小さな docs dict を作り、query に近い document を keyword score で選んでください。

この Drill で使う docs data は次の形にします。

```python
DOCS = {
    "refund.md": "返金期限は購入から30日以内です。",
    "shipping.md": "配送日数は3〜5営業日です。",
    "account.md": "アカウント削除は設定画面から申請できます。",
}
```

keyword score は、query に含まれる単語の数で十分です。

```python
KEYWORDS = {"refund.md": ["返金", "期限"]}
score = sum(1 for keyword in KEYWORDS["refund.md"] if keyword in query)
```

`search_docs(query, top_k=1)` は、score が一番高い document を `(file, text)` の tuple で返します。

呼び出し例:

```python
results = search_docs("返金期限は？")
# [("refund.md", "返金期限は購入から30日以内です。")]
```

実装ヒント:

1. まず `DOCS` と `KEYWORDS` を上の例の形で用意します。
2. `score()` は `KEYWORDS[file]` を取り出し、query に含まれる keyword の数を数えます。
3. `search_docs()` は `DOCS.items()` を score の大きい順に並べ替えます。
4. 並べ替えたあと、score が 0 の document は返さないようにします。
5. `answer()` は `search_docs(query)` を呼び、見つかったら先頭の `(file, text)` を使います。

`answer()` の返り値は次の形にすると、後続の Drill と揃います。

```python
{
    "type": "final",
    "content": {
        "answer": "返金期限は購入から30日以内です。",
        "source": "refund.md",
    },
}
```

見つからなかった場合は、同じ形のまま `source` を `None` にします。

合格条件:

- `返金期限は？` で `refund.md`
- `content["source"]` が入る

条件を満たさない場合:

- score が 0 の場合は source を作らず、`content["answer"]` に `見つかりませんでした。` を返す

回答例: [drill_11_keyword_search_rag.py](drill_11_keyword_search_rag.py)

### <a id="drill-12"></a>Drill 12: citation 付き回答

作るもの: `answer_with_source(query: str) -> dict`, `validate_sources(response: dict) -> None`

回答に `sources` を付け、quote が document 内に存在することを確認してください。

この Drill で使う docs data は次の形にします。

```python
DOCS = {
    "refund.md": "返金は購入から30日以内に申請できます。",
    "shipping.md": "通常配送は3〜5営業日です。",
}
```

`sources` は list にします。1つの根拠だけでも list で持つと、複数根拠に拡張しやすくなります。

```python
{
    "type": "final",
    "content": {
        "answer": "返金は購入から30日以内に申請できます。",
        "sources": [{"file": "refund.md", "quote": "購入から30日以内"}],
    },
}
```

quote の確認は、`quote in document_text` でできます。

実装ヒント:

1. `answer_with_source()` では、まず query に `"返金"` が含まれているかを見ます。
2. 返金の質問なら `refund.md` の本文を根拠にして `answer` と `sources` を作ります。
3. `quote` は document の一部をそのまま入れます。たとえば `"購入から30日以内"` は `refund.md` の本文に含まれています。
4. response を作ったら、返す前に `validate_sources(response)` を呼びます。
5. `validate_sources()` は `response["content"]["sources"]` を1件ずつ見て、`DOCS[file]` の中に `quote` があるか確認します。

`validate_sources()` の中では、次の3つを取り出せれば十分です。

```python
file = source["file"]
quote = source["quote"]
document_text = DOCS[file]
```

合格条件:

- `sources` が空でない
- `quote` が document 内に存在する
- 不明なら `不明です` と答える

条件を満たさない場合:

- quote が document 内に存在しない場合は `ValueError` を出す
- 根拠が見つからない場合は `content["answer"]` を `不明です。`、`content["sources"]` を空にする

回答例: [drill_12_citation_answer.py](drill_12_citation_answer.py)

---

## Level 6: Planning

この Level では、Agent の途中状態を `state` dict にまとめます。

- `goal`: 何を達成したいか
- `plan`: これから行う手順
- `completed_steps`: 終わった手順
- `observations`: tool や検索で得た結果
- `final_answer`: 最終回答。これが入ったら終了

### <a id="drill-13"></a>Drill 13: plan -> act -> observe

作るもの: `search_policy() -> str`, `run(state: dict) -> dict`

state に goal、plan、completed_steps、observations、final_answer を持たせ、検索結果を観察して final を作ってください。返り値は `{"type": "state", "content": state}` にします。

入力の state は次の形にします。

```python
state = {
    "goal": "返金ポリシーを短く説明する",
    "plan": ["検索する", "要約する"],
    "completed_steps": [],
    "observations": [],
    "final_answer": None,
}
```

`act` は tool を実行すること、`observe` は tool 結果を state に記録することです。この Drill では `search_policy()` を act として呼び、返り値を `observations` に追加します。

合格条件:

- plan がある
- observation が追加される
- final_answer で終了する

条件を満たさない場合:

- observation が空なら final_answer を作らず、state に `error` を入れる

回答例: [drill_13_plan_act_observe.py](drill_13_plan_act_observe.py)

### <a id="drill-14"></a>Drill 14: stop condition

作るもの: `run(actions: list[dict], max_steps: int = 5) -> dict`

同じ action が続く場合や max_steps を超える場合に停止してください。

`actions` は次のような dict の list にします。

```python
actions = [
    {"tool": "search", "arguments": {"query": "返金"}},
    {"tool": "search", "arguments": {"query": "返金"}},
    {"tool": "search", "arguments": {"query": "返金"}},
]
```

stop condition は、Agent loop を止めるための条件です。この Drill では次のどちらかで止めます。

- 同じ action が3回続いた
- 処理数が `max_steps` に達した

合格条件:

- 同じ action が3回続いたら停止
- max_steps 超過で停止
- `content["reason"]` に停止理由を返す

条件を満たさない場合:

- action が空なら `content["reason"]` に `finished` を返す
- `max_steps` が 1 未満なら `ValueError` を出す

回答例: [drill_14_stop_condition.py](drill_14_stop_condition.py)

---

## Level 7: Multi-Agent

この Level では、複数の小さな Agent 関数を組み合わせます。

- router は、入力を見て担当先を選ぶ関数です。
- handoff は、選んだ担当先に処理を渡したことを dict に残す処理です。
- agents as tools は、Agent も普通の Python 関数として順番に呼べる、という考え方です。

### <a id="drill-15"></a>Drill 15: router agent

作るもの: `route(user_input: str) -> dict`, `handoff(user_input: str) -> dict`

問い合わせを billing、tech_support、general_faq のどれかに振り分けてください。

分類は keyword の `if` で十分です。

```python
if "請求" in user_input:
    route = "billing"
elif "ログイン" in user_input:
    route = "tech_support"
else:
    route = "general_faq"
```

合格条件:

- 請求は billing
- ログインは tech_support
- その他は general_faq
- `content["log"]` が残る

条件を満たさない場合:

- 空の入力では general_faq に振り分け、reason に `empty input` を残す

回答例: [drill_15_router_agent.py](drill_15_router_agent.py)

### <a id="drill-16"></a>Drill 16: agents as tools

作るもの: `research_agent(topic: str) -> str`, `writing_agent(research: str) -> str`, `review_agent(draft: str) -> str`, `manager(user_input: str) -> dict`

Manager が Research、Writing、Review の3つの Agent 関数を順番に呼んでください。

ここでの agent は class ではなく、普通の関数で大丈夫です。前の関数の返り値を次の関数に渡します。

```python
research = research_agent(topic)
draft = writing_agent(research)
review = review_agent(draft)
```

合格条件:

- 3つの agent tool が順に呼ばれる
- 前の出力が次に渡る
- final に review 結果が入る

条件を満たさない場合:

- topic が空なら agent tool を呼ばず、`ValueError` を出す

回答例: [drill_16_agents_as_tools.py](drill_16_agents_as_tools.py)

---

## Level 8: Guardrails

Guardrail は、Agent の入力、tool 実行、出力を検査して、危ない処理や根拠の弱い回答を止める仕組みです。

- input guardrail は、tool を呼ぶ前に user input を見る
- tool approval は、危険な tool を実行前に承認待ちにする
- output guardrail は、final answer をユーザーに返す前に見る

### <a id="drill-17"></a>Drill 17: input guardrail

作るもの: `input_guardrail(user_input: str) -> dict`, `run(user_input: str) -> dict`

危険入力を tool 実行前に止めてください。

返り値は、止めたかどうかを `blocked` で表します。

```python
{"type": "guardrail", "content": {"blocked": True, "reason": "dangerous input"}}
```

合格条件:

- `APIキー`、`rm -rf`、`パスワードを取得` をブロック
- `content["blocked"]` と `content["reason"]` が残る
- 通常入力は通す

条件を満たさない場合:

- 危険入力では tool を実行せず、`content["blocked"] = True` と reason を返す
- 空の入力では `content["blocked"] = True` と `empty input` を返す

回答例: [drill_17_input_guardrail.py](drill_17_input_guardrail.py)

### <a id="drill-18"></a>Drill 18: tool approval

作るもの: `request_tool(tool_name: str, arguments: dict) -> dict`, `approve(pending: dict, allowed: bool) -> dict`

破壊的 tool には承認待ち状態を作ってください。

この Drill では、tool を3種類に分けます。

- すぐ実行してよい tool: `read_file`
- 承認が必要な tool: `delete_file`, `send_email`
- 未知の tool: 実行せず reject

承認待ちは、まだ tool result ではありません。`approve(pending, allowed=True)` が呼ばれてから実行します。

合格条件:

- `read_file` は `type="tool_result"` を返す
- `delete_file` と `send_email` は `type="pending_approval"` を返す
- reject されたら `type="rejected"` を返し、実行しない

条件を満たさない場合:

- 未知の tool は `type="rejected"` にして実行しない
- 承認待ちを reject した場合は `type="rejected"` を返し、tool 結果を作らない

回答例: [drill_18_tool_approval.py](drill_18_tool_approval.py)

### <a id="drill-19"></a>Drill 19: output guardrail

作るもの: `output_guardrail(answer: dict) -> dict`

最終回答を検査し、sources なしの RAG 回答や根拠なし断定を reject してください。

output guardrail は、受け取った answer dict を見て、返してよいかを判定します。reject するときは理由を `content["reason"]` に残します。

合格条件:

- sources なしは reject
- `わかりません` は許可
- `content["reason"]` が残る

条件を満たさない場合:

- `content["answer"]` がない出力は reject する
- sources がない断定回答や `grounded=False` は reject する

回答例: [drill_19_output_guardrail.py](drill_19_output_guardrail.py)

---

## Level 9: Observability / Evaluation

この Level では、Agent が何をしたかを後から確認できるようにします。

- observability は、実行中に起きた event を記録して見えるようにすることです。
- trace は、1回の実行にひもづく event のまとまりです。
- eval は、入力と期待結果の dataset を使って Agent を確認することです。

### <a id="drill-20"></a>Drill 20: trace logger

作るもの: `TraceLogger.log(event_type: str, **data) -> None`, `TraceLogger.jsonl() -> str`

Agent のイベントを JSONL で保存する logger を作ってください。

JSONL は、1行に1つ JSON を置くログ形式です。Python では `json.dumps(...)` で dict を JSON 文字列にできます。

```python
import json

line = json.dumps(event, ensure_ascii=False)
```

`trace_id` は1回の実行を識別する ID、`timestamp` は記録した時刻です。

合格条件:

- trace_id がある
- timestamp がある
- user_input、tool_call、final を記録できる

条件を満たさない場合:

- event_type が空なら `ValueError` を出す
- data は空でも記録できる

回答例: [drill_20_trace_logger.py](drill_20_trace_logger.py)

### <a id="drill-21"></a>Drill 21: eval dataset

作るもの: `agent(user_input: str) -> dict`, `evaluate(dataset: list[dict]) -> dict`

小さな eval dataset を作り、期待 tool と期待回答をチェックしてください。

dataset は list of dict で大丈夫です。

```python
dataset = [
    {"input": "返金期限は？", "expected_answer": "30日", "expected_tool": "search_docs"}
]
```

各 case を `agent(case["input"])` に渡し、`result["content"]["tool_name"]` が `expected_tool` と一致し、`expected_answer` が `result["content"]["answer"]` に含まれていたら `passed=True` にします。

`agent(user_input)` の返り値は次の形にします。

```python
{
    "type": "final",
    "content": {"tool_name": "search_docs", "answer": "返金は30日以内です。"},
}
```

合格条件:

- `content["accuracy"]` を出す
- 失敗 case が見える
- 同じ dataset を何度も回せる

条件を満たさない場合:

- dataset が空なら `ValueError` を出す
- 不一致 case は `passed=False` として `content["rows"]` に残す

回答例: [drill_21_eval_dataset.py](drill_21_eval_dataset.py)

---

## Level 10: Production 風

この Level では、ここまで作った Agent の外側を少しだけ作ります。

- CLI は、ターミナルで入力を受け取る形です。この Drill では入力処理そのものではなく、`/history` などの command 処理だけを作ります。
- FastAPI は、Python 関数を HTTP endpoint として公開するためのライブラリです。未インストールでも落ちない形にします。
- SQLite は、Python 標準ライブラリ `sqlite3` で使える小さなデータベースです。

### <a id="drill-22"></a>Drill 22: CLI Agent

作るもの: `chat(user_input: str) -> dict`, `handle_command(text: str) -> dict`

`/history`、`/reset`、`/exit` を処理する CLI 用の関数を作ってください。

`handle_command(text)` は、先頭が `/` の入力だけを command として扱います。履歴は list に保存します。

合格条件:

- 通常入力に `type="final"` で回答する
- `/history` で `content["messages"]` を表示できる
- `/reset` で履歴を消せる

条件を満たさない場合:

- 未知の `/` コマンドでは `content["answer"]` に `unknown command` を返す
- `/reset` 後は history が空になる

回答例: [drill_22_cli_agent.py](drill_22_cli_agent.py)

### <a id="drill-23"></a>Drill 23: FastAPI endpoint

作るもの: `agent(user_input: str) -> dict`, `chat(payload: dict) -> dict`, `trace(trace_id: str) -> dict`

`POST /chat` と `GET /traces/{trace_id}` の最小例を作ってください。

FastAPI が入っていない環境でも README の学習が止まらないように、import は `try` / `except ModuleNotFoundError` で囲みます。

```python
try:
    from fastapi import FastAPI
except ModuleNotFoundError:
    FastAPI = None
```

合格条件:

- `/chat` が `type="final"` で answer と trace_id を返す
- `/traces/{trace_id}` が `type="trace"` で events を返す
- FastAPI 未インストール時も説明を出せる

条件を満たさない場合:

- payload に `user_input` がなければ `ValueError` を出す
- 未知の trace_id では events を空で返す

回答例: [drill_23_fastapi_endpoint.py](drill_23_fastapi_endpoint.py)

### <a id="drill-24"></a>Drill 24: SQLite persistence

作るもの: `save_message(session_id: str, role: str, content: str) -> None`, `load_messages(session_id: str) -> list[dict]`

SQLite に messages を保存し、session_id ごとに読み出してください。

SQLite は `sqlite3.connect(...)` で使います。最初に table を作り、保存時は `INSERT`、読み出し時は `SELECT` を使います。

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE IF NOT EXISTS messages (session_id TEXT, role TEXT, content TEXT)")
```

合格条件:

- messages table がある
- save と load ができる
- session_id で分かれる

条件を満たさない場合:

- session_id が空なら `ValueError` を出す
- 保存がない session_id では空リストを返す
- 読み出し結果は `{"role": ..., "content": ...}` のリストにする

回答例: [drill_24_sqlite_persistence.py](drill_24_sqlite_persistence.py)

---

## 4週間メニュー

- Week 1: Drill 0.1〜5
- Week 2: Drill 6〜12
- Week 3: Drill 13〜19
- Week 4: Drill 20〜24 と復習

## 最終試験

何も見ずに、次の機能を持つ小さな Customer Support Agent を作ってください。

- FAQ search
- calculator
- memory
- guardrail
- trace logger
- eval dataset
- `max_turns`

最初は 100 行以内で十分です。大きく作るより、messages に何が残るかを説明できることを目標にしてください。
