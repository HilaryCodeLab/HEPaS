"""
Jacob Vanderwiel (10536622)
Hilary Soong (10591936)
Lecturer: Dr Jitian XIAO
Campus: ECU Joondalup
Submission Date: 22/05/2024
"""

# File saved as HEPaS-server-1.py
import Pyro5.api
import mysql.connector
import HEPaS_server_2 as server2

# Constants for readability
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

    def login(self, student_id, first_name, last_name, oust_email):
        server2_proxy = Pyro5.api.Proxy("PYRONAME:HEPaS2")
        if student_id != "" and first_name != "" and last_name != "" and oust_email != "":
            if server2_proxy.retrieve_user_from_table(student_id, first_name, last_name, oust_email):
                print("Login Success")
                return True
            else:
                print("Login Failed")
                return False
        else:
            print("Login Failed")
            return False

    def double_Average(self, score_list):
        grade_marks = [i for i in score_list if i != end_mark]
        return sum(grade_marks) / len(grade_marks)

    def top_Eight(self, score_list):
        topScores = sorted(score_list, reverse=True)[:8]
        return sum(topScores) / len(topScores)

    def evaluate_Student(self, student_id, score_list):
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
        return f"{student_id}, Course Grade Average: {average}%, {message}"

    def evaluate_existing_records(self, student_id):
        server2_proxy = Pyro5.api.Proxy("PYRONAME:HEPaS2")
        result = server2_proxy.get_existing_score(student_id)
        scores = [record['score'] for record in result] + [end_mark]
        outcome = self.evaluate_Student(student_id, scores)
        return outcome

    def retrieve_existing_records(self, student_id):
        server2_proxy = Pyro5.api.Proxy("PYRONAME:HEPaS2")
        return server2_proxy.get_existing_records(student_id)

    def add_unit_record(self,student_id, unit_code, score):
        server2_proxy = Pyro5.api.Proxy("PYRONAME:HEPaS2")
        return server2_proxy.add_new_record(student_id, unit_code, score)
def setup_server():
    print("...Starting Server 1...")
    daemon = Pyro5.server.Daemon()  # make a Pyro daemon
    ns = Pyro5.api.locate_ns()  # find the name server
    uri = daemon.register(HEPaS1)  # register the greeting maker as a Pyro object
    ns.register("HEPaS1", uri)  # register the object with a name in the name server
    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls



if __name__ == "__main__":
    setup_server()