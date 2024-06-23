FROM python:3.10-slim

WORKDIR app/

COPY ./tables kanbanize/tables
COPY . kanbanize

RUN pip install --no-cache-dir -r kanbanize/tables/requirements.txt

EXPOSE 9999

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "kanbanize.tables.table_rest:app", "-b", "0.0.0.0:9999"]