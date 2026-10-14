import csv
import os


class Employee:

    def __init__(self):
        self.filename = "employees.csv"
        self.fields = ["id", "name", "department", "salary"]

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fields)

    def create(self):
        emp_id = input("Enter Employee ID: ")

        employees = self.get_all()

        for emp in employees:
            if emp["id"] == emp_id:
                print("Employee ID already exists.")
                return

        name = input("Enter Name: ")
        department = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([emp_id, name, department, salary])

        print("Employee added successfully.")

    def get_all(self):
        with open(self.filename, "r", newline="") as file:
            return list(csv.DictReader(file))

    def read(self):
        employees = self.get_all()

        if not employees:
            print("No employee records found.")
            return

        for emp in employees:
            print(
                f"ID: {emp['id']} | Name: {emp['name']} | "
                f"Department: {emp['department']} | "
                f"Salary: {emp['salary']}"
            )

    def update(self):
        emp_id = input("Enter Employee ID to update: ")
        employees = self.get_all()
        found = False

        for emp in employees:
            if emp["id"] == emp_id:
                emp["name"] = input("Enter new Name: ")
                emp["department"] = input("Enter new Department: ")
                emp["salary"] = input("Enter new Salary: ")
                found = True
                break

        if found:
            self.save_all(employees)
            print("Employee updated successfully.")
        else:
            print("Employee not found.")

    def delete(self):
        emp_id = input("Enter Employee ID to delete: ")
        employees = self.get_all()

        remaining = [
            emp for emp in employees
            if emp["id"] != emp_id
        ]

        if len(remaining) == len(employees):
            print("Employee not found.")
        else:
            self.save_all(remaining)
            print("Employee deleted successfully.")

    def save_all(self, employees):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(employees)


def main():
    employee = Employee()

    while True:
        print("\n--- Employee Management System ---")
        print("1. Create Employee")
        print("2. Read Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                employee.create()

            elif choice == "2":
                employee.read()

            elif choice == "3":
                employee.update()

            elif choice == "4":
                employee.delete()

            elif choice == "5":
                print("Program exited.")
                break

            else:
                print("Invalid choice.")

        except (OSError, csv.Error) as error:
            print("File error:", error)


if __name__ == "__main__":
    main()