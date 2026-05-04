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

よく出る言葉は次の通りです。

- `type`: LLM の返答の種類。`final` または `tool_call`
- `role`: messages の発言者。`user` / `assistant` / `tool` / `system`
- `tool_call`: LLM が tool 実行を依頼する dict
- `arguments`: tool に渡す引数 dict
- `messages`: user、assistant、tool の履歴
- `max_turns`: 終わらない Agent を止める上限

## Drill 一覧

各回答例は、学習しやすいように小さく書いてあります。高度な章でも、まずは概念が動く最小実装を優先しています。

「クラスとして書くもの」に名前がある Drill は、その名前のクラスを作ってください。`なし` の Drill は、まずは関数と dict だけで書いて大丈夫です。
`FakeLLM` は本物の LLM の代わりをする練習用クラスです。Tool や Guardrail などの主役は、表で `なし` になっていれば関数で書きます。

| Drill | お題 | クラスとして書くもの | 回答例 |
| --- | --- | --- | --- |
| 0.1 | FakeLLM が final を返す | `FakeLLM` | `drill_0_1_fake_llm_final.py` |
| 0.2 | FakeLLM が tool_call を返す | `FakeLLM` | `drill_0_2_fake_llm_tool_call.py` |
| 0.3 | arguments で関数を呼ぶ | なし | `drill_0_3_tool_arguments.py` |
| 0.4 | tool result を message にする | なし | `drill_0_4_tool_result_message.py` |
| 0.5 | FakeLLM を2回呼ぶ | `FakeLLM` | `drill_0_5_fake_llm_two_turns.py` |
| 0.6 | 小さい Runner を関数で作る | `FakeLLM` | `drill_0_6_tiny_runner.py` |
| 1 | FakeLLM で Agent ループを書く | `Message`, `Tool`, `Agent`, `RunResult`, `FakeLLM`, `Runner` | `drill_1_agent_loop.py` |
| 2 | max_turns で止める | `MaxTurnsExceededError`, `FakeLLM` | `drill_2_max_turns.py` |
| 3 | calculator tool | `FakeLLM` | `drill_3_calculator_tool.py` |
| 4 | dictionary search tool | `FakeLLM` | `drill_4_dictionary_search_tool.py` |
| 5 | tool error handling | なし | `drill_5_tool_error_handling.py` |
| 6 | TaskPlan を返す | `TaskPlan`, `FakeLLM` | `drill_6_task_plan.py` |
| 7 | 壊れた JSON を repair する | `FakeLLM` | `drill_7_json_repair.py` |
| 8 | short-term memory | `ShortTermMemory` | `drill_8_short_term_memory.py` |
| 9 | summary memory | `SummaryMemory` | `drill_9_summary_memory.py` |
| 10 | key-value memory | なし | `drill_10_key_value_memory.py` |
| 11 | keyword search RAG | なし | `drill_11_keyword_search_rag.py` |
| 12 | citation 付き回答 | なし | `drill_12_citation_answer.py` |
| 13 | plan -> act -> observe | なし | `drill_13_plan_act_observe.py` |
| 14 | stop condition | なし | `drill_14_stop_condition.py` |
| 15 | router agent | なし | `drill_15_router_agent.py` |
| 16 | agents as tools | なし | `drill_16_agents_as_tools.py` |
| 17 | input guardrail | なし | `drill_17_input_guardrail.py` |
| 18 | tool approval | なし | `drill_18_tool_approval.py` |
| 19 | output guardrail | なし | `drill_19_output_guardrail.py` |
| 20 | trace logger | `TraceLogger` | `drill_20_trace_logger.py` |
| 21 | eval dataset | なし | `drill_21_eval_dataset.py` |
| 22 | CLI Agent | なし | `drill_22_cli_agent.py` |
| 23 | FastAPI endpoint | なし | `drill_23_fastapi_endpoint.py` |
| 24 | SQLite persistence | なし | `drill_24_sqlite_persistence.py` |

---

## Level 0: Agent の材料

### Drill 0.1: FakeLLM が final を返す

FakeLLM に `こんにちは` と渡したら、次の dict を返してください。

```python
{"type": "final", "content": "こんにちは！"}
```

合格条件:

- `response["type"] == "final"`
- `response["content"]` を表示できる

回答例: `drill_0_1_fake_llm_final.py`

### Drill 0.2: FakeLLM が tool_call を返す

