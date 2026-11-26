import sqlite3


class EmployeeDatabase:

    def __init__(self):
        self.database = sqlite3.connect("employees.db")
        self.db_cursor = self.database.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
        """
        self.db_cursor.execute(query)
        self.database.commit()

    def insert_employee(self):
        try:
            emp_id = int(input("Enter Employee ID: "))
            emp_name = input("Enter Employee Name: ")
            emp_dept = input("Enter Department: ")
            emp_salary = float(input("Enter Salary: "))

            query = "INSERT INTO employee VALUES (?, ?, ?, ?)"
            values = (emp_id, emp_name, emp_dept, emp_salary)

            self.db_cursor.execute(query, values)
            self.database.commit()

            print("Employee record inserted successfully.")

        except ValueError:
            print("Invalid input. Enter numeric ID and salary.")

        except sqlite3.IntegrityError:
            print("This Employee ID already exists.")

    def display_employees(self):
        query = "SELECT * FROM employee"
        self.db_cursor.execute(query)

        result = self.db_cursor.fetchall()

        if len(result) == 0:
            print("No records available.")
        else:
            print("\nEmployee Records")
            print("-" * 45)

            for record in result:
                print("Employee ID:", record[0])
                print("Employee Name:", record[1])
                print("Department:", record[2])
                print("Salary:", record[3])
                print("-" * 45)

    def modify_employee(self):
        try:
            emp_id = int(input("Enter Employee ID to modify: "))

            self.db_cursor.execute(
                "SELECT * FROM employee WHERE id = ?", (emp_id,)
            )

            if self.db_cursor.fetchone() is None:
                print("Employee record not found.")
                return

            new_name = input("Enter New Name: ")
            new_dept = input("Enter New Department: ")
            new_salary = float(input("Enter New Salary: "))

            query = """
            UPDATE employee
            SET name = ?, department = ?, salary = ?
            WHERE id = ?
            """

            self.db_cursor.execute(
                query, (new_name, new_dept, new_salary, emp_id)
            )

            self.database.commit()
            print("Employee information updated successfully.")

        except ValueError:
            print("Please enter valid numeric values.")

    def remove_employee(self):
        try:
            emp_id = int(input("Enter Employee ID to remove: "))

            self.db_cursor.execute(
                "DELETE FROM employee WHERE id = ?", (emp_id,)
            )

            self.database.commit()

            if self.db_cursor.rowcount == 0:
                print("Employee record not found.")
            else:
                print("Employee record deleted successfully.")

        except ValueError:
            print("Enter a valid Employee ID.")

    def close_connection(self):
        self.database.close()


def main():

    obj = EmployeeDatabase()

    while True:
        print("\n===== EMPLOYEE DATABASE SYSTEM =====")
        print("1. Insert Employee")
        print("2. Display Employees")
        print("3. Modify Employee")
        print("4. Remove Employee")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            obj.insert_employee()

        elif choice == "2":
            obj.display_employees()

        elif choice == "3":
            obj.modify_employee()

        elif choice == "4":
            obj.remove_employee()

        elif choice == "5":
            obj.close_connection()
            print("Database connection closed.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()