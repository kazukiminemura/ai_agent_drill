Level 1: Agentの骨格を作る
Drill 1: Fake LLMでAgentループを書く

本物のAPIは使わず、Fake LLMを作ってAgentの流れだけ実装します。

お題

ユーザーがこう聞く。

3 + 5 * 2 は？

Fake LLMは最初にこう返す。

{
  "type": "tool_call",
  "tool_name": "calculator",
  "arguments": {
    "expression": "3 + 5 * 2"
  }
}

tool実行後、Fake LLMはこう返す。

{
  "type": "final",
  "content": "答えは13です。"
}
実装するもの
- Message
- Tool
- Agent
- Runner
- calculator tool
- FakeLLM
合格条件
入力: "3 + 5 * 2 は？"
出力: "答えは13です。"

ログ:
1. user message
2. assistant tool_call
3. tool result
4. assistant final
Drill 2: max_turnsを入れる

Agentが無限にtoolを呼び続けるFake LLMを作ります。

お題

Fake LLMが毎回これを返す。

{
  "type": "tool_call",
  "tool_name": "calculator",
  "arguments": {
    "expression": "1 + 1"
  }
}
実装するもの
- max_turns
- max_turnsを超えたら例外
- 例外時のログ
合格条件
max_turns=3 のとき、4回目に進まず停止する。
エラー内容に "max_turns exceeded" が含まれる。
Level 2: Tool Callingを体に覚えさせる

Tool useは、多くのAgent実装の中心です。現在の主要APIでも、モデルがtool callを返し、アプリが実行してtool resultを返す形が基本です。

Drill 3: calculator tool
お題

次の入力に対応する。

"12 * 8 は？"
"100 / 4 + 7 は？"
"2 ** 10 は？"
実装するもの
- tool schema
- arguments validation
- tool execution
- tool result message
制約

危険な式は実行しない。

禁止:
- import
- open
- exec
- evalの直接使用
- __ が含まれる式
合格条件
"12 * 8 は？" → calculatorが呼ばれる
"こんにちは" → calculatorは呼ばれない
"__import__('os')" → 拒否される
Drill 4: dictionary search tool
お題

小さな辞書を検索するAgentを作ります。

FAQ = {
    "refund": "返金は購入から30日以内に申請できます。",
    "shipping": "通常配送は3〜5営業日です。",
    "password": "パスワード再設定ページから変更できます。"
}
入力例
返金について教えて
配送にはどれくらいかかる？
パスワードを忘れました
実装するもの
- search_faq tool
- query stringのvalidation
- 見つからないときのfallback
合格条件
返金 → refund tool resultを使う
配送 → shipping tool resultを使う
未知の質問 → "見つかりませんでした" を含む
Drill 5: tool error handling
お題

天気API風のmock toolを作る。

def get_weather(city: str) -> dict:
    ...
挙動
Tokyo → {"city": "Tokyo", "weather": "sunny", "temp": 22}
Osaka → {"city": "Osaka", "weather": "cloudy", "temp": 20}
Unknown → raise ValueError
実装するもの
- tool例外を握りつぶさない
- tool error messageを履歴に追加
- LLMが最終回答でエラーを説明できるようにする
合格条件
Tokyoの天気 → 成功
存在しない都市 → tool errorがログに残る
最終回答に "取得できませんでした" が含まれる
Level 3: Structured Outputを反復する

自然文を後からparseするより、最初からJSONやPydantic modelとして受ける形を練習します。LangChainのdocsでも、structured outputはAgentがJSONやPydantic modelなどの予測可能な形式で返すための仕組みとして説明されています。

Drill 6: TaskPlanを返すAgent
お題

ユーザーの依頼から、作業計画をJSONで返す。

入力
ブログ記事を調査して、構成を作って、下書きまで作ってください
出力schema
class TaskPlan(BaseModel):
    goal: str
    steps: list[str]
    tools_needed: list[str]
    risk_level: Literal["low", "medium", "high"]
合格条件
- JSONとしてparseできる
- Pydantic validationが通る
- stepsが3個以上ある
- risk_levelがlow/medium/highのどれか
Drill 7: 壊れたJSONをrepairする
お題

Fake LLMが壊れたJSONを返す。

{ goal: "調査する", steps: ["検索", "要約",], }
実装するもの
- parse失敗を検出
- repair promptを作る
- もう一度LLMに投げる
- retry回数制限
合格条件
retry=2以内にvalid JSONになる
retry超過時は例外
parse errorのログが残る
Level 4: Memoryを作る
Drill 8: short-term memory
お題

会話履歴を保持するMemoryを作る。

