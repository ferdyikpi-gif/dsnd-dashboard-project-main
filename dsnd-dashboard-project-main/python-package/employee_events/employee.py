# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
# (Not needed directly; QueryBase already inherits QueryMixin)

# Define a subclass of QueryBase
# called Employee
class Employee(QueryBase):
    # Set the class attribute `name`
    # to the string "employee"
    name = "employee"

    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    def names(self):
        # Query 3
        # Write an SQL query that selects two columns:
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data for all employees
        sql = "SELECT first_name || ' ' || last_name AS full_name, employee_id FROM employee"
        return self.query(sql)

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    def username(self, id):
        # Query 4
        # Write an SQL query that selects an employee's full name.
        # Use f-string formatting and a WHERE filter to return only the employee
        # with the given id.
        sql = f"SELECT first_name || ' ' || last_name AS full_name FROM employee WHERE employee_id = {id}"
        return self.query(sql)

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returned containing the execution of the sql query
    def model_data(self, id):
        sql = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        return self.pandas_query(sql)
