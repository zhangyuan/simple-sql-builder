from view import View


class TableColumn(object):
    def __init__(self, name, datatype, desc=""):
        self.name = name
        self.datatype = datatype
        self.desc = desc

    def build(self):
        return "{0} {1} {2}".format(self.name, self.datatype, self.desc)


class PrimaryKey(object):
    def __init__(self, key):
        self.key = key

    def build(self):
        return "PRIMARY KEY ({0})".format(self.key)


class TableBuilder(object):
    def __init__(self):
        self.columns = []
        self.primary_key = None

    def with_column(self, name, datatype, desc=""):
        column = TableColumn(name, datatype, desc)
        self.columns.append(column)
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_primary_key(self, key):
        self.primary_key = PrimaryKey(key)
        return self

    def build(self):
        statements = []

        for column in self.columns:
            statements.append(column.build())

        if self.primary_key:
            statements.append(self.primary_key.build())

        if len(statements) > 0:
            statements_text = "\n  " + ",\n  ".join(statements) + "\n"
        else:
            statements_text = "\n"

        statement = """CREATE TABLE {0}({1});""".format(
            self.name,statements_text
        )
        return statement

    def build_view(self):
        return View(self)