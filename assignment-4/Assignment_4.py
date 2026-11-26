import sqlite3


def connect_database():
    con = sqlite3.connect("employees.db")

    con.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    con.commit()
    return con


def add_record(con):
    try:
        emp_id = int(input("Enter Employee ID: "))
        name = input("Enter Employee Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        sql = """
        INSERT INTO employee (id, name, department, salary)
        VALUES (?, ?, ?, ?)
        """

        con.execute(sql, (emp_id, name, department, salary))
        con.commit()

        print("Employee record added successfully.")

    except ValueError:
        print("Please enter valid numeric values.")

    except sqlite3.IntegrityError:
        print("Employee ID already exists.")


def show_records(con):
    cursor = con.execute("SELECT * FROM employee")
    data = cursor.fetchall()

    if len(data) == 0:
        print("No employee information available.")
        return

    print("\n------- EMPLOYEE DETAILS -------")

    for item in data:
        print(f"""
        Employee ID : {item[0]}
        Name        : {item[1]}
        Department  : {item[2]}
        Salary      : {item[3]}
        """)


def edit_record(con):
    try:
        emp_id = int(input("Enter ID of employee to update: "))

        result = con.execute(
            "SELECT id FROM employee WHERE id = ?", (emp_id,)
        ).fetchone()

        if result is None:
            print("Employee record not found.")
            return

        name = input("Enter updated name: ")
        department = input("Enter updated department: ")
        salary = float(input("Enter updated salary: "))

        con.execute("""
            UPDATE employee
            SET name = ?, department = ?, salary = ?
            WHERE id = ?
        """, (name, department, salary, emp_id))

        con.commit()
        print("Employee information updated.")

    except ValueError:
        print("Invalid input. Please enter correct values.")


def remove_record(con):
    try:
        emp_id = int(input("Enter Employee ID to delete: "))

        cursor = con.execute(
            "DELETE FROM employee WHERE id = ?", (emp_id,)
        )

        con.commit()

        if cursor.rowcount == 0:
            print("No matching employee found.")
        else:
            print("Employee record deleted.")

    except ValueError:
        print("Enter a valid Employee ID.")


def main():

    connection = connect_database()

    while True:

        print("\n===== EMPLOYEE RECORD SYSTEM =====")
        print("1. Add New Employee")
        print("2. View Employee Records")
        print("3. Edit Employee Details")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Choose an operation: ")

        if choice == "1":
            add_record(connection)

        elif choice == "2":
            show_records(connection)

        elif choice == "3":
            edit_record(connection)

        elif choice == "4":
            remove_record(connection)

        elif choice == "5":
            connection.close()
            print("Database connection terminated.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()