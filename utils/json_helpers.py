import json


def parse_json_response(text: str):
    """
    Parses JSON from a Claude response.
    Falls back to extracting the first valid array or dict if direct parse fails.
    Raises ValueError if all attempts fail.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue

    raise ValueError(f"No valid JSON found in response: {text[:300]}")
