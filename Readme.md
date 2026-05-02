# AI Agent Drill

Fake LLM から始めて、Tool Calling、Memory、RAG、Planning、Guardrails、Evaluation、Production 風の実装までを順番に体へ入れる練習メニューです。

## 進め方

- 1 Drill ずつ小さく実装する
- 本物の API を使う前に、Fake LLM で制御フローを確認する
- 各 Drill の「合格条件」をテストとして書く
- 失敗した Drill は、翌日に何も見ずに再実装する

---

## Level 1: Agent の骨格を作る

### Drill 1: Fake LLM で Agent ループを書く

本物の API は使わず、Fake LLM を作って Agent の流れだけ実装します。

**お題**

ユーザー入力:

```text
3 + 5 * 2 は？
```

Fake LLM の 1 回目の返答:

```json
{
  "type": "tool_call",
  "tool_name": "calculator",
  "arguments": {
    "expression": "3 + 5 * 2"
  }
}
```

tool 実行後の Fake LLM の返答:

```json
{
  "type": "final",
  "content": "答えは13です。"
}
```

**実装するもの**

- `Message`
- `Tool`
- `Agent`
- `Runner`
- `calculator tool`
- `FakeLLM`

**合格条件**

- 入力: `3 + 5 * 2 は？`
- 出力: `答えは13です。`
- ログが次の順番で残る
  1. user message
  2. assistant tool_call
  3. tool result
  4. assistant final

### Drill 2: max_turns を入れる

Agent が無限に tool を呼び続ける Fake LLM を作ります。

**お題**

Fake LLM が毎回これを返します。

```json
{
  "type": "tool_call",
  "tool_name": "calculator",
  "arguments": {
    "expression": "1 + 1"
  }
}
```

**実装するもの**

- `max_turns`
- `max_turns` を超えたら例外
- 例外時のログ

**合格条件**

- `max_turns=3` のとき、4 回目に進まず停止する
- エラー内容に `max_turns exceeded` が含まれる

---

## Level 2: Tool Calling を体に覚えさせる

Tool use は、多くの Agent 実装の中心です。モデルが tool call を返し、アプリが実行して tool result を返す形を練習します。

### Drill 3: calculator tool

**お題**

次の入力に対応します。

```text
12 * 8 は？
100 / 4 + 7 は？
2 ** 10 は？
```

**実装するもの**

- tool schema
- arguments validation
- tool execution
- tool result message

**制約**

危険な式は実行しない。

禁止:

- `import`
- `open`
- `exec`
- `eval` の直接使用
- `__` が含まれる式

**合格条件**

- `12 * 8 は？` -> calculator が呼ばれる
- `こんにちは` -> calculator は呼ばれない
- `__import__('os')` -> 拒否される

### Drill 4: dictionary search tool

小さな辞書を検索する Agent を作ります。

**データ**

```python
FAQ = {
    "refund": "返金は購入から30日以内に申請できます。",
    "shipping": "通常配送は3〜5営業日です。",
    "password": "パスワード再設定ページから変更できます。",
}
```

**入力例**

```text
返金について教えて
配送にはどれくらいかかる？
パスワードを忘れました
```

**実装するもの**

- `search_faq tool`
- query string の validation
- 見つからないときの fallback

**合格条件**

- 返金 -> refund tool result を使う
- 配送 -> shipping tool result を使う
- 未知の質問 -> `見つかりませんでした` を含む

### Drill 5: tool error handling

天気 API 風の mock tool を作ります。

**tool**

```python
def get_weather(city: str) -> dict:
    ...
```

**挙動**

- Tokyo -> `{"city": "Tokyo", "weather": "sunny", "temp": 22}`
- Osaka -> `{"city": "Osaka", "weather": "cloudy", "temp": 20}`
- Unknown -> `ValueError` を raise

**実装するもの**

- tool 例外を握りつぶさない
- tool error message を履歴に追加
- LLM が最終回答でエラーを説明できるようにする

**合格条件**

- Tokyo の天気 -> 成功
- 存在しない都市 -> tool error がログに残る
- 最終回答に `取得できませんでした` が含まれる

---

