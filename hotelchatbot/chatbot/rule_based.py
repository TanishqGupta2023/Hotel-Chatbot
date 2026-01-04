import json

def load_definitions():
    with open("definitions.json", "r") as file:
        return json.load(file)

def rule_based_answer(user_input):
    definitions = load_definitions()
    user_input = user_input.lower()
    for keyword, answer in definitions.items():
        if keyword in user_input:
            return answer
    return None
