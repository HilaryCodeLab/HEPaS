"""
Jacob Vanderwiel (10536622)
Hilary Soong (10591936)
Lecturer: Dr Jitian XIAO
Campus: ECU Joondalup
Submission Date: 22/05/2024
"""
# File saved as HEPaS-client.py
# Imports
import Pyro5.api
from getpass import getpass
import HEPaS_server_2 as db

student_credentials = []

oust_student_password = ""
def print_Heading(heading, width=70):
    print("=" * width)
    print(f"|{heading.center(width - 2)}|")
    print("=" * width)

def main():
    score = 0
    score_list = []
    any_person_id = ""
    auth = False
    is_oust_student = False
    print_Heading("Login")
    HEPaS_1 = Pyro5.api.Proxy("PYRONAME:HEPaS1")  # use name server object lookup uri shortcut

    while True:
        student = input("Are you a current or former OUST student? (yes/no): ").lower()
        if student == "yes":
            person_id = input("Please enter person_id: ")
            first_name = input("Please enter first name: ")
            last_name = input("Please enter last name: ")
            oust_email = input("Please enter OUST email: ")
            login = HEPaS_1.login(person_id, first_name, last_name, oust_email)
            if login:
                print("Login success!")
                any_person_id = person_id
                auth = True
                is_oust_student = True
                break
            else:
                auth = False
                print("Login failure!")

        elif student == "no":
            person_id = input("Please enter person_id: ")
            if person_id != "":
                auth = True
                is_oust_student = False
                break
            else:
                print("person_id cannot be empty. Try again.")
        else:
            print("Please enter either 'yes' or 'no'.")

    if auth is True:
        print_Heading("Welcome to HEPaS")
        if is_oust_student:
            print_Heading("OUST student")
            # print(HEPaS_1.get_student_learning_record)
            print(HEPaS_1.get_student_learning_record(any_person_id, first_name, last_name, oust_email ))

        else:
            while score != -1:
                score = float(input("Please enter an integer as a unit mark (enter -1 to stop): "))
                if 0 < score < 100 or score == -1:
                    score_list.append(score)
                elif score != -1:
                    print("Please enter a valid score")
            print_Heading("Evaluation")
            print("...Contacting HEPaS Evaluation Server...")
            print(HEPaS_1.evaluate_Student(any_person_id, score_list))


if __name__ == "__main__":
    main()