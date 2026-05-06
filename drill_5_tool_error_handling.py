WEATHER = {
    "Tokyo": {"city": "Tokyo", "weather": "sunny", "temp": 22},
    "Osaka": {"city": "Osaka", "weather": "cloudy", "temp": 20},
}


def get_weather(city: str) -> dict:
    if city not in WEATHER:
        raise ValueError(f"unknown city: {city}")
    return WEATHER[city]


def run(city: str) -> list[dict]:
    messages = [{"role": "user", "content": f"{city} の天気は？"}]
    response = {
        "type": "tool_call",
        "content": {"tool_name": "get_weather", "arguments": {"city": city}},
    }
    call = response["content"]
    messages.append({"role": "assistant", "type": response["type"], "content": call})

    try:
        result = get_weather(**call["arguments"])
        messages.append({"role": "tool", "content": {"tool_name": call["tool_name"], "result": result}})
        messages.append({"role": "assistant", "type": "final", "content": f"{city} は {result['weather']} です。"})
    except ValueError as error:
        messages.append({"role": "tool", "content": {"tool_name": call["tool_name"], "error": str(error)}})
        messages.append({"role": "assistant", "type": "final", "content": "天気を取得できませんでした。"})

    return messages


for message in run("Tokyo"):
    print(message)

print("---")

for message in run("Unknown"):
    print(message)
