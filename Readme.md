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

この教材では、返り値の dict はできるだけ次の形に統一します。

```python
{"type": "final", "content": "答えです。"}
{"type": "tool_call", "content": {"tool_name": "calculator", "arguments": {"expression": "1 + 1"}}}
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

この教材の前半では、`type` と `role` は別の場所で使います。

`type` は `FakeLLM.chat()` が返す dict の種類です。

```python
{"type": "tool_call", "content": {...}}
{"type": "final", "content": "..."}
```

- `tool_call`: LLM が「tool を実行してほしい」と返した
- `final`: LLM が「これが最終回答」と返した

`role` は `messages` に保存する会話履歴の発言者です。

```python
{"role": "user", "content": "..."}
{"role": "tool", "content": {"tool_name": "calculator", "result": 2}}
```

- `user`: ユーザー入力
- `tool`: tool を実行した結果
- `assistant`: LLM の返答を履歴に残す場合に使う

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
| 0.1 | FakeLLM が final を返す | `FakeLLM.chat` | [drill_0_1_fake_llm_final.py](drill_0_1_fake_llm_final.py) |
| 0.2 | FakeLLM が tool_call を返す | `FakeLLM.chat` | [drill_0_2_fake_llm_tool_call.py](drill_0_2_fake_llm_tool_call.py) |
| 0.3 | arguments で関数を呼ぶ | `calculator` | [drill_0_3_tool_arguments.py](drill_0_3_tool_arguments.py) |
| 0.4 | tool result を message にする | `make_message` | [drill_0_4_tool_result_message.py](drill_0_4_tool_result_message.py) |
| 0.5 | FakeLLM を2回呼ぶ | `FakeLLM.chat` | [drill_0_5_fake_llm_two_turns.py](drill_0_5_fake_llm_two_turns.py) |
| 0.6 | 小さい Runner を関数で作る | `calculator`, `FakeLLM.chat`, `run` | [drill_0_6_tiny_runner.py](drill_0_6_tiny_runner.py) |
| 0.7 | tools dict で tool を探す | `calculator`, `run_tool` | [drill_0_7_tool_table.py](drill_0_7_tool_table.py) |
| 0.8 | Runner をクラスにする | `calculator`, `FakeLLM.chat`, `Runner.run` | [drill_0_8_runner_class.py](drill_0_8_runner_class.py) |
| 1 | FakeLLM で Agent ループを書く | `calculator`, `FakeLLM.chat`, `Runner.run` | [drill_1_agent_loop.py](drill_1_agent_loop.py) |
| 2 | max_turns で止める | `MaxTurnsExceededError`, `FakeLLM.chat`, `calculator`, `run` | [drill_2_max_turns.py](drill_2_max_turns.py) |
| 3 | calculator tool | `validate_expression`, `evaluate`, `calculator`, `FakeLLM.chat` | [drill_3_calculator_tool.py](drill_3_calculator_tool.py) |
| 4 | dictionary search tool | `search_faq`, `FakeLLM.chat` | [drill_4_dictionary_search_tool.py](drill_4_dictionary_search_tool.py) |
| 5 | tool error handling | `get_weather`, `run` | [drill_5_tool_error_handling.py](drill_5_tool_error_handling.py) |
| 6 | TaskPlan を返す | `TaskPlan.validate`, `FakeLLM.chat` | [drill_6_task_plan.py](drill_6_task_plan.py) |
| 7 | 壊れた JSON を repair する | `FakeLLM.repair`, `parse_or_repair` | [drill_7_json_repair.py](drill_7_json_repair.py) |
| 8 | short-term memory | `ShortTermMemory` | [drill_8_short_term_memory.py](drill_8_short_term_memory.py) |
| 9 | summary memory | `SummaryMemory` | [drill_9_summary_memory.py](drill_9_summary_memory.py) |
| 10 | key-value memory | `save_memory`, `read_memory`, `run` | [drill_10_key_value_memory.py](drill_10_key_value_memory.py) |
| 11 | keyword search RAG | `score`, `search_docs`, `answer` | [drill_11_keyword_search_rag.py](drill_11_keyword_search_rag.py) |
| 12 | citation 付き回答 | `answer_with_source`, `validate_sources` | [drill_12_citation_answer.py](drill_12_citation_answer.py) |
| 13 | plan -> act -> observe | `search_policy`, `run` | [drill_13_plan_act_observe.py](drill_13_plan_act_observe.py) |
| 14 | stop condition | `run` | [drill_14_stop_condition.py](drill_14_stop_condition.py) |
| 15 | router agent | `route`, `handoff` | [drill_15_router_agent.py](drill_15_router_agent.py) |
| 16 | agents as tools | `research_agent`, `writing_agent`, `review_agent`, `manager` | [drill_16_agents_as_tools.py](drill_16_agents_as_tools.py) |
| 17 | input guardrail | `input_guardrail`, `run` | [drill_17_input_guardrail.py](drill_17_input_guardrail.py) |
| 18 | tool approval | `request_tool`, `approve` | [drill_18_tool_approval.py](drill_18_tool_approval.py) |
| 19 | output guardrail | `output_guardrail` | [drill_19_output_guardrail.py](drill_19_output_guardrail.py) |
| 20 | trace logger | `TraceLogger.log`, `TraceLogger.jsonl` | [drill_20_trace_logger.py](drill_20_trace_logger.py) |
| 21 | eval dataset | `agent`, `evaluate` | [drill_21_eval_dataset.py](drill_21_eval_dataset.py) |
| 22 | CLI Agent | `chat`, `handle_command` | [drill_22_cli_agent.py](drill_22_cli_agent.py) |
| 23 | FastAPI endpoint | `agent`, `chat`, `trace` | [drill_23_fastapi_endpoint.py](drill_23_fastapi_endpoint.py) |
| 24 | SQLite persistence | `save_message`, `load_messages` | [drill_24_sqlite_persistence.py](drill_24_sqlite_persistence.py) |

---

## Level 0: Agent の材料

### Drill 0.1: FakeLLM が final を返す

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

### Drill 0.2: FakeLLM が tool_call を返す

作るもの: `FakeLLM.chat(message: str) -> dict`

FakeLLM に `3 + 5 * 2 は？` と渡したら、calculator の tool_call を返してください。

合格条件:

- `type` が `tool_call`
- `content["tool_name"]` が `calculator`
- `content["arguments"]["expression"]` が `3 + 5 * 2`

条件を満たさない場合:

- 対応していない入力では、tool_call せず `final` で `計算できません。` を返す

回答例: [drill_0_2_fake_llm_tool_call.py](drill_0_2_fake_llm_tool_call.py)

### Drill 0.3: arguments で関数を呼ぶ

作るもの: `calculator(expression: str) -> int`

`calculator(expression: str)` を作り、tool_call の `content["arguments"]` を `calculator(**arguments)` で渡してください。

合格条件:

- `3 + 5 * 2` の結果が `13`
- 引数名は `expression`

条件を満たさない場合:

- 未対応の式では `ValueError` を出す

回答例: [drill_0_3_tool_arguments.py](drill_0_3_tool_arguments.py)

### Drill 0.4: tool result を message にする

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

### Drill 0.5: FakeLLM を2回呼ぶ

作るもの: `FakeLLM.chat(messages: list[dict]) -> dict`

messages に tool result がなければ `tool_call`、あれば `final` を返す FakeLLM を作ってください。

合格条件:

- 1回目は `tool_call`
- 2回目は `final`

条件を満たさない場合:

- tool result に `error` が入っている場合は、`final` で `計算できませんでした。` を返す

回答例: [drill_0_5_fake_llm_two_turns.py](drill_0_5_fake_llm_two_turns.py)

### Drill 0.6: 小さい Runner を関数で作る

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `run(user_input: str) -> str`

`run(user_input: str) -> str` を作り、user message、tool_call、tool result、final までを1つの関数で動かしてください。

合格条件:

- 出力が `答えは13です。`
- FakeLLM を2回呼ぶ
- tool result を messages に追加する

条件を満たさない場合:

- 未知の tool 名や未対応の LLM 応答では `ValueError` を出す
- tool 実行が失敗したら tool error を messages に追加し、`計算できませんでした。` を返す

回答例: [drill_0_6_tiny_runner.py](drill_0_6_tiny_runner.py)

### Drill 0.7: tools dict で tool を探す

作るもの: `calculator(expression: str) -> int`, `run_tool(call: dict, tools: dict) -> dict`

`tools = {"calculator": calculator}` を作り、`call["tool_name"]` で関数を探して実行してください。

合格条件:

- `tools["calculator"]` から calculator を呼べる
- tool result message の形は `{"role": "tool", "content": {"tool_name": ..., "result": ...}}`
- 引数は `call["arguments"]` から渡す

条件を満たさない場合:

- 未知の tool 名では `ValueError` を出す

回答例: [drill_0_7_tool_table.py](drill_0_7_tool_table.py)

### Drill 0.8: Runner をクラスにする

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `Runner.run(user_input: str) -> dict`

Drill 0.6 の `run` 関数を `Runner` クラスに移してください。まだ while ループは使わず、FakeLLM を2回呼ぶだけで大丈夫です。

合格条件:

- `Runner(FakeLLM(), tools).run(user_input)` で動く
- `Runner` が `llm` と `tools` を持つ
- 返り値は `{"type": "final", "content": {"answer": ..., "messages": ...}}`

条件を満たさない場合:

- 未知の tool 名や未対応の LLM 応答では `ValueError` を出す

回答例: [drill_0_8_runner_class.py](drill_0_8_runner_class.py)

---

## Level 1: Agent の骨格

### Drill 1: FakeLLM で Agent ループを書く

作るもの: `calculator(expression: str) -> int`, `FakeLLM.chat(messages: list[dict]) -> dict`, `Runner.run(user_input: str) -> dict`

Drill 0.8 の Runner に while ループを入れて、`final` が返るまで tool_call を処理してください。message や tool はまだクラスにせず、dict のまま扱います。

合格条件:

- `Runner(FakeLLM(), tools).run(user_input)` で動く
- ログが user、assistant tool_call、tool、assistant final の順に残る
- 最終回答が `答えは13です。`

条件を満たさない場合:

- tool が見つからない場合は tool error を messages に残し、最終回答で失敗を伝える
- 未対応の LLM 応答では `ValueError` を出す

回答例: [drill_1_agent_loop.py](drill_1_agent_loop.py)

### Drill 2: max_turns を入れる

作るもの: `MaxTurnsExceededError`, `FakeLLM.chat(messages: list[dict]) -> dict`, `calculator(expression: str) -> int`, `run(user_input: str, max_turns: int = 3) -> list[dict]`

FakeLLM が毎回 calculator の `tool_call` を返すようにします。`run(user_input, max_turns=3)` で、終わらない処理を止めてください。

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

### Drill 3: calculator tool

作るもの: `validate_expression(expression: str) -> None`, `evaluate(node)`, `calculator(expression: str)`, `FakeLLM.chat(user_input: str) -> dict`

式を受け取って計算する `calculator(expression)` を作ってください。

合格条件:

- `12 * 8` が `96`
- 危険な文字列は拒否する
- `import`、`open`、`exec`、`eval`、`__` を拒否する

条件を満たさない場合:

- 危険な文字列や未対応の構文では `ValueError` を出す
- calculator が不要な入力では tool_call せず `final` を返す

回答例: [drill_3_calculator_tool.py](drill_3_calculator_tool.py)

### Drill 4: dictionary search tool

作るもの: `search_faq(query: str) -> str`, `FakeLLM.chat(user_input: str) -> dict`

小さな FAQ dict を検索する `search_faq(query)` を作ってください。

合格条件:

- 返金、配送、パスワードの質問に答える
- 未知の質問では `見つかりませんでした` を返す

条件を満たさない場合:

- 空の query では `ValueError` を出す
- FAQ にない query では例外にせず `見つかりませんでした。` を返す

回答例: [drill_4_dictionary_search_tool.py](drill_4_dictionary_search_tool.py)

### Drill 5: tool error handling

作るもの: `get_weather(city: str) -> dict`, `run(city: str) -> list[dict]`

天気 tool が `ValueError` を出したとき、落とさず tool error と final response を messages に残してください。

合格条件:

- Tokyo は成功
- Unknown は tool error が残る
- 最終回答に `取得できませんでした` が含まれる

条件を満たさない場合:

- 天気を取得できない city では例外を外へ出さず、tool message に `error` を入れる
- 最終回答では `天気を取得できませんでした。` を返す

回答例: [drill_5_tool_error_handling.py](drill_5_tool_error_handling.py)

---

## Level 3: Structured Output

### Drill 6: TaskPlan を返す

作るもの: `TaskPlan.validate() -> None`, `FakeLLM.chat(user_input: str) -> dict`

ユーザー依頼から `goal`、`steps`、`tools_needed`、`risk_level` を持つ TaskPlan を作ってください。

合格条件:

- `steps` が3個以上
- `risk_level` は `low` / `medium` / `high`
- validation できる

条件を満たさない場合:

- `steps` が3個未満、または `risk_level` が許可値以外なら `ValueError` を出す

回答例: [drill_6_task_plan.py](drill_6_task_plan.py)

### Drill 7: 壊れた JSON を repair する

作るもの: `FakeLLM.repair(broken_json: str) -> str`, `parse_or_repair(text: str, retry: int = 2) -> dict`

壊れた JSON を parse し、失敗したら FakeLLM に repair させて再試行してください。

合格条件:

- retry 回数を持つ
- parse error を記録する
- valid JSON を dict にできる

条件を満たさない場合:

- retry 後も JSON にできなければ `ValueError` を出し、parse error の一覧を含める

回答例: [drill_7_json_repair.py](drill_7_json_repair.py)

---

## Level 4: Memory

### Drill 8: short-term memory

作るもの: `ShortTermMemory.add(role: str, content) -> None`, `ShortTermMemory.recent() -> list[dict]`

messages を保存し、直近 N 件だけ取り出す Memory を作ってください。

合格条件:

- `limit=4` なら最新4件だけ返す
- tool message も保存できる

条件を満たさない場合:

- `limit` が 1 未満なら `ValueError` を出す
- messages が limit 未満なら、ある分だけ返す

回答例: [drill_8_short_term_memory.py](drill_8_short_term_memory.py)

### Drill 9: summary memory

作るもの: `SummaryMemory.add(role: str, content: str) -> None`, `SummaryMemory.prompt_messages() -> list[dict]`

messages が増えたら古いものを summary にまとめ、prompt には summary と最新 messages だけ入れてください。

合格条件:

- 10件を超えたら summary ができる
- prompt が summary + recent になる

条件を満たさない場合:

- 10件以下なら summary を作らず、messages をそのまま prompt に使う
- `keep_recent` が 1 未満なら `ValueError` を出す

回答例: [drill_9_summary_memory.py](drill_9_summary_memory.py)

### Drill 10: key-value memory

作るもの: `save_memory(key: str, value: str) -> str`, `read_memory(key: str) -> str`, `run(user_input: str) -> dict`

ユーザーの好みを保存・読み出しできる小さな memory store を作ってください。

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

### Drill 11: keyword search RAG

作るもの: `score(query: str, file: str) -> int`, `search_docs(query: str, top_k: int = 1)`, `answer(query: str) -> dict`

小さな docs dict を作り、query に近い document を keyword score で選んでください。

合格条件:

- `返金期限は？` で `refund.md`
- `content["source"]` が入る

条件を満たさない場合:

- score が 0 の場合は source を作らず、`content["answer"]` に `見つかりませんでした。` を返す

回答例: [drill_11_keyword_search_rag.py](drill_11_keyword_search_rag.py)

### Drill 12: citation 付き回答

作るもの: `answer_with_source(query: str) -> dict`, `validate_sources(response: dict) -> None`

回答に `sources` を付け、quote が document 内に存在することを確認してください。

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

### Drill 13: plan -> act -> observe

作るもの: `search_policy() -> str`, `run(state: dict) -> dict`

state に goal、plan、completed_steps、observations、final_answer を持たせ、検索結果を観察して final を作ってください。返り値は `{"type": "state", "content": state}` にします。

合格条件:

- plan がある
- observation が追加される
- final_answer で終了する

条件を満たさない場合:

- observation が空なら final_answer を作らず、state に `error` を入れる

回答例: [drill_13_plan_act_observe.py](drill_13_plan_act_observe.py)

### Drill 14: stop condition

作るもの: `run(actions: list[dict], max_steps: int = 5) -> dict`

同じ action が続く場合や max_steps を超える場合に停止してください。

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

### Drill 15: router agent

作るもの: `route(user_input: str) -> dict`, `handoff(user_input: str) -> dict`

問い合わせを billing、tech_support、general_faq のどれかに振り分けてください。

合格条件:

- 請求は billing
- ログインは tech_support
- その他は general_faq
- `content["log"]` が残る

条件を満たさない場合:

- 空の入力では general_faq に振り分け、reason に `empty input` を残す

回答例: [drill_15_router_agent.py](drill_15_router_agent.py)

### Drill 16: agents as tools

作るもの: `research_agent(topic: str) -> str`, `writing_agent(research: str) -> str`, `review_agent(draft: str) -> str`, `manager(user_input: str) -> dict`

Manager が Research、Writing、Review の3つの Agent 関数を順番に呼んでください。

合格条件:

- 3つの agent tool が順に呼ばれる
- 前の出力が次に渡る
- final に review 結果が入る

条件を満たさない場合:

- topic が空なら agent tool を呼ばず、`ValueError` を出す

回答例: [drill_16_agents_as_tools.py](drill_16_agents_as_tools.py)

---

## Level 8: Guardrails

### Drill 17: input guardrail

作るもの: `input_guardrail(user_input: str) -> dict`, `run(user_input: str) -> dict`

危険入力を tool 実行前に止めてください。

合格条件:

- `APIキー`、`rm -rf`、`パスワードを取得` をブロック
- `content["blocked"]` と `content["reason"]` が残る
- 通常入力は通す

条件を満たさない場合:

- 危険入力では tool を実行せず、`content["blocked"] = True` と reason を返す
- 空の入力では `content["blocked"] = True` と `empty input` を返す

回答例: [drill_17_input_guardrail.py](drill_17_input_guardrail.py)

### Drill 18: tool approval

作るもの: `request_tool(tool_name: str, arguments: dict) -> dict`, `approve(pending: dict, allowed: bool) -> dict`

破壊的 tool には承認待ち状態を作ってください。

合格条件:

- `read_file` は `type="tool_result"` を返す
- `delete_file` と `send_email` は `type="pending_approval"` を返す
- reject されたら `type="rejected"` を返し、実行しない

条件を満たさない場合:

- 未知の tool は `type="rejected"` にして実行しない
- 承認待ちを reject した場合は `type="rejected"` を返し、tool 結果を作らない

回答例: [drill_18_tool_approval.py](drill_18_tool_approval.py)

### Drill 19: output guardrail

作るもの: `output_guardrail(answer: dict) -> dict`

最終回答を検査し、sources なしの RAG 回答や根拠なし断定を reject してください。

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

### Drill 20: trace logger

作るもの: `TraceLogger.log(event_type: str, **data) -> None`, `TraceLogger.jsonl() -> str`

Agent のイベントを JSONL で保存する logger を作ってください。

合格条件:

- trace_id がある
- timestamp がある
- user_input、tool_call、final を記録できる

条件を満たさない場合:

- event_type が空なら `ValueError` を出す
- data は空でも記録できる

回答例: [drill_20_trace_logger.py](drill_20_trace_logger.py)

### Drill 21: eval dataset

作るもの: `agent(user_input: str) -> dict`, `evaluate(dataset: list[dict]) -> dict`

小さな eval dataset を作り、期待 tool と期待回答をチェックしてください。

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

### Drill 22: CLI Agent

作るもの: `chat(user_input: str) -> dict`, `handle_command(text: str) -> dict`

`/history`、`/reset`、`/exit` を処理する CLI 用の関数を作ってください。

合格条件:

- 通常入力に `type="final"` で回答する
- `/history` で `content["messages"]` を表示できる
- `/reset` で履歴を消せる

条件を満たさない場合:

- 未知の `/` コマンドでは `content["answer"]` に `unknown command` を返す
- `/reset` 後は history が空になる

回答例: [drill_22_cli_agent.py](drill_22_cli_agent.py)

### Drill 23: FastAPI endpoint

作るもの: `agent(user_input: str) -> dict`, `chat(payload: dict) -> dict`, `trace(trace_id: str) -> dict`

`POST /chat` と `GET /traces/{trace_id}` の最小例を作ってください。

合格条件:

- `/chat` が `type="final"` で answer と trace_id を返す
- `/traces/{trace_id}` が `type="trace"` で events を返す
- FastAPI 未インストール時も説明を出せる

条件を満たさない場合:

- payload に `user_input` がなければ `ValueError` を出す
- 未知の trace_id では events を空で返す

回答例: [drill_23_fastapi_endpoint.py](drill_23_fastapi_endpoint.py)

### Drill 24: SQLite persistence

作るもの: `save_message(session_id: str, role: str, content: str) -> None`, `load_messages(session_id: str) -> list[dict]`

SQLite に messages を保存し、session_id ごとに読み出してください。

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
