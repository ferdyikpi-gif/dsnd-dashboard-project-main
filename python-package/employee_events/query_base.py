# Import any dependencies needed to execute sql queries
import pandas as pd
from employee_events.sql_execution import QueryMixin

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase(QueryMixin):
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # Return an empty list
        return []
    
    # Define an `event_counts` method
    # that receives an `id` argument
    def event_counts(self, id):
        sql = f"""
        SELECT event_date, SUM(positive_events) as positive, SUM(negative_events) as negative
        FROM {self.name}
        JOIN employee_events USING({self.name}_id)
        WHERE {self.name}.{self.name}_id = {id}
        GROUP BY event_date
        ORDER BY event_date
        """
        # This method should return a pandas dataframe
        return self.pandas_query(sql)

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        # YOUR CODE HERE

    # Define a `notes` method that receives an id argument
    def notes(self, id):
        sql = f"""
        SELECT note_date, note
        FROM notes
        JOIN {self.name} ON notes.{self.name}_id = {self.name}.{self.name}_id
        WHERE {self.name}.{self.name}_id = {id}
        ORDER BY note_date
        """
        # This function should return a pandas dataframe
        return self.pandas_query(sql)
        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE
