FROM python:3.10

WORKDIR /

ENV PYTHONPATH "${PYTHONPATH}:/"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ARG RUN_TESTS=False

CMD if [ "$RUN_TESTS" = "True" ]; then \
        python tests/test.py; \
    else \
        python -u src/bot/TeleMeetBot.py; \
    fi

# CMD ["python", "-u", "src/bot/TeleMeetBot.py"]