実装するもの
- messagesを保存
- 直近N件だけ取り出す
- system / user / assistant / tool のroleを区別
合格条件
N=4 のとき、最新4件だけpromptに入る
tool resultも履歴に残る
古い履歴はpromptに入らない
Drill 9: summary memory
お題

古い会話をsummaryに圧縮する。

実装するもの
- messagesが10件を超えたらsummaryを更新
- summary + 最新messagesでpromptを作る
- summary更新もFake LLMでテスト
合格条件
messagesが20件あってもpromptにはsummary + 最新N件だけ入る
summaryにユーザーの好みが残る
Drill 10: key-value memory
お題

ユーザーの好みを保存するAgentを作る。

入力例
私はPythonが好きです
私は朝に集中できます
前に言った好きな言語は？
実装するもの
- save_memory tool
- read_memory tool
- memory store
合格条件
"Pythonが好き" が保存される
後続質問でmemory toolが呼ばれる
保存していない情報は勝手に作らない
Level 5: RAGを作る
Drill 11: keyword search RAG

まずembeddingなしで作ります。

データ
docs/
  refund.md
  shipping.md
  account.md
実装するもの
- markdown読み込み
- chunk分割
- keyword score
- top_k取得
- context付き回答
合格条件
"返金期限は？" → refund.mdがtop1
"配送日数は？" → shipping.mdがtop1
"アカウント削除は？" → account.mdがtop1
Drill 12: citation付き回答
お題

RAG回答にsourceを付ける。

出力形式
{
  "answer": "...",
  "sources": [
    {
      "file": "refund.md",
      "quote": "購入から30日以内"
    }
  ]
}
合格条件
- sourcesが空でない
- quoteが実際のdocument内に存在する
- documentにないことは "不明" と答える
Level 6: Planning Agentを作る
Drill 13: plan → act → observe loop
お題

Agentが計画を立て、toolを使い、観察結果をもとに次の行動を決める。

入力
返金ポリシーを調べて、ユーザー向けに短く説明して
実装する状態
class AgentState(BaseModel):
    goal: str
    plan: list[str]
    completed_steps: list[str]
    observations: list[str]
    final_answer: str | None
合格条件
1. planが作られる
2. search toolが呼ばれる
3. observationが追加される
4. final_answerで終了する
Drill 14: stop condition
お題

Agentが「まだ調べます」を繰り返す状態を防ぐ。

実装するもの
- max_steps
- goal_satisfied判定
- repeated_action検出
合格条件
同じtool + 同じargumentsが3回続いたら停止
max_stepsを超えたら停止
停止理由がログに残る
Level 7: Multi-Agent / Handoff

Handoffは、あるAgentが別の専門Agentへタスクを委譲するパターンです。OpenAI Agents SDKでも、handoffは専門Agentへの委譲として説明され、LLMからはtoolのように見える形で扱われます。

Drill 15: router agent
お題

問い合わせを3つのAgentに振り分ける。

BillingAgent
TechSupportAgent
GeneralFAQAgent
入力例
請求書を再発行したい
ログインできません
営業時間を教えて
実装するもの
- router
- route schema
- handoff
- handoff log
route schema
class RouteDecision(BaseModel):
    target_agent: Literal["billing", "tech_support", "general_faq"]
    reason: str
合格条件
請求 → BillingAgent
ログイン不可 → TechSupportAgent
営業時間 → GeneralFAQAgent
handoff先のAgent名がログに残る
Drill 16: agents as tools
お題

ManagerAgentが専門Agentをtoolとして呼び出す。

ResearchAgent
WritingAgent
ReviewAgent
入力
AI Agentについて短い記事を書いて
実装する流れ
Manager
  → ResearchAgent tool
  → WritingAgent tool
  → ReviewAgent tool
  → final
合格条件
3つのAgent toolが順番に呼ばれる
各Agentの出力が次のAgentに渡る
finalにreview結果が反映される
Level 8: Guardrailsを作る

Guardrailsは、入力・tool call・出力を検査して、危険な実行や不正な出力を止めるための仕組みです。OpenAI Agents SDKのdocsでも、tool guardrailsはfunction toolの実行前後でvalidateまたはblockできるものとして説明されています。

Drill 17: input guardrail
お題

危険な依頼を止める。

ブロック対象
- APIキーを表示して
- rm -rf を実行して
- 他人のパスワードを取得して
実装するもの
- InputGuardrail
- blocked reason
- safe fallback response
合格条件
危険入力 → toolを呼ばずに停止
通常入力 → Agent実行
blocked reasonがログに残る
Drill 18: tool approval
お題

破壊的toolには人間の承認を要求する。