FakeLLM に `3 + 5 * 2 は？` と渡したら、calculator の tool_call を返してください。

合格条件:

- `type` が `tool_call`
- `tool_name` が `calculator`
- `arguments["expression"]` が `3 + 5 * 2`

回答例: `drill_0_2_fake_llm_tool_call.py`

### Drill 0.3: arguments で関数を呼ぶ

`calculator(expression: str)` を作り、tool_call の `arguments` を `calculator(**arguments)` で渡してください。

合格条件:

- `3 + 5 * 2` の結果が `13`
- 引数名は `expression`

回答例: `drill_0_3_tool_arguments.py`

### Drill 0.4: tool result を message にする

tool の結果を messages に入れる dict にしてください。

```python
{"role": "tool", "content": {"tool_name": "calculator", "result": 13}}
```

合格条件:

- `role` が `tool`
- `content` に tool 名と結果が入る

回答例: `drill_0_4_tool_result_message.py`

### Drill 0.5: FakeLLM を2回呼ぶ

messages に tool result がなければ `tool_call`、あれば `final` を返す FakeLLM を作ってください。

合格条件:

- 1回目は `tool_call`
- 2回目は `final`

回答例: `drill_0_5_fake_llm_two_turns.py`

### Drill 0.6: 小さい Runner を関数で作る

`run(user_input: str) -> str` を作り、user message、tool_call、tool result、final までを1つの関数で動かしてください。

合格条件:

- 出力が `答えは13です。`
- FakeLLM を2回呼ぶ
- tool result を messages に追加する

回答例: `drill_0_6_tiny_runner.py`

---

## Level 1: Agent の骨格

### Drill 1: FakeLLM で Agent ループを書く

Drill 0.6 の dict 実装を、`Message`、`Tool`、`Agent`、`Runner` に分けてください。

合格条件:

- `Runner.run(agent, user_input)` で動く
- ログが user、assistant tool_call、tool、assistant final の順に残る
- 最終回答が `答えは13です。`

回答例: `drill_1_agent_loop.py`

### Drill 2: max_turns を入れる

FakeLLM が毎回 calculator の `tool_call` を返すようにします。`run(user_input, max_turns=3)` で、終わらない処理を止めてください。

合格条件:

- `max_turns=3` なら tool_call は3回まで
- エラー文に `max_turns exceeded` が含まれる
- エラー時の messages を確認できる

回答例: `drill_2_max_turns.py`

---

## Level 2: Tool Calling

### Drill 3: calculator tool

式を受け取って計算する `calculator(expression)` を作ってください。

合格条件:

- `12 * 8` が `96`
- 危険な文字列は拒否する
- `import`、`open`、`exec`、`eval`、`__` を拒否する

回答例: `drill_3_calculator_tool.py`

### Drill 4: dictionary search tool

小さな FAQ dict を検索する `search_faq(query)` を作ってください。

合格条件:

- 返金、配送、パスワードの質問に答える
- 未知の質問では `見つかりませんでした` を返す

回答例: `drill_4_dictionary_search_tool.py`

### Drill 5: tool error handling

天気 tool が `ValueError` を出したとき、落とさず tool error と final answer を messages に残してください。

合格条件:

- Tokyo は成功
- Unknown は tool error が残る
- 最終回答に `取得できませんでした` が含まれる

回答例: `drill_5_tool_error_handling.py`

---

## Level 3: Structured Output

### Drill 6: TaskPlan を返す

ユーザー依頼から `goal`、`steps`、`tools_needed`、`risk_level` を持つ TaskPlan を作ってください。

合格条件:

- `steps` が3個以上
- `risk_level` は `low` / `medium` / `high`
- validation できる

回答例: `drill_6_task_plan.py`

### Drill 7: 壊れた JSON を repair する

壊れた JSON を parse し、失敗したら FakeLLM に repair させて再試行してください。

合格条件:

- retry 回数を持つ
- parse error を記録する
- valid JSON を dict にできる

回答例: `drill_7_json_repair.py`

---

## Level 4: Memory

### Drill 8: short-term memory

messages を保存し、直近 N 件だけ取り出す Memory を作ってください。

合格条件:

- `limit=4` なら最新4件だけ返す
- tool message も保存できる

回答例: `drill_8_short_term_memory.py`

### Drill 9: summary memory

messages が増えたら古いものを summary にまとめ、prompt には summary と最新 messages だけ入れてください。

