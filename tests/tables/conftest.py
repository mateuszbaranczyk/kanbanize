from pytest import fixture

from kanbanize.schemas import Table


@fixture
def table():
    table = Table(name="test_table", tasks=[])
    return table
