def get_weather(city: str) -> dict:
    data = {
        "Tokyo": {"city": "Tokyo", "weather": "sunny", "temp": 22},
        "Osaka": {"city": "Osaka", "weather": "cloudy", "temp": 20},
    }
    if city not in data:
        raise ValueError(f"unknown city: {city}")
    return data[city]


def run(city: str) -> list[dict]:
    messages = [{"role": "user", "content": f"{city} の天気は？"}]
    tool_call = {"tool_name": "get_weather", "arguments": {"city": city}}
    messages.append({"role": "assistant", "content": tool_call})

    try:
        result = get_weather(**tool_call["arguments"])
        messages.append({"role": "tool", "content": result})
        messages.append({"role": "assistant", "content": f"{city} は {result['weather']} です。"})
    except ValueError as error:
        messages.append({"role": "tool", "content": {"error": str(error)}})
        messages.append({"role": "assistant", "content": "天気を取得できませんでした。"})

    return messages


for message in run("Unknown"):
    print(message)