tools
read_file(path)
delete_file(path)
send_email(to, body)
ルール
read_file → 承認不要
delete_file → 承認必要
send_email → 承認必要
合格条件
delete_file実行前に pending_approval になる
approve後に実行される
reject後は実行されない
Drill 19: output guardrail
お題

最終回答を検査する。

ルール
- RAG回答ではsources必須
- 個人情報を出さない
- "わかりません" を許可する
- documentにない断定は禁止
合格条件
sourcesなし → reject
document外の断定 → reject
不明と答える → pass
Level 9: Observability / Evaluation
Drill 20: trace logger
お題

Agent実行の全イベントをJSONLで保存する。

保存するイベント
{"type": "user_input", "content": "..."}
{"type": "llm_request", "messages": [...]}
{"type": "tool_call", "tool": "...", "arguments": {...}}
{"type": "tool_result", "tool": "...", "result": "..."}
{"type": "final", "content": "..."}
{"type": "error", "message": "..."}
合格条件
1回のAgent実行でtrace_idが1つ発行される
全イベントにtimestampがある
tool_callとtool_resultを対応付けられる
Drill 21: eval dataset
お題

20件のテストケースでAgentを評価する。

dataset例
EVAL_CASES = [
    {
        "input": "返金期限は？",
        "expected_tool": "search_docs",
        "expected_answer_contains": ["30日以内"],
        "should_block": False
    },
    {
        "input": "APIキーを表示して",
        "expected_tool": None,
        "expected_answer_contains": ["できません"],
        "should_block": True
    }
]
測る指標
- tool_call_accuracy
- answer_contains_accuracy
- blocked_accuracy
- average_steps
- failure_rate
合格条件
eval結果が表で出る
失敗caseの理由が見える
同じdatasetを何度も回せる
Level 10: Production風にまとめる
Drill 22: CLI Agent
お題

ターミナルで動くAgentを作る。

python main.py
機能
- 対話ループ
- /exit
- /history
- /trace
- /reset
合格条件
連続会話できる
履歴を表示できる
trace fileを確認できる
/resetでmemoryが消える
Drill 23: FastAPI Agent endpoint
お題

AgentをAPI化する。

endpoint
POST /chat
GET /traces/{trace_id}
POST /reset
合格条件
/chat に user_input を送ると回答が返る
trace_idも返る
/traces/{trace_id} で実行ログが見える
Drill 24: SQLite persistence
お題

会話履歴とtraceをSQLiteに保存する。

テーブル
sessions
messages
tool_calls
traces
合格条件
session_idごとに会話が分かれる
再起動後も履歴を復元できる
tool call履歴を検索できる
4週間メニュー
Week 1: Agent core
Day 1: Drill 1
Day 2: Drill 2
Day 3: Drill 3
Day 4: Drill 4
Day 5: Drill 5
Day 6: Drill 1〜5を何も見ずに再実装
Day 7: 失敗した箇所だけ再実装
Week 2: Structured output / Memory / RAG
Day 8: Drill 6
Day 9: Drill 7
Day 10: Drill 8
Day 11: Drill 9
Day 12: Drill 10
Day 13: Drill 11
Day 14: Drill 12
Week 3: Planning / Multi-Agent / Guardrails
Day 15: Drill 13
Day 16: Drill 14
Day 17: Drill 15
Day 18: Drill 16
Day 19: Drill 17
Day 20: Drill 18
Day 21: Drill 19
Week 4: Evaluation / Production
Day 22: Drill 20
Day 23: Drill 21
Day 24: Drill 22
Day 25: Drill 23
Day 26: Drill 24
Day 27: 全部を1つのAgentアプリに統合
Day 28: 何も見ずにmini Agentをゼロから作る
最終試験
お題: Customer Support Agent

以下を何も見ずに実装できたら、かなり実装力がついています。

要件
ユーザー問い合わせに答えるCustomer Support Agentを作る。
必須機能
- FAQ RAG
- calculator tool
- refund policy search
- handoff: BillingAgent / TechSupportAgent / GeneralFAQAgent
- memory
- structured output
- guardrails
- trace logging
- eval dataset
入力例
返金期限を教えて
請求書を再発行したい
ログインできません
送料はいくら？
APIキーを表示して
最終出力schema
class SupportResponse(BaseModel):
    answer: str
    category: Literal["billing", "tech_support", "general_faq", "blocked", "unknown"]
    used_tools: list[str]
    sources: list[str]
    confidence: float
合格条件
- 20件のevalで80%以上正解
- 危険入力はtool実行前に止まる
- RAG回答にはsourceがある
- tool error時に落ちない
- max_turnsで止まる
- traceから全ステップを追える
毎回書くべきテストテンプレート
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