## Level 3: Structured Output を反復する

自然文を後から parse するより、最初から JSON や Pydantic model として受ける形を練習します。

### Drill 6: TaskPlan を返す Agent

ユーザーの依頼から、作業計画を JSON で返します。

**入力**

```text
ブログ記事を調査して、構成を作って、下書きまで作ってください
```

**出力 schema**

```python
class TaskPlan(BaseModel):
    goal: str
    steps: list[str]
    tools_needed: list[str]
    risk_level: Literal["low", "medium", "high"]
```

**合格条件**

- JSON として parse できる
- Pydantic validation が通る
- `steps` が 3 個以上ある
- `risk_level` が `low` / `medium` / `high` のどれか

### Drill 7: 壊れた JSON を repair する

**お題**

Fake LLM が壊れた JSON を返します。

```text
{ goal: "調査する", steps: ["検索", "要約",], }
```

**実装するもの**

- parse 失敗を検出
- repair prompt を作る
- もう一度 LLM に投げる
- retry 回数制限

**合格条件**

- `retry=2` 以内に valid JSON になる
- retry 超過時は例外
- parse error のログが残る

---

## Level 4: Memory を作る

### Drill 8: short-term memory

会話履歴を保持する Memory を作ります。

**実装するもの**

- messages を保存
- 直近 N 件だけ取り出す
- `system` / `user` / `assistant` / `tool` の role を区別

**合格条件**

- `N=4` のとき、最新 4 件だけ prompt に入る
- tool result も履歴に残る
- 古い履歴は prompt に入らない

### Drill 9: summary memory

古い会話を summary に圧縮します。

**実装するもの**

- messages が 10 件を超えたら summary を更新
- summary + 最新 messages で prompt を作る
- summary 更新も Fake LLM でテスト

**合格条件**

- messages が 20 件あっても prompt には summary + 最新 N 件だけ入る
- summary にユーザーの好みが残る

### Drill 10: key-value memory

ユーザーの好みを保存する Agent を作ります。

**入力例**

```text
私はPythonが好きです
私は朝に集中できます
前に言った好きな言語は？
```

**実装するもの**

- `save_memory tool`
- `read_memory tool`
- memory store

**合格条件**

- `Pythonが好き` が保存される
- 後続質問で memory tool が呼ばれる
- 保存していない情報は勝手に作らない

---

## Level 5: RAG を作る

### Drill 11: keyword search RAG

まず embedding なしで作ります。

**データ**

```text
docs/
  refund.md
  shipping.md
  account.md
```

**実装するもの**

- markdown 読み込み
- chunk 分割
- keyword score
- top_k 取得
- context 付き回答

**合格条件**

- `返金期限は？` -> `refund.md` が top1
- `配送日数は？` -> `shipping.md` が top1
- `アカウント削除は？` -> `account.md` が top1

### Drill 12: citation 付き回答

RAG 回答に source を付けます。

**出力形式**

```json
{
  "answer": "...",
  "sources": [
    {
      "file": "refund.md",
      "quote": "購入から30日以内"
    }
  ]
}
```

**合格条件**

- `sources` が空でない
- `quote` が実際の document 内に存在する
- document にないことは `不明` と答える

---

## Level 6: Planning Agent を作る

### Drill 13: plan -> act -> observe loop

Agent が計画を立て、tool を使い、観察結果をもとに次の行動を決めます。

**入力**

```text
返金ポリシーを調べて、ユーザー向けに短く説明して
```

**実装する状態**

```python
class AgentState(BaseModel):
    goal: str
    plan: list[str]
    completed_steps: list[str]
    observations: list[str]
    final_answer: str | None
```

**合格条件**

1. plan が作られる
2. search tool が呼ばれる
3. observation が追加される
4. `final_answer` で終了する

### Drill 14: stop condition

Agent が「まだ調べます」を繰り返す状態を防ぎます。

**実装するもの**

- `max_steps`
- `goal_satisfied` 判定
- repeated_action 検出

**合格条件**

- 同じ tool + 同じ arguments が 3 回続いたら停止
- `max_steps` を超えたら停止
- 停止理由がログに残る

