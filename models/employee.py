import sqlite3


class EmployeeModel:
    def __init__(self, _id, prod_hours, team_id):
        self._id = _id
        self.prod_hours = prod_hours
        self.team_id = team_id

    def json(self):
        return {"employeeID": self._id, "prodHours": self.prod_hours, "teamID": self.team_id}

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM employees WHERE employeeID = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def insert_employee(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO employees VALUES (?,?,?)"
        cursor.execute(query, (self._id,
                               self.prod_hours,
                               self.team_id))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE employees SET prodHours=?, teamID=? WHERE employeeID=?"
        cursor.execute(query, (self.prod_hours, self.team_id, self._id))
        connection.commit()
        connection.close()
