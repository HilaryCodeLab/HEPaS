"""
Jacob Vanderwiel (10536622)
Hilary Soong (10591936)
Lecturer: Dr Jitian XIAO
Campus: ECU Joondalup
Submission Date: 22/05/2024
"""

# File saved as HEPaS-client.py
import Pyro5.api


def print_heading(heading, width=70):
    print("=" * width)
    print(f"|{heading.center(width - 2)}|")
    print("=" * width)


def user_authentication(proxy):
    """Handles user authentication, returning student details if authenticated."""
    while True:
        student_status = input("Are you a current or former OUST student? (yes/no): ").lower()
        if student_status in ("yes", "no"):
            student_id = input("Please enter student_id: ")
            if student_status == "yes":
                first_name = input("Please enter first name: ")
                last_name = input("Please enter last name: ")
                oust_email = input("Please enter OUST email: ")
                auth = proxy.login(student_id, first_name, last_name, oust_email)
                return student_id, auth, student_status  # Simulate successful authentication
            return student_id, True, student_status  # Allow for non-students to test their scores
        print("Please enter either 'yes' or 'no'.")


def collect_scores():
    """Collects and returns a list of valid scores entered by the user, and retains unit codes."""
    scores = []
    unit_codes = []
    while True:
        entry = input("Enter a unit code and mark separated by a comma (type '-1' to finish): ")
        if entry.lower() == "-1":
            scores.append(-1)
            break
        try:
            unit_code, score_str = entry.split(',')
            score = float(score_str.strip())
            if 0 <= score <= 100:
                scores.append(score)  # Append only the score for evaluation
                unit_codes.append(unit_code)
            else:
                print("Please enter a valid score (0 to 100)")
        except ValueError:
            print("Invalid format. Please enter in the format 'unit_code, score'.")
    return scores, unit_codes


def main():
    hepas_proxy = Pyro5.api.Proxy("PYRONAME:HEPaS1")  # Pyro5 proxy to the HEPaS server
    print_heading("Login")
    student_id, auth, student_status = user_authentication(hepas_proxy)

    if auth:
        print_heading("Welcome to HEPaS")
        if student_status == "yes":
            while True:
                print("\n")
                print("1. Evaluate existing records")
                print("2. Display existing records")
                print("3. Add new records")
                print("4. Exit")
                choice = input("Choose an option (1-4): ")

                if choice == "1":
                    print_heading("Evaluate Existing Records")
                    print("...Contacting HEPaS Evaluation Server...")
                    print(hepas_proxy.evaluate_existing_records(student_id))
                elif choice == "2":
                    print_heading("Display Existing Records")
                    records = hepas_proxy.retrieve_existing_records(student_id)
                    if isinstance(records, str):
                        print(records)
                    else:
                        for record in records:
                            print(f"Course: {record['unit_code']}, Grade: {record['score']}")
                elif choice == "3":
                    print_heading("Add New Records")
                    while True:
                        entry = input("Enter a unit code and mark separated by a comma (type '-1' to finish): ")
                        if entry.lower() == "-1":
                            break
                        try:
                            unit_code, score_str = entry.split(',')
                            score = float(score_str.strip())
                            if 0 <= score <= 100:
                                response = hepas_proxy.add_unit_record(student_id, unit_code, score)
                                print(response)
                            else:
                                print("Please enter a valid score (0 to 100)")
                        except ValueError:
                            print("Invalid format. Please enter in the format 'unit_code, score'.")
                elif choice == "4":
                    print("Goodbye")
                    break
                else:
                    print("Invalid choice. Please choose a valid option.")
        else:
            scores, unit_codes = collect_scores()
            print_heading("Evaluation")
            print("...Contacting HEPaS Evaluation Server...")
            print(hepas_proxy.evaluate_Student(student_id, scores))


if __name__ == "__main__":
    main()