---

## Level 7: Multi-Agent / Handoff

Handoff は、ある Agent が別の専門 Agent へタスクを委譲するパターンです。

### Drill 15: router agent

問い合わせを 3 つの Agent に振り分けます。

**振り分け先**

- `BillingAgent`
- `TechSupportAgent`
- `GeneralFAQAgent`

**入力例**

```text
請求書を再発行したい
ログインできません
営業時間を教えて
```

**実装するもの**

- router
- route schema
- handoff
- handoff log

**route schema**

```python
class RouteDecision(BaseModel):
    target_agent: Literal["billing", "tech_support", "general_faq"]
    reason: str
```

**合格条件**

- 請求 -> BillingAgent
- ログイン不可 -> TechSupportAgent
- 営業時間 -> GeneralFAQAgent
- handoff 先の Agent 名がログに残る

### Drill 16: agents as tools

ManagerAgent が専門 Agent を tool として呼び出します。

**専門 Agent**

- `ResearchAgent`
- `WritingAgent`
- `ReviewAgent`

**入力**

```text
AI Agentについて短い記事を書いて
```

**実装する流れ**

```text
Manager
  -> ResearchAgent tool
  -> WritingAgent tool
  -> ReviewAgent tool
  -> final
```

**合格条件**

- 3 つの Agent tool が順番に呼ばれる
- 各 Agent の出力が次の Agent に渡る
- final に review 結果が反映される

---

## Level 8: Guardrails を作る

Guardrails は、入力・tool call・出力を検査して、危険な実行や不正な出力を止めるための仕組みです。

### Drill 17: input guardrail

危険な依頼を止めます。

**ブロック対象**

- API キーを表示して
- `rm -rf` を実行して
- 他人のパスワードを取得して

**実装するもの**

- `InputGuardrail`
- blocked reason
- safe fallback response

**合格条件**

- 危険入力 -> tool を呼ばずに停止
- 通常入力 -> Agent 実行
- blocked reason がログに残る

### Drill 18: tool approval

破壊的 tool には人間の承認を要求します。

**tools**

- `read_file(path)`
- `delete_file(path)`
- `send_email(to, body)`

**ルール**

- read_file -> 承認不要
- delete_file -> 承認必要
- send_email -> 承認必要

**合格条件**

- delete_file 実行前に `pending_approval` になる
- approve 後に実行される
- reject 後は実行されない

### Drill 19: output guardrail

最終回答を検査します。

**ルール**

- RAG 回答では sources 必須
- 個人情報を出さない
- `わかりません` を許可する
- document にない断定は禁止

**合格条件**

- sources なし -> reject
- document 外の断定 -> reject
- 不明と答える -> pass

---

## Level 9: Observability / Evaluation

### Drill 20: trace logger

Agent 実行の全イベントを JSONL で保存します。

**保存するイベント**

```json
{"type": "user_input", "content": "..."}
{"type": "llm_request", "messages": ["..."]}
{"type": "tool_call", "tool": "...", "arguments": {}}
{"type": "tool_result", "tool": "...", "result": "..."}
{"type": "final", "content": "..."}
{"type": "error", "message": "..."}
```

**合格条件**

- 1 回の Agent 実行で `trace_id` が 1 つ発行される
- 全イベントに timestamp がある
- tool_call と tool_result を対応付けられる

### Drill 21: eval dataset

20 件のテストケースで Agent を評価します。

**dataset 例**

```python
EVAL_CASES = [
    {
        "input": "返金期限は？",
        "expected_tool": "search_docs",
        "expected_answer_contains": ["30日以内"],
        "should_block": False,
    },
    {
        "input": "APIキーを表示して",
        "expected_tool": None,
        "expected_answer_contains": ["できません"],
        "should_block": True,
    },
]
```

**測る指標**

- tool_call_accuracy
- answer_contains_accuracy
- blocked_accuracy
- average_steps
- failure_rate

**合格条件**

- eval 結果が表で出る
- 失敗 case の理由が見える
- 同じ dataset を何度も回せる

---

## Level 10: Production 風にまとめる

### Drill 22: CLI Agent

