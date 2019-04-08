class ColumnNotExits(Exception):
    pass


class ViewColumn(object):
    def __init__(self, name):
        self.name = name

    def build(self):
        return "{0}".format(self.name)


class View(object):
    def __init__(self, table_builder):
        self.table_builder = table_builder
        self.action = None
        self.name = None
        self.columns = []

    def with_name(self, name):
        self.name = name
        return self

    def with_action(self, action):
        self.action = action
        return self

    def select_column(self, name):
        available_columns = (column.name for column in self.table_builder.columns)
        if name not in available_columns:
            raise ColumnNotExits("""Column 'title' does not exist""")
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
        statement = """{0} VIEW {1}
AS
SELECT
{2}
FROM {3};""".format(
            self.action,
            self.name,
            statements_text,
            self.table_builder.name
        )
        return statement
