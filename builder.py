class Column(object):
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

class Builder(object):
    def __init__(self):
        self.columns = []
        self.primary_key = None
    def with_column(self, name, datatype, desc=""):
        column = Column(name, datatype, desc)
        self.columns.append(column)
        return self
    def with_name(self, name):
        self.name = name
        return self
    def with_primary_key(self, key):
        self.primary_key = PrimaryKey(key)
        return self
    def build(self):
        pass

class ViewColumn(object):
    def __init__(self, name):
        self.name = name
    def build(self):
        return "{0}".format(self.name)

class ViewBuilder(object):
    def __init__(self, table_builder):
        self.table_builder = table_builder
        self.columns = []

    def with_name(self, name):
        self.name = name
        return self

    def with_action(self, action):
        self.action = action
        return self

    def select_column(self, name):
        self.columns.append(ViewColumn(name))
        return self

    def build(self):
        statements = []
        for column in self.columns:
            statements.append(column.build())
        if(len(statements) > 0):
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
class TableBuilder(Builder):
    def build(self):
        statements = []

        for column in self.columns:
            statements.append(column.build())

        if (self.primary_key):
            statements.append(self.primary_key.build())

        if(len(statements) > 0):
            statements_text = "\n  " + ",\n  ".join(statements) + "\n"
        else:
            statements_text = "\n"

        statement = """CREATE TABLE {0}({1});""".format(
            self.name,statements_text
        )
        return statement
    def to_view(self):
        return ViewBuilder(self)