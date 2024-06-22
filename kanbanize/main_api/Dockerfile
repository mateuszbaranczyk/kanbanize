FROM python:3.10-slim

WORKDIR /kanbanize

COPY ./ /kanbanize/main_api
COPY ../ /kanbanize

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main_api.run:rest", "-b", "0.0.0.0:8000"]