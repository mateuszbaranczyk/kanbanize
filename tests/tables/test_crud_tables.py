from pytest import fixture, raises

from kanbanize.schemas import TABLE_PREFIX, TableResponse
from kanbanize.tables.crud import TablesAdapter


@fixture
def table_adapter(mock_db):
    adapter = TablesAdapter(mock_db)
    return adapter


def test_create_table(table_adapter, table):
    result = table_adapter.create(table)
    assert isinstance(result, TableResponse)
    assert result.uuid.startswith(TABLE_PREFIX)


def test_get_table(table_adapter, table):
    new_table = table_adapter.create(table)
    result = table_adapter.get(new_table.uuid)
    assert isinstance(result, TableResponse)
    assert result.uuid == new_table.uuid


def test_get_table_name_error(table_adapter):
    uuid = "ta-test"
    with raises(NameError, match=f"No such document! {uuid}"):
        table_adapter.get(uuid)


def test_edit_table(table_adapter, table):
    table = table_adapter.create(table)
    new_name = "new name"
    data = {"name": new_name}

    result = table_adapter.edit(table.uuid, data)
    assert result.name == new_name
