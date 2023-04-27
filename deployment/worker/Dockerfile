FROM python:3.10

WORKDIR /worker

COPY ./ ./

RUN pip install --no-cache-dir -r deployment/worker/requirements.txt

CMD ["celery", "-A", "md5_service.worker.tasks", "worker", "-c", "1", "-E"]

