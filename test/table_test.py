import unittest

from table import TableBuilder


class ViewBuilderTest(unittest.TestCase):
    def test_build_empty_table(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        statement = builder.build()

        expected_statement = """
CREATE TABLE POSTS(
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_table_with_one_column(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        builder.with_column("title", "varchar(10)", "not null")

        statement = builder.build()

        expected_statement = """
CREATE TABLE POSTS(
  title varchar(10) not null
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_table_with_multiple_columns(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        builder.with_column("id", "INTEGER", "not null")
        builder.with_column("title", "varchar(10)", "not null")

        statement = builder.build()

        expected_statement = """
CREATE TABLE POSTS(
  id INTEGER not null,
  title varchar(10) not null
);""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_table_with_primary_key(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        builder.with_column("id", "INTEGER", "not null")
        builder.with_primary_key("id")
        statement = builder.build()

        expected_statement = """
CREATE TABLE POSTS(
  id INTEGER not null,
  PRIMARY KEY (id)
);""".strip()
        self.assertEqual(statement, expected_statement)