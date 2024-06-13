from kanbanize.schemas import TABLE_PREFIX, TableResponse


def test_create_table(client, table):
    table_dump = table.model_dump_json()
    response = client.post("/tables/create", data=table_dump)
    assert response.status_code == 200
    table_response = TableResponse(**response.json())

    assert response.status_code == 200
    assert table_response.name == table.name
    assert table_response.uuid.startswith(TABLE_PREFIX)
