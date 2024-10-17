FROM python:3.9-slim
RUN apt-get update && apt-get install -y stress
RUN pip install flask
COPY app.py /app/app.py
WORKDIR /app
CMD ["python", "app.py"]
