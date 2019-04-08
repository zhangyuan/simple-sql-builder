import unittest
from builder import TableBuilder

class TableBuilderTest(unittest.TestCase):

    def test_build_view_from_table(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        builder.with_column("id", "INTEGER", "not null")
        builder.with_column("title", "varchar(10)", "not null")

        view_builder = builder.to_view()
        view_builder.with_name("POSTS_VIEW")
        view_builder.select_column("title")
        view_builder.with_action("CREATE")

        statement = view_builder.build()

        expected_statement = """
CREATE VIEW POSTS_VIEW
AS
SELECT
title
FROM POSTS;""".strip()
        self.assertEqual(statement, expected_statement)

    def test_build_view_with_multiple_columns_from_table(self):
        builder = TableBuilder()
        builder.with_name("POSTS")
        builder.with_column("id", "INTEGER", "not null")
        builder.with_column("title", "varchar(10)", "not null")
        builder.with_column("author", "varchar(20)")

        view_builder = builder.to_view()
        view_builder.with_name("POSTS_VIEW")
        view_builder.select_column("title")
        view_builder.select_column("author")
        view_builder.with_action("CREATE")

        statement = view_builder.build()

        expected_statement = """
CREATE VIEW POSTS_VIEW
AS
SELECT
title,
author
FROM POSTS;""".strip()
        self.assertEqual(statement, expected_statement)        