合格条件:

- 10件を超えたら summary ができる
- prompt が summary + recent になる

回答例: `drill_9_summary_memory.py`

### Drill 10: key-value memory

ユーザーの好みを保存・読み出しできる小さな memory store を作ってください。

合格条件:

- `Pythonが好き` を保存する
- 後続質問で `Python` を返す
- 未保存の情報は作らない

回答例: `drill_10_key_value_memory.py`

---

## Level 5: RAG

### Drill 11: keyword search RAG

小さな docs dict を作り、query に近い document を keyword score で選んでください。

合格条件:

- `返金期限は？` で `refund.md`
- 回答に source が入る

回答例: `drill_11_keyword_search_rag.py`

### Drill 12: citation 付き回答

回答に `sources` を付け、quote が document 内に存在することを確認してください。

合格条件:

- `sources` が空でない
- `quote` が document 内に存在する
- 不明なら `不明です` と答える

回答例: `drill_12_citation_answer.py`

---

## Level 6: Planning

### Drill 13: plan -> act -> observe

state に goal、plan、completed_steps、observations、final_answer を持たせ、検索結果を観察して final を作ってください。

合格条件:

- plan がある
- observation が追加される
- final_answer で終了する

回答例: `drill_13_plan_act_observe.py`

### Drill 14: stop condition

同じ action が続く場合や max_steps を超える場合に停止してください。

合格条件:

- 同じ action が3回続いたら停止
- max_steps 超過で停止
- 停止理由を返す

回答例: `drill_14_stop_condition.py`

---

## Level 7: Multi-Agent

### Drill 15: router agent

問い合わせを billing、tech_support、general_faq のどれかに振り分けてください。

合格条件:

- 請求は billing
- ログインは tech_support
- その他は general_faq
- handoff log が残る

回答例: `drill_15_router_agent.py`

### Drill 16: agents as tools

Manager が Research、Writing、Review の3つの Agent 関数を順番に呼んでください。

合格条件:

- 3つの agent tool が順に呼ばれる
- 前の出力が次に渡る
- final に review 結果が入る

回答例: `drill_16_agents_as_tools.py`

---

## Level 8: Guardrails

### Drill 17: input guardrail

危険入力を tool 実行前に止めてください。

合格条件:

- `APIキー`、`rm -rf`、`パスワードを取得` をブロック
- blocked reason が残る
- 通常入力は通す

回答例: `drill_17_input_guardrail.py`

### Drill 18: tool approval

破壊的 tool には承認待ち状態を作ってください。

合格条件:

- `read_file` は実行
- `delete_file` と `send_email` は `pending_approval`
- reject されたら実行しない

回答例: `drill_18_tool_approval.py`

### Drill 19: output guardrail

最終回答を検査し、sources なしの RAG 回答や根拠なし断定を reject してください。

合格条件:

- sources なしは reject
- `わかりません` は許可
- reject reason が残る

回答例: `drill_19_output_guardrail.py`

---

## Level 9: Observability / Evaluation

### Drill 20: trace logger

Agent のイベントを JSONL で保存する logger を作ってください。

合格条件:

- trace_id がある
- timestamp がある
- user_input、tool_call、final を記録できる

回答例: `drill_20_trace_logger.py`

### Drill 21: eval dataset

小さな eval dataset を作り、期待 tool と期待回答をチェックしてください。

合格条件:

- accuracy を出す
- 失敗 case が見える
- 同じ dataset を何度も回せる

回答例: `drill_21_eval_dataset.py`

---

## Level 10: Production 風

### Drill 22: CLI Agent

`/history`、`/reset`、`/exit` を処理する CLI 用の関数を作ってください。

合格条件:

- 通常入力に回答する
- history を表示できる
- reset で履歴を消せる

回答例: `drill_22_cli_agent.py`

### Drill 23: FastAPI endpoint

`POST /chat` と `GET /traces/{trace_id}` の最小例を作ってください。

合格条件:

- `/chat` が answer と trace_id を返す
- `/traces/{trace_id}` が events を返す
- FastAPI 未インストール時も説明を出せる

回答例: `drill_23_fastapi_endpoint.py`

### Drill 24: SQLite persistence

SQLite に messages を保存し、session_id ごとに読み出してください。

合格条件:

- messages table がある
- save と load ができる
- session_id で分かれる

回答例: `drill_24_sqlite_persistence.py`

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
