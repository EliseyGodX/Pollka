FROM python:3.12.4

RUN apt-get update && apt-get install -y curl build-essential libpq-dev

ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "pollka.wsgi:application", "--chdir", "pollka", "--bind", "0.0.0.0:8000"]

