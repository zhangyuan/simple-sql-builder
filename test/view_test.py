import unittest
from table import Table
from view import ColumnNotExits


class ViewTest(unittest.TestCase):
    def test_build_view_from_table(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")
        table.with_column("title", "varchar(10)", "not null")

        view = table.build_view()
        view.with_name("POSTS_VIEW")
        view.select_column("title")
        view.with_action("CREATE")

        statement = view.build()

        expected_statement = """
CREATE VIEW POSTS_VIEW
AS
SELECT
title
FROM POSTS;""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_view_with_multiple_columns_from_table(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")
        table.with_column("title", "varchar(10)", "not null")
        table.with_column("author", "varchar(20)")

        view = table.build_view()
        view.with_name("POSTS_VIEW")
        view.select_column("title")
        view.select_column("author")
        view.with_action("CREATE")

        statement = view.build()

        expected_statement = """
CREATE VIEW POSTS_VIEW
AS
SELECT
title,
author
FROM POSTS;""".strip()
        self.assertEqual(statement, expected_statement)

    def test_raise_error_when_column_does_not_exist_on_table(self):
        table = Table()
        table.with_name("POSTS")
        table.with_column("id", "INTEGER", "not null")

        view = table.build_view()
        view.with_name("POSTS_VIEW")
        with self.assertRaises(ColumnNotExits) as context:
            view.select_column("title")
        self.assertEqual('Column \'title\' does not exist', str(context.exception))

