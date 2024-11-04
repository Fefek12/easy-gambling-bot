import json

def l(id: str) -> bool:
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        data = {}
    
    if not id in data:
        data[id] = {"money": 1000}

        with open("users.json", "w") as f:
            json.dump(data, f)
    
    return True