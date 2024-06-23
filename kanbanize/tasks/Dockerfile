FROM python:3.10-slim

WORKDIR app/

COPY ./tasks kanbanize/
COPY . kanbanize

RUN pip install --no-cache-dir -r kanbanize/tasks/requirements.txt

EXPOSE 8888

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "kanbanize.tasks.tasks_rest:app", "-b", "0.0.0.0:8888"]