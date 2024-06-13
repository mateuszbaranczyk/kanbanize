from kanbanize.schemas import TABLE_PREFIX, TableResponse


def test_create_table(client, table):
    table_dump = table.model_dump_json()
    response = client.post("/tables/create", data=table_dump)
    table_response = TableResponse(**response.json())

    assert response.status_code == 200
    assert table_response.name == table.name
    assert table_response.uuid.startswith(TABLE_PREFIX)


def test_get_table(client, table, mock_db):
    table_uuid = create_new_table(mock_db=mock_db, table=table).uuid

    response = client.get(f"/tables/get/{table_uuid}")

    assert response.status_code == 200


def create_new_table(mock_db, table) -> TableResponse:
    new_table = TableResponse(**table.model_dump())
    mock_db.collection("tables").document(new_table.uuid).set(
        new_table.model_dump()
    )
    return new_table