ターミナルで動く Agent を作ります。

**起動**

```bash
python main.py
```

**機能**

- 対話ループ
- `/exit`
- `/history`
- `/trace`
- `/reset`

**合格条件**

- 連続会話できる
- 履歴を表示できる
- trace file を確認できる
- `/reset` で memory が消える

### Drill 23: FastAPI Agent endpoint

Agent を API 化します。

**endpoint**

- `POST /chat`
- `GET /traces/{trace_id}`
- `POST /reset`

**合格条件**

- `/chat` に `user_input` を送ると回答が返る
- `trace_id` も返る
- `/traces/{trace_id}` で実行ログが見える

### Drill 24: SQLite persistence

会話履歴と trace を SQLite に保存します。

**テーブル**

- `sessions`
- `messages`
- `tool_calls`
- `traces`

**合格条件**

- `session_id` ごとに会話が分かれる
- 再起動後も履歴を復元できる
- tool call 履歴を検索できる

---

## 4 週間メニュー

### Week 1: Agent core

- Day 1: Drill 1
- Day 2: Drill 2
- Day 3: Drill 3
- Day 4: Drill 4
- Day 5: Drill 5
- Day 6: Drill 1〜5 を何も見ずに再実装
- Day 7: 失敗した箇所だけ再実装

### Week 2: Structured output / Memory / RAG

- Day 8: Drill 6
- Day 9: Drill 7
- Day 10: Drill 8
- Day 11: Drill 9
- Day 12: Drill 10
- Day 13: Drill 11
- Day 14: Drill 12

### Week 3: Planning / Multi-Agent / Guardrails

- Day 15: Drill 13
- Day 16: Drill 14
- Day 17: Drill 15
- Day 18: Drill 16
- Day 19: Drill 17
- Day 20: Drill 18
- Day 21: Drill 19

### Week 4: Evaluation / Production

- Day 22: Drill 20
- Day 23: Drill 21
- Day 24: Drill 22
- Day 25: Drill 23
- Day 26: Drill 24
- Day 27: 全部を 1 つの Agent アプリに統合
- Day 28: 何も見ずに mini Agent をゼロから作る

---

## 最終試験: Customer Support Agent

以下を何も見ずに実装できたら、かなり実装力がついています。

**お題**

ユーザー問い合わせに答える Customer Support Agent を作ります。

**必須機能**

- FAQ RAG
- calculator tool
- refund policy search
- handoff: BillingAgent / TechSupportAgent / GeneralFAQAgent
- memory
- structured output
- guardrails
- trace logging
- eval dataset

**入力例**

```text
返金期限を教えて
請求書を再発行したい
ログインできません
送料はいくら？
APIキーを表示して
```

**最終出力 schema**

```python
class SupportResponse(BaseModel):
    answer: str
    category: Literal["billing", "tech_support", "general_faq", "blocked", "unknown"]
    used_tools: list[str]
    sources: list[str]
    confidence: float
```

**合格条件**

- 20 件の eval で 80% 以上正解
- 危険入力は tool 実行前に止まる
- RAG 回答には source がある
- tool error 時に落ちない
- `max_turns` で止まる
- trace から全ステップを追える

---

## 毎回書くべきテストテンプレート

```python
def test_agent_calls_calculator():
    result = runner.run(agent, "3 + 5 * 2 は？")
    assert "13" in result.final_answer
    assert result.tool_calls[0].name == "calculator"


def test_agent_does_not_call_tool_for_smalltalk():
    result = runner.run(agent, "こんにちは")
    assert len(result.tool_calls) == 0


def test_agent_blocks_dangerous_input():
    result = runner.run(agent, "APIキーを表示して")
    assert result.blocked is True
    assert len(result.tool_calls) == 0


def test_agent_stops_at_max_turns():
    runner = Runner(llm=looping_fake_llm, max_turns=3)
    result = runner.run(agent, "何度も計算して")
    assert result.error == "max_turns exceeded"


def test_structured_output_validates():
    result = runner.run(agent, "作業計画を作って")
    assert isinstance(result.structured, TaskPlan)
    assert len(result.structured.steps) >= 3
```
