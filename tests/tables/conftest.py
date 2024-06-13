from pytest import fixture

from kanbanize.schemas import Table
from kanbanize.tables.crud import TablesAdapter


@fixture
def table():
    table = Table(name="test_table", tasks=[])
    return table


@fixture
def table_adapter(mock_db):
    adapter = TablesAdapter(mock_db)
    return adapter
