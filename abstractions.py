import csv
from typing import List, Dict

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

