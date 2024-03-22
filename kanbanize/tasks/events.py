# TODO
# send message to queue
# save event in db?


def send_message(task, table_uuid):
    if table_uuid:
        send_event(task)


def send_event(task):
    pass
