FROM python:3.9-slim
RUN apt-get update && apt-get install -y stress vim curl
RUN pip install flask
COPY app.py /app.py
CMD ["python", "app.py"]
