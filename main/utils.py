from typing import Dict
import uuid
def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'*{key}*: {value}')

    return "\n".join(facts).join(['\n', '\n'])

    
def generate_token():
    return uuid.uuid4()