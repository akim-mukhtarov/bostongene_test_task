FROM python:3.10

WORKDIR /app

COPY ./ ./

RUN pip install --no-cache-dir -r deployment/api/requirements.txt

EXPOSE 9000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "9000", "--log-level", "debug", "md5_service.api.app:app"]
