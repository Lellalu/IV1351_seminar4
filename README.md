# IV1351_seminar4

This is seminar 4 of IV1351 Data Storage Paradigms. The goal of this assignment is learn to create a program that can access a database. We are required to develop part of Soundgood's website by using the database that we have created in previous seminars. The focus of this assignment is on database access, therefore, a command line user interface is sufficient rather than a web interface. The program is also required to handle ACID transactions properly, which means that it should call commit and rollback instead of auto-commit and the `SELECT FOR UPDATE` must be used when required.

## How to install dependecies

```Python
pip install -r requirements.txt
```

## How to the program


See all options by
```Python
python3 main.py -h
```

For example, to list all available `Violin` in the `soundgoods4` database with host `localhost` and username `postgres` can be done with
```Python
python3 main.py --host localhost --database soundgoods4 --user postgres --query_type list --kind Violin
```
