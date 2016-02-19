FROM python:2.7
COPY src/ /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","server.py"]
