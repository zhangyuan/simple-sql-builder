class ColumnNotExits(Exception):
    pass


class ViewColumn(object):
    def __init__(self, name):
        self.name = name

    def build(self):
        return "{0}".format(self.name)


class View(object):
    def __init__(self, table):
        self.table = table
        self.action = "CREATE"
        self.name = None
        self.columns = []
        self.database_name = None
        self.header = None

    def full_name(self):
        if self.database_name:
            name = "{0}.{1}".format(self.database_name, self.name)
        else:
            name = self.name
        return name

    def with_name(self, name):
        self.name = name
        return self

    def with_database_name(self, name):
        self.database_name = name
        return self

    def with_action(self, action):
        self.action = action
        return self

    def with_header(self, text):
        self.header = text
        return self

    def header_text(self):
        return self.header + "\n" if self.header else ""

    def select_column(self, name):
        available_columns = (column.name for column in self.table.columns)
        if name not in available_columns:
            raise ColumnNotExits("""Column '{0}' does not exist""".format(name))
        self.columns.append(ViewColumn(name))
        return self

    def build(self):
        statements = []
        for column in self.columns:
            statements.append(column.build())

        if len(statements) > 0:
            statements_text = ",\n".join(statements)
        else:
            statements_text = "\n"

        statement = """{0}{1} VIEW {2}
AS
SELECT
{3}
FROM {4};""".format(
            self.header_text(),
            self.action,
            self.full_name(),
            statements_text,
            self.table.full_name()
        )
        return statement

    def to_path(self, path):
        with open(path, 'w') as the_file:
            the_file.write(self.build())


if __name__ == '__main__':
    from table import Table
    Table() \
        .with_database_name("dev")\
        .with_name("POSTS") \
        .with_column("id", "INTEGER", "not null") \
        .with_column("title", "varchar(10)", "not null") \
        .build_view()\
        .with_database_name("dev_view")\
        .with_name("POSTS_VIEW")\
        .select_column("title")\
        .with_header("/* This is comment for view */")\
        .to_path("/tmp/POSTS_VIEW.sql")
