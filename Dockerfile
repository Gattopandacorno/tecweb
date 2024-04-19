FROM python

ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=0 \
	POETRY_VIRTUALENVS_CREATE=0 \
	POETRY_CACHE_DIR=/tmp/poetry_cache \
	PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
	&& rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install poetry
RUN poetry install

EXPOSE 8000

WORKDIR /app/core/
RUN poetry run python -m manage migrate 

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]