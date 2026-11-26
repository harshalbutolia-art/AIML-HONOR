import csv
import os


class EmployeeManager:

    def __init__(self):
        self.file = "employees.csv"

        if not os.path.isfile(self.file):
            with open(self.file, "w", newline="") as f:
                data = csv.writer(f)
                data.writerow(["ID", "Name", "Department", "Salary"])

    def add_employee(self):
        emp_id = input("Enter ID: ")

        records = self.fetch_records()

        for row in records:
            if row["ID"] == emp_id:
                print("Employee already exists.")
                return

        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        salary = input("Enter Salary: ")

        with open(self.file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([emp_id, name, dept, salary])

        print("Record inserted successfully.")

    def fetch_records(self):
        with open(self.file, "r", newline="") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def display_employees(self):
        records = self.fetch_records()

        if len(records) == 0:
            print("Employee list is empty.")
            return

        print("\nEmployee Details")
        print("-" * 45)

        for row in records:
            print("ID:", row["ID"])
            print("Name:", row["Name"])
            print("Department:", row["Department"])
            print("Salary:", row["Salary"])
            print("-" * 45)

    def modify_employee(self):
        emp_id = input("Enter ID to modify: ")

        records = self.fetch_records()
        updated = False

        for row in records:
            if row["ID"] == emp_id:
                row["Name"] = input("Enter updated name: ")
                row["Department"] = input("Enter updated department: ")
                row["Salary"] = input("Enter updated salary: ")
                updated = True
                break

        if updated:
            self.write_records(records)
            print("Employee details modified.")
        else:
            print("Employee ID does not exist.")

    def remove_employee(self):
        emp_id = input("Enter ID to remove: ")

        records = self.fetch_records()
        new_records = []

        for row in records:
            if row["ID"] != emp_id:
                new_records.append(row)

        if len(records) == len(new_records):
            print("Employee not found.")
        else:
            self.write_records(new_records)
            print("Employee removed successfully.")

    def write_records(self, records):
        with open(self.file, "w", newline="") as f:
            columns = ["ID", "Name", "Department", "Salary"]
            writer = csv.DictWriter(f, fieldnames=columns)

            writer.writeheader()
            writer.writerows(records)


def main():

    obj = EmployeeManager()

    while True:

        print("\n===== EMPLOYEE MANAGEMENT =====")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Modify Employee")
        print("4. Remove Employee")
        print("5. Exit")

        option = input("Select an option: ")

        try:
            if option == "1":
                obj.add_employee()

            elif option == "2":
                obj.display_employees()

            elif option == "3":
                obj.modify_employee()

            elif option == "4":
                obj.remove_employee()

            elif option == "5":
                print("Exiting the program.")
                break

            else:
                print("Invalid selection.")

        except (OSError, csv.Error) as e:
            print("File handling error:", e)


if __name__ == "__main__":
    main()