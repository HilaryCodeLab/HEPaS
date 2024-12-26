import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hepas_db"

)


def retrieve_user_from_table(person_id, first_name, last_name, email):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM student_info WHERE person_id=%s AND first_name=%s AND last_name=%s AND email=%s"
    val = (person_id, first_name, last_name, email, )
    mycursor.execute(sql, val)
    check_user = mycursor.fetchone()
    if check_user is None:
        print('Login Failure')
        return []
    # retrieve student unit record
    results = []
    query2 = "select result_score from student_unit WHERE person_id=%s"
    val2 = (person_id, )
    mycursor.execute(query2, val2)
    cols = mycursor.description
    unit_counts = 0
    for value in mycursor.fetchall():
        tmp = {}
        for(index, col) in enumerate(value):
            tmp[cols[index][0]] = col
        unit_counts += 1
        results.append(tmp)
    # print("total units: ", unit_counts)
    # print(results)
    return results


def main():
    # retrieve_user_from_table("10591936", "john", "doe", "jd@our.oust.edu.au")
    retrieve_user_from_table("20241201", "Jim", "MAX", "j.max@our.oust.edu.au")

if __name__ == "__main__":
    main()