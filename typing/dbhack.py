import os
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring, redefined-outer-name
import logging
import sys
from typing import Generator
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, cursor
# pylint: disable=no-name-in-module
from pydantic import BaseModel
# pylint: enable=no-name-in-module

is_debugging = os.environ.get("DEBUG", "").lower() in ['1', 'true', 'yes']
logger = logging.getLogger()
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter("%(filename)s:%(lineno)d -- %(message)s"))
logger.handlers = [h]
logger.setLevel(logging.DEBUG if is_debugging else logging.INFO)


def execute_db(engine: Engine, *args, **kw):
    assert isinstance(engine, Engine), engine
    stacklevel = kw.pop('stacklevel', 2)
    logger.debug(args, stacklevel=stacklevel)
    sql, args = text(args[0]), args[1:]
    with engine.connect() as connection:
        # mypy doesn't know about connections
        # the "begin" context manager handles commit and rollback
        with connection.begin():                     # type: ignore
            return connection.execute(sql, *args)    # type: ignore


class Table(BaseModel, frozen=True):

    @classmethod
    def create(cls, eng: Engine):
        fsql = ", ".join([
            f"{f.name} {f.type_.__name__}"
            for f in cls.__fields__.values()
        ])
        execute_db(eng, f"CREATE TABLE {cls.__name__} ({fsql})", stacklevel=3)

    @classmethod
    def insert(cls, eng: Engine, **kw):
        obj = cls(**kw)
        fsql = ", ".join(map(repr, obj.dict().values()))
        execute_db(eng,
                   f"INSERT INTO {cls.__name__} VALUES ({fsql})",
                   stacklevel=3)

    @classmethod
    def select(cls, eng: Engine, *clauses) -> cursor.CursorResult:
        csql = " AND ".join(clauses)
        if csql:
            csql = f"WHERE {csql}"
        return execute_db(eng,
                          f"SELECT * FROM {cls.__name__} {csql}",
                          stacklevel=3)


class BaseQuery:
    """
    The SQL query string goes here in the docstring.
    Note this is NOT a pydantic model.
    Queries like this are iterators. They can query across multiple
    tables using JOINs.
    """
    def __init__(self, eng: Engine, **args):
        self.eng = eng    # later this will need to be SQLAlchemy connection
        self.args = args

    def __iter__(self) -> Generator[BaseModel, None, None]:
        result_class = getattr(self, 'Result')
        keys = result_class.__fields__.keys()
        for row in execute_db(self.eng, self.__doc__, self.args, stacklevel=3):
            yield result_class(**dict(zip(keys, row)))


#######################################


class Person(Table, frozen=True):
    name: str
    age: int
    # id: int     # auto increment???


class Book(Table, frozen=True):
    owner: str     # use ID instead?
    title: str


class YoungFolksWithBooks(BaseQuery):
    """
    SELECT DISTINCT    -- any person owning any books
        Person.name
    FROM Person
    JOIN Book
        ON Book.owner = Person.name
    WHERE age < :cutoff
    """
    class Result(BaseModel, frozen=True):
        name: str


####################################


@pytest.fixture
def testdb() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def scenario(testdb):
    assert isinstance(testdb, Engine), testdb
    Person.create(testdb)
    Person.insert(testdb, name='Alice', age=23)
    Person.insert(testdb, name='Bob', age=25)
    Person.insert(testdb, name='Charlie', age=12)
    Book.create(testdb)
    Book.insert(testdb, owner="Alice", title="Book 1")
    Book.insert(testdb, owner="Alice", title="Book 2")
    Book.insert(testdb, owner="Bob", title="Book 3")
    return testdb


def test_1_check_engine(scenario):
    eng = scenario
    assert isinstance(eng, Engine), eng


def test_2_everybody(scenario):
    eng = scenario
    # fetchone or fetchall from a table returns a list of tuples
    assert Person.select(eng).fetchall() == [
        ('Alice', 23), ('Bob', 25), ('Charlie', 12)
    ]


def test_3_select_with_where_clause(scenario):
    eng = scenario
    assert Person.select(eng, 'age > 24').fetchall() == [
        ('Bob', 25)
    ]


def test_4_queries_are_iterable(scenario):
    def is_iterable(thing):
        return iter(thing) is not None

    eng = scenario
    these = YoungFolksWithBooks(eng=eng, cutoff=24)
    assert is_iterable(these), these
    assert isinstance(list(these), list), these


def test_5_select_with_books(scenario):
    eng = scenario
    these = YoungFolksWithBooks(eng=eng, cutoff=24)
    assert [result.name for result in these] == ['Alice']
    assert list(YoungFolksWithBooks(eng=eng, cutoff=30)) == [
        YoungFolksWithBooks.Result(name='Alice'),
        YoungFolksWithBooks.Result(name='Bob')
    ]


if __name__ == "__main__":
    pytest.main([__file__])
