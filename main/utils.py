from typing import Dict
import uuid
from datetime import datetime


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        if(key != 'equal' and key != "diff"):
            facts.append(f'*{key}*: {value}')

    return "\n".join(facts).join(['\n', '\n'])


def facts_amount_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, value in user_data.items():
        facts.append(f'*{key}*: {facts_to_str(value)}')

    return "\n".join(facts).join(['\n', '\n'])

def multi_users_to_str(user_data: Dict[str, str]) -> str:
    facts = list()
    total=0
    for key, value in user_data.items():
        if( key == 'Amount'):
            facts.append(f"*{'Details'}*: \n")
            for x in range(0, len(value)):
                facts.append(f"  *{'Name'}*: {value[x+1]['name']}")
                facts.append(f"  *{'Amount'}*: {value[x+1]['amount']} \n")
                total=int(value[x+1]['amount'])+total
        elif(key != 'equal' and key != 'diff'):
            facts.append(f'*{key}*: {value}')
        
    facts.append(f"*{'Total'}*: {total}")
        
    return "\n".join(facts).join(['\n', '\n'])
    
def generate_token():
    return uuid.uuid4()