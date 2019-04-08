import tempfile
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

    def test_build_view_from_table_with_database_name(self):
        table = Table()\
            .with_database_name("dev")\
            .with_name("POSTS")\
            .with_column("id", "INTEGER", "not null")\
            .with_column("title", "varchar(10)", "not null")

        view = table.build_view()
        view.with_database_name("dev_views")
        view.with_name("POSTS_VIEW")
        view.select_column("title")
        view.with_action("CREATE")

        statement = view.build()

        expected_statement = """
CREATE VIEW dev_views.POSTS_VIEW
AS
SELECT
title
FROM dev.POSTS;""".strip()
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

    def test_chain_calls(self):
        statement = Table()\
            .with_name("POSTS")\
            .with_column("id", "INTEGER", "not null")\
            .with_column("title", "varchar(10)", "not null")\
            .with_column("author", "varchar(20)")\
            .build_view()\
            .with_name("POSTS_VIEW")\
            .select_column("title")\
            .select_column("author")\
            .with_action("CREATE")\
            .build()

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

    def test_to_file_from_view(self):
        file = tempfile.NamedTemporaryFile()

        Table()\
            .with_name("POSTS")\
            .with_column("id", "INTEGER", "not null")\
            .with_column("title", "varchar(10)", "not null")\
            .build_view()\
            .with_name("POSTS_VIEW")\
            .select_column("title")\
            .with_action("CREATE")\
            .to_path(file.name)

        expected_statement = """
CREATE VIEW POSTS_VIEW
AS
SELECT
title
FROM POSTS;""".strip()
        with open(file.name, 'r') as the_file:
            content = the_file.read()
            self.assertEqual(expected_statement, content)


    def test_with_header(self):
        statement = Table() \
            .with_name("POSTS") \
            .with_column("id", "INTEGER", "not null") \
            .with_column("title", "varchar(10)", "not null") \
            .build_view() \
            .with_name("POSTS_VIEW") \
            .select_column("title") \
            .with_action("CREATE") \
            .with_header("/* This is comment */")\
            .build()

        expected_statement = """
/* This is comment */
CREATE VIEW POSTS_VIEW
AS
SELECT
title
FROM POSTS;""".strip()
        self.assertEqual(expected_statement, statement)
