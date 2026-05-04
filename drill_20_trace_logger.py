import json
from datetime import datetime
from uuid import uuid4


class TraceLogger:
    def __init__(self):
        self.trace_id = str(uuid4())
        self.events: list[dict] = []

    def log(self, event_type: str, **data) -> None:
        self.events.append({
            "trace_id": self.trace_id,
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            **data,
        })

    def jsonl(self) -> str:
        return "\n".join(json.dumps(event, ensure_ascii=False) for event in self.events)


logger = TraceLogger()
logger.log("user_input", content="返金期限は？")
logger.log("tool_call", tool="search_docs", arguments={"query": "返金"})
logger.log("final", content="返金は30日以内です。")
print(logger.jsonl())
