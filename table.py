from view import View


class TableColumn(object):
    def __init__(self, name, datatype, desc=""):
        self.name = name
        self.datatype = datatype
        self.desc = desc

    def duplicate(self):
        return TableColumn(self.name, self.datatype, self.desc)

    def build(self):
        return "{0} {1} {2}".format(self.name, self.datatype, self.desc)


class PrimaryKey(object):
    def __init__(self, key):
        self.key = key

    def build(self):
        return "PRIMARY KEY ({0})".format(self.key)


class Table(object):
    def __init__(self):
        self.database_name = None
        self.name = None
        self.columns = []
        self.primary_key = None
        self.header = None

    def extend(self):
        table = Table()
        table.name = self.name
        table.columns = list(column.duplicate() for column in self.columns)
        table.primary_key = self.primary_key
        return table

    def with_database_name(self, name):
        self.database_name = name
        return self

    def with_column(self, name, datatype, desc=""):
        existing_column = False
        for column in self.columns:
            if column.name == name:
                existing_column = True
                column.datatype = datatype
                column.desc = desc
        if not existing_column:
            column = TableColumn(name, datatype, desc)
            self.columns.append(column)

        return self

    def drop_column(self, name):
        self.columns = list(column for column in self.columns if column.name != name)
        return self

    def with_name(self, name):
        self.name = name
        return self

    def with_primary_key(self, key):
        self.primary_key = PrimaryKey(key)
        return self

    def with_header(self, text):
        self.header = text
        return self

    def full_name(self):
        if self.database_name:
            name = "{0}.{1}".format(self.database_name, self.name)
        else:
            name = self.name

        return name

    def header_text(self):
        return self.header + "\n" if self.header else ""

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

        statement = """{0}CREATE TABLE {1}({2});""".format(
            self.header_text(), self.full_name(), statements_text
        )
        return statement

    def to_path(self, path):
        with open(path, 'w') as the_file:
            the_file.write(self.build())

    def build_view(self):
        return View(self)