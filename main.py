import time
import stage_merim
from typing import List, Dict

def get_html_ref(element):
    _ = {
        'log-in': 'log-in-btn',
        'merim-staff': 'social-keycloak-oidc',
        'user': 'username',
    }

    return _.get(element)

def get_action(word):
    _ = {
        'click': 'click',
        'enter': 'write',
        'entrer': 'write',
    }

    return _.get(word)

def execute_step(step, input_data):
    print(f"\nStep: {step}...")

    step_words = step.split(" ")
    csv_action = step_words[0]
    csv_target = "".join(step_words[1:])

    real_action = get_action(csv_action)
    real_target = get_html_ref(csv_target)

    if not real_action:
        print("Invalid action")
        return False

    if not real_target:
        print("Could not find the html element")
        return False

    if real_action == "click":
        success = stage_merim.click(real_target)
        if not success: return False

    elif real_action == "write":
        to_write = input_data.get(csv_target)
        success = stage_merim.write(real_target, to_write)
        if not success: return False

    return True

stage_merim.main(execute_step)
