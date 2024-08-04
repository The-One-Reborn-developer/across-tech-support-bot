import json

def conversion_to_json(data) -> str:
    return json.dumps(data, ensure_ascii=False)