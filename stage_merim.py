import csv
import time
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver

def load_test() -> List[List[str]]:
    with open("tests.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        return list(reader)

def convert_to_dictionnaries(test_list: List[List[str]]) -> List[Dict[str, str]]:
    headers = test_list.pop(0)
    tests_as_dict: List[Dict[str, str]] = []

    for test in test_list:
        test_as_dict: Dict[str, str] = {}

        for idx, header in enumerate(headers):
            test_as_dict[header.lower()] = test[idx]

        tests_as_dict.append(test_as_dict)

    return tests_as_dict

def clear():
    print("\n" * 99)

def print_test_details(test):
    print(f"\n=== Test detail page ({test.get('id')})".upper())
    for key, value in test.items():
        if not value: continue
        print(f"{key}: {value}")

    # Laisser le temps à l'utilisateur de voir l'affichage:
    print("\nWrite 'exec' to execute this test ")
    print("\nPress 'enter' to continue to the next test")
    user_input = input("\nYour choice: ")

    return user_input == "exec"

def get_html_element_from_ui_text(ui_text):
    global driver

    try:
        return driver.find_element(By.XPATH, f"//*[contains(text(), {ui_text})]")

    except Exception as e:
        #print("Error:", e)
        return None

def execute(test, callback):
    global driver

    # Open the app
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options)
    driver.get("http://192.168.1.200:8585")
    ###

    input_data_as_list = test.get('input data').replace(" ", "").split(",")
    input_data_as_dict = {}
    for input_data in input_data_as_list:
        key = input_data.split("=")[0]
        value = input_data.split("=")[1]
        input_data_as_dict[key] = value

    for step in test.get('steps').split(" > "):
        execute_step = lambda: callback(step, input_data_as_dict)
        success = execute_step()
        if not success:
            print("Step was not executed correctly, stopping execution...")
            input("Press 'enter' to close the browser ")
            driver.close()
            return False

        time.sleep(0.5)

    # Close the app
    input("Press 'enter' to close the browser ")
    driver.close()

    return True

def click(html_ref):
    global driver

    target = None

    try:
        target = driver.find_element(By.ID, html_ref)
    except Exception as e:
        #print("Error:", e)
        pass

    if not target:
        print(f"Looking for an element with the text '{html_ref}'...")
        target = get_html_element_from_ui_text(html_ref)

    if not target:
        return False

    ActionChains(driver).click(target).perform()
    return True

def write(html_ref, to_write):
    global driver

    target = None

    try:
        target = driver.find_element(By.ID, html_ref)
    except Exception as e:
        #print("Error:", e)
        pass

    if not target:
        print(f"Looking for an element with the text '{html_ref}'...")
        target = get_html_element_from_ui_text(html_ref)

    if not target:
        return False

    target.send_keys(to_write)
    return True

def main(callback):
    global driver

    driver = None
    header_msg = None

    tests: List[List[str]] = load_test()
    tests_as_dict = convert_to_dictionnaries(tests)
    for test_as_dict in tests_as_dict:
        clear()

        if header_msg:
            print(f"\n>>> {header_msg}\n")
            header_msg = None

        print(f"\n=== {test_as_dict['id']} ===")
        print(f"1: See details")
        print(f"2: Execute")
        print(f"3: Skip")

        print(f"\n'exit' to quit")

        user_choice = input(f"\nYour choice: ")
        if user_choice.lower() in ["1","2","3","exit"]:
            if user_choice == "1":
                if print_test_details(test_as_dict):
                    success = execute(test_as_dict, callback)
                    header_msg = f"{test_as_dict['id']} executed."
                    if not success: header_msg += " But failed."

            elif user_choice == "2":
                success = execute(test_as_dict, callback)
                header_msg = f"{test_as_dict['id']} executed."
                if not success: header_msg += " But failed."

            elif user_choice == "3":
                header_msg = f"{test_as_dict['id']} skipped."

            elif user_choice == "exit":
                exit()

        else:
            header_msg = f"Unknown value, {test_as_dict['id']} was skipped..."

driver = None
