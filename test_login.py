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


def print_Heading(heading, width=70):
    print("=" * width)
    print(f"|{heading.center(width - 2)}|")
    print("=" * width)

def main():
    print_Heading("Login")
    HEPaS_1 = Pyro5.api.Proxy("PYRONAME:HEPaS1")  # use name server object lookup uri shortcut

    while True:
        student = input("Are you a current or former OUST student? (yes/no): ").lower()
        if student == "yes":
            student_id = input("Please enter student_id: ")
            password = input("Please enter password: ")
            try:
                print(HEPaS_1.login(student_id, password))
            except:
                print("login error")
            break

        elif student == "no":
            person_id = input("Please enter person_id: ")
            password = input("Please enter password: ")
            if person_id != "" and password != "":
                print("login success")
                break
            else:
                print("person_id and password cannot be empty. Try again.")
        else:
            print("Please enter either 'yes' or 'no'.")

if __name__ == "__main__":
    main()