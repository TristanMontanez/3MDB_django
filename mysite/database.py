import mysql.connector
import csv

from mysql.connector import Error
from typing import List


class Database:
    def __init__(self):
        self.__connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='P@ssw0rd2404',
            database='3MDB'
        )
        self.__cursor = self.__connection.cursor()

    def execute_query(self, query):
        """
        Executes query

        :param query: MySQL query
        :return:
        """

        try:
            self.__cursor.execute(query)
            self.__connection.commit()
            print(f'Query Success: "{query}"')
            return True
        except Error as err:
            print(f'Error in "{query}": {err}')
            return False

    def read_from_database(self, sql_filters: dict, sql_columns: List, sql_table: str):
        """
        Reads from database

        :param sql_filters: SQL Filters
        :param sql_columns: SQL Columns
        :param sql_table: SQL Table
        :return: List of entries
        """

        filters = ''
        filter_label = ''
        for key, value in sql_filters.items():
            filters += ' AND ' if filters else ''
            delimiter = '","'
            if type(value) == list:
                filters += f'{key} IN ("{delimiter.join(value)}")'
                filter_label += f'{", ".join(value)}'
            else:
                filters += f'{key} = "{value}"'
                filter_label += f'{value}'

        query = f'SELECT {", ".join(sql_columns)} FROM {sql_table}'
        query += f'WHERE {filters}' if filters else ''

        self.__cursor.execute(query)
        result =self.__cursor.fetchall()
        data = [sql_columns]
        for item in result:
            data_row = [str(item[0])]
            data_row.extend(item[1::])
            data.append(data_row)

        return data, filter_label

    def delete_item(self, sql_filters: dict, sql_table: str):
        """
        Deletes item based on sql_filter

        :param sql_filters: SQL Condition
        :param sql_table: SQL Table Name
        :return: query
        """
        filters = ''
        for key, value in sql_filters.items():
            filters += ' AND ' if filters else ''
            delimiter = '","'
            if type(value) is list:
                filters += f'{key} IN ("{delimiter.join(value)}")'
            else:
                filters += f'{key}="{value}"'

        query = f'DELETE FROM {sql_table} WHERE {filters}'
        print(query)
        if self.execute_query(query):
            return query
        else:
            return False

    def edit_item(self, sql_filters: dict, sql_table: str, sql_updates):
        """
        Edits item based on sql_updates

        :param sql_filters: SQL Condition
        :param sql_table: SQL Table Name
        :param sql_updates: SQL Updates
        :return: query
        """
        filters = ''
        for key, value in sql_filters.items():
            filters += ' AND ' if filters else ''
            delimiter = '","'
            if type(value) is list:
                filters += f'{key} IN ("{delimiter.join(value)}")'
            else:
                filters += f'{key}="{value}"'

        updates = ''
        for key, value in sql_updates.items():
            updates += ', ' if updates else ''
            delimiter = '","'
            if type(value) is list:
                updates += f'{key} IN ("{delimiter.join(value)}")'
            else:
                updates += f'{key}="{value}"'

        query = f'UPDATE {sql_table} SET {updates} WHERE {filters}'
        print(query)
        if self.execute_query(query):
            return query
        else:
            return False

    # def populate_db(self):
    #     with open('product_db.csv', newline='') as f:
    #         reader = csv.reader(f)
    #         for row in reader:
    #             row[0] = 'product_' + row[0]
    #             row[1] = row[1].replace('_', ' ')
    #             quoted = []
    #             for item in row:
    #                 quoted.append(f'"{item}"')
    #             values = ', '.join(quoted)
    #             query = f"INSERT INTO product_table (product_key, product_name, price) VALUES ({values})"
    #             self.execute_query(query)
    #             print(query)

