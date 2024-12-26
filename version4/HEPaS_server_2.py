import mysql.connector
from mysql.connector import errorcode

end_mark = -1

def retrieve_user_from_table(student_id, first_name, last_name, oust_email):
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


def get_existing_records(student_id):
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


def get_existing_score(student_id):
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


def add_new_record(student_id, unit_code, score):
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


def main():
    # retrieve_user_from_table("10591936", "john", "doe", "jd@our.oust.edu.au")
    retrieve_user_from_table("20241201", "Jim", "MAX", "j.max@our.oust.edu.au")


if __name__ == "__main__":
    main()