import mysql.connector
import Pyro5.api

end_mark = -1

@Pyro5.api.expose
class Server2(object):
    def retrieve_user_from_table(self, student_id, first_name, last_name, oust_email):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='OSCLR',
                user='root',
                password=''  # Use your MySQL root password
            )

            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM students
            WHERE student_id = %s AND first_name = %s AND last_name = %s AND oust_email = %s
            """
            cursor.execute(query, (student_id, first_name, last_name, oust_email))
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result:
                return True
            else:
                return False

        except mysql.connector.Error as error:
            print(f"Failed to retrieve record from database: {error}")
            return False


    def get_existing_records(self, student_id):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='OSCLR',
                user='root',
                password=''  # Use your MySQL root password
            )

            cursor = connection.cursor(dictionary=True)
            query = "SELECT unit_code, score FROM unit_scores WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            if result:
                return result
            else:
                return "No records found."

        except mysql.connector.Error as error:
            print(f"Failed to retrieve records from database: {error}")
            return "Error retrieving records."


    def get_existing_score(self, student_id):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='OSCLR',
                user='root',
                password=''  # Use your MySQL root password
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT score FROM unit_scores WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            if result:
                return result
            else:
                return "No records found to evaluate."

        except mysql.connector.Error as error:
            print(f"Failed to evaluate records from database: {error}")
            return "Error evaluating records."


    def add_new_record(self, student_id, unit_code, score):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='OSCLR',
                user='root',
                password=''  # Use your MySQL root password
            )

            cursor = connection.cursor()
            query = "INSERT INTO unit_scores (student_id, unit_code, score) VALUES (%s, %s, %s)"
            cursor.execute(query, (student_id, unit_code, score))
            connection.commit()
            cursor.close()
            connection.close()
            return "Record added successfully."

        except mysql.connector.Error as error:
            print(f"Failed to add record to database: {error}")
            return "Error adding record."



def setup_server():
    print("...Starting Server 2...")
    daemon = Pyro5.server.Daemon()  # make a Pyro daemon
    ns = Pyro5.api.locate_ns()  # find the name server
    uri = daemon.register(Server2)  # register the greeting maker as a Pyro object
    ns.register("HEPaS2", uri)  # register the object with a name in the name server
    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls


if __name__ == "__main__":
    setup_server()