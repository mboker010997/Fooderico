FROM python:3.10

WORKDIR /

ENV PYTHONPATH "${PYTHONPATH}:/"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "src/bot/TeleMeetBot.py"]
