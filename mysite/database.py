import mysql.connector

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
        :return: None
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

    def populate_db(self):
        for i in range(5000):
            z = str(i).zfill(4)
            query = f'INSERT INTO test_table (full_name, age, position, office)' \
                    f' VALUES ("name_{z}", {z}, "position_{z}", "office_{z}")'
            self.execute_query(query)
