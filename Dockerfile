FROM python:3.13

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-root

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

