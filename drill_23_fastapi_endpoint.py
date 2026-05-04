try:
    from fastapi import FastAPI
except ModuleNotFoundError:
    FastAPI = None


def agent(user_input: str) -> dict:
    return {
        "answer": f"echo: {user_input}",
        "trace_id": "demo-trace",
    }


if FastAPI is None:
    print("FastAPI is not installed. Run: pip install fastapi uvicorn")
else:
    app = FastAPI()

    @app.post("/chat")
    def chat(payload: dict) -> dict:
        return agent(payload["user_input"])

    @app.get("/traces/{trace_id}")
    def trace(trace_id: str) -> dict:
        return {"trace_id": trace_id, "events": []}
