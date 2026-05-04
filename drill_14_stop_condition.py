def run(actions: list[dict], max_steps: int = 5) -> str:
    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")

    seen_repeats = 1
    previous = None

    for step, action in enumerate(actions, start=1):
        if step > max_steps:
            return "stopped: max_steps exceeded"

        if action == previous:
            seen_repeats += 1
        else:
            seen_repeats = 1

        if seen_repeats >= 3:
            return "stopped: repeated action"

        previous = action

    return "finished"


same_action = {"tool": "search", "arguments": {"query": "返金"}}
print(run([same_action, same_action, same_action]))
