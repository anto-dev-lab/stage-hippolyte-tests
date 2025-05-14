from typing import List, Dict
from abstractions import load_test, convert_to_dictionnaries

def clear():
    print("\n" * 99)






###### EXO TEST #################################################

def print_test_details(test):
    # Affichage ici avec des prints :
    # ...
    print("blablabla")
    print("blablabla")
    print("blablabla")


    # Laisser le temps à l'utilisateur de voir l'affichage:
    input("\nPress 'enter' to continue to the next test ")

#################################################################






# NE PAS TOUCHER ################################################
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
            print_test_details(test_as_dict)

        elif user_choice == "2":
            pass

        elif user_choice == "3":
            pass

        elif user_choice == "exit":
            exit()

    else:
        header_msg = f"Unknown value, {test_as_dict['id']} was skipped..."
