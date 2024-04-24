FROM python:3.10

WORKDIR /

ENV PYTHONPATH "${PYTHONPATH}:/"
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ARG RUN_TESTS=False
ARG UNIT_TEST=False

CMD if [ "$RUN_TESTS" = "True" ]; then \
        python tests/test.py; \
    elif [ "$UNIT_TEST" = "True" ]; then \
        python src/algo/SimilaritySets_Test.py; \
    else \
        python -u src/bot/TeleMeetBot.py; \
    fi

# CMD ["python", "-u", "src/bot/TeleMeetBot.py"]
