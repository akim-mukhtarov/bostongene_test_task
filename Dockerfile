FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./md5_service ./md5_service

EXPOSE 9000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "9000", "--log-level", "debug", "md5_service.app:app"]
