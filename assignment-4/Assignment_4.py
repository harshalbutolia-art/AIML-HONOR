import sqlite3


class Employee:

    def __init__(self):
        self.conn = sqlite3.connect("employees.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)

        self.conn.commit()

    def create(self):
        try:
            emp_id = int(input("Enter Employee ID: "))
            name = input("Enter Name: ")
            department = input("Enter Department: ")
            salary = float(input("Enter Salary: "))

            self.cursor.execute(
                "INSERT INTO employee VALUES (?, ?, ?, ?)",
                (emp_id, name, department, salary)
            )

            self.conn.commit()
            print("Employee added successfully.")

        except ValueError:
            print("Please enter valid numeric values.")

        except sqlite3.IntegrityError:
            print("Employee ID already exists.")

    def read(self):
        self.cursor.execute("SELECT * FROM employee")
        employees = self.cursor.fetchall()

        if not employees:
            print("No employee records found.")
        else:
            for emp in employees:
                print(
                    f"ID: {emp[0]}, Name: {emp[1]}, "
                    f"Department: {emp[2]}, Salary: {emp[3]}"
                )

    def update(self):
        try:
            emp_id = int(input("Enter Employee ID to update: "))
            name = input("Enter New Name: ")
            department = input("Enter New Department: ")
            salary = float(input("Enter New Salary: "))

            self.cursor.execute("""
                UPDATE employee
                SET name = ?, department = ?, salary = ?
                WHERE id = ?
            """, (name, department, salary, emp_id))

            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("Employee updated successfully.")
            else:
                print("Employee not found.")

        except ValueError:
            print("Please enter valid numeric values.")

    def delete(self):
        try:
            emp_id = int(input("Enter Employee ID to delete: "))

            self.cursor.execute(
                "DELETE FROM employee WHERE id = ?",
                (emp_id,)
            )

            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("Employee deleted successfully.")
            else:
                print("Employee not found.")

        except ValueError:
            print("Please enter a valid Employee ID.")

    def close(self):
        self.conn.close()


def main():
    employee = Employee()

    while True:
        print("\n--- Employee Database Menu ---")
        print("1. Create Employee")
        print("2. Read Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            employee.create()

        elif choice == "2":
            employee.read()

        elif choice == "3":
            employee.update()

        elif choice == "4":
            employee.delete()

        elif choice == "5":
            employee.close()
            print("Program exited.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()