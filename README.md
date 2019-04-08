# simple-sql-builder

Library to help build SQL with Python script.

## Usage

### Generate SQL to create table

```
Table() \
    .with_database_name("dev") \
    .with_name("POSTS") \
    .with_column("id", "INTEGER", "not null") \
    .with_column("title", "varchar(10)", "not null") \
    .with_header("""/* This is comment for table */""") \
    .to_path("/tmp/POSTS.sql")
```

The content of `/tmp/POSTS.sql` is below:
```
/* This is comment for table */
CREATE TABLE dev.POSTS(
  id INTEGER not null,
  title varchar(10) not null
);
```

### Generate SQL to create view from table
```
Table() \
    .with_database_name("dev")\
    .with_name("POSTS") \
    .with_column("id", "INTEGER", "not null") \
    .with_column("title", "varchar(10)", "not null") \
    .build_view()\
    .with_database_name("dev_view")\
    .with_name("POSTS_VIEW")\
    .select_column("title")\
    .with_header("This is comment for view")\
    .to_path("/tmp/POSTS_VIEW.sql")
```
The content of `/tmp/POSTS_VIEW.sql` is below:
```
/* This is comment for view */
CREATE VIEW dev_view.POSTS_VIEW
AS
SELECT
title
FROM dev.POSTS;
```

### More

Check the test cases for more usage.
