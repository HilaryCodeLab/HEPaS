"""
Jacob Vanderwiel (10536622)
Hilary Soong (10591936)
Lecturer: Dr Jitian XIAO
Campus: ECU Joondalup
Submission Date: 22/05/2024
"""

# File saved as HEPaS-server-1.py
import Pyro5.api
import HEPaS_server_2 as db
import HEPaS_client as client

#Constants for readability
min_pass = 50
max_fails = 5
qualification_grade = 70
high_margin = 65
low_margin = 60
top_eight_qualification = 80
min_units = 15
end_mark = -1


@Pyro5.api.expose
class HEPaS1(object):
    # ******************************************************* new lines start ****************************************************************************************
    # def login(self, person_id, first_name, last_name, oust_email):
    #     if person_id != "" and first_name != "" and last_name != "" and oust_email != "":
    #         if db.read_from_table(person_id, first_name, last_name, oust_email):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False

    def login(self, person_id,  first_name, last_name, oust_email):
        if person_id != "" and first_name != "" and last_name != "" and oust_email != "":
            if db.retrieve_user_from_table(person_id, first_name, last_name, oust_email):
                return True
            else:
                return False
        else:
            return False

    def get_student_learning_record(self, person_id, first_name, last_name, oust_email):
        data = []
        student_unit_records = db.retrieve_user_from_table(person_id, first_name, last_name, oust_email)
        # student_unit_records = db.read_from_table(person_id, first_name, last_name, oust_email)
        # data.append(student_unit_records)
        for i in student_unit_records:
           # print(i["result_score"])
           data.append(i["result_score"])
        outcome = self.evaluate_Student(person_id, data)
        return outcome
        # print(outcome)

    # ******************************************************* new lines end ****************************************************************************************
    def double_Average(self, score_list):
        grade_marks = [i for i in score_list if i != end_mark]
        return sum(grade_marks) / len(grade_marks)

    def top_Eight(self, score_list):
        topScores = sorted(score_list, reverse=True)[:8]
        return sum(topScores) / len(topScores)

    def evaluate_Student(self, studentID, score_list):

        fail_marks = [i for i in score_list if i < min_pass and i != end_mark]
        average = round(self.double_Average(score_list), 2)
        top_eight = round(self.top_Eight(score_list), 2)

        if len(score_list) <= min_units:
            message = "completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!"
        elif len(fail_marks) > max_fails:
            message = "has 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!"
        elif average >= qualification_grade:
            message = "QUALIFIES FOR HONOURS STUDY!"
        elif 70 >= average >= 65 and top_eight >= 80:
            message = (f"with a top eight average of {top_eight}%, "
                       "QUALIFIES FOR HONOURS STUDY!")
        elif 70 >= average >= 65 and top_eight < 80:
            message = (f"with a top eight average of {top_eight}%, "
                       "MAY HAVE A GOOD CHANCE! Need further assessment!")
        elif 65 >= average >= 60 and top_eight >= 80:
            message = (f"with a top eight average of {top_eight}%,"
                       "MAY HAVE A CHANCE! Must be carefully reassessed with coordinator’s permission!")
        else:
            message = "DOES NOT QUALIFY FOR HONORS STUDY!"
        # new line
        outcome = f"{studentID}, Course Grade Average: {average}%, {message}"
        return outcome


def setup_server():
    print("...Starting Server...")
    daemon = Pyro5.server.Daemon()  # make a Pyro daemon
    ns = Pyro5.api.locate_ns()  # find the name server
    uri = daemon.register(HEPaS1)  # register the greeting maker as a Pyro object
    ns.register("HEPaS1", uri)  # register the object with a name in the name server
    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls


if __name__ == "__main__":
    setup_server()