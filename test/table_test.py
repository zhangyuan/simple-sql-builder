import unittest

from table import Table


class TableTest(unittest.TestCase):
    def test_build_empty_table(self):
        table = Table()
        table.with_name("POSTS")
        statement = table.build()

        expected_statement = """
CREATE TABLE POSTS(
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_table_with_one_column(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("title", "varchar(10)", "not null")

        statement = table.build()

        expected_statement = """
CREATE TABLE POSTS(
  title varchar(10) not null
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_overwrite_column(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("title", "varchar(10)", "not null")
        table.with_column("title", "varchar(30)", "not null")

        statement = table.build()

        expected_statement = """
CREATE TABLE POSTS(
  title varchar(30) not null
);""".strip()
        self.assertEqual(statement, expected_statement)


    def test_build_table_with_multiple_columns(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")
        table.with_column("title", "varchar(10)", "not null")

        statement = table.build()

        expected_statement = """
CREATE TABLE POSTS(
  id INTEGER not null,
  title varchar(10) not null
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_chain_calls(self):
        statement = Table()\
            .with_name("POSTS")\
            .with_column("id", "INTEGER", "not null")\
            .with_column("title", "varchar(10)", "not null")\
            .build()

        expected_statement = """
CREATE TABLE POSTS(
  id INTEGER not null,
  title varchar(10) not null
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_table_with_primary_key(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")
        table.with_primary_key("id")
        statement = table.build()

        expected_statement = """
CREATE TABLE POSTS(
  id INTEGER not null,
  PRIMARY KEY (id)
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_extend_from_existing_table(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")
        table.with_primary_key("id")

        extended_table = table.extend()

        extended_table.with_column("start_date", "DATE", "not null")

        self.assertEqual(table.build(), """
CREATE TABLE POSTS(
  id INTEGER not null,
  PRIMARY KEY (id)
);""".strip())

        self.assertEqual(extended_table.build(), """
CREATE TABLE POSTS(
  id INTEGER not null,
  start_date DATE not null,
  PRIMARY KEY (id)
);""".strip())
