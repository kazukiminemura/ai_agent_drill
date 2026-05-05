import ast
import operator


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def validate_expression(expression: str) -> None:
    blocked = ["import", "open", "exec", "eval", "__"]
    if any(word in expression for word in blocked):
        raise ValueError("dangerous expression")


def evaluate(node: ast.AST) -> int | float:
    if isinstance(node, ast.Expression):
        return evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.left), evaluate(node.right))
    raise ValueError("unsupported expression")


def calculator(expression: str) -> int | float:
    validate_expression(expression)
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise ValueError("unsupported expression") from error
    return evaluate(tree)


class FakeLLM:
    def chat(self, user_input: str) -> dict:
        if "12 * 8" in user_input:
            return {
                "type": "tool_call",
                "content": {
                    "tool_name": "calculator",
                    "arguments": {"expression": "12 * 8"},
                },
            }
        return {"type": "final", "content": "calculator は使いません。"}


response = FakeLLM().chat("12 * 8 は？")
if response["type"] == "tool_call":
    print(calculator(**response["content"]["arguments"]))
else:
    print(response["content"])
