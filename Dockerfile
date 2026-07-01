FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apk update && apk add bash alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev

RUN addgroup -g 1000 mygroup && adduser -u 1000 -G mygroup -S myuser
RUN chown -R myuser:mygroup /app

ENV PATH=$PATH:/home/myuser/.local/bin

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin:/home/myuser/.local/bin
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

RUN chmod -R 777 /app

USER myuser

RUN echo "migrate() { if [ -n \"\$1\" ]; then alembic upgrade +\$1; else alembic upgrade head; fi; }" >> ~/.bashrc
RUN echo "downgrade() { if [ -n \"\$1\" ]; then alembic downgrade -\$1; else alembic downgrade base; fi; }" >> ~/.bashrc
RUN echo "alias migrate:fresh='alembic downgrade base && alembic upgrade head'" >> ~/.bashrc
RUN echo "alias seed='python -m db.config.seed'" >> ~/.bashrc
RUN echo "alias migration='python -m db.config.create_migration'" >> ~/.bashrc
RUN echo "alias seeder='python -m db.config.create_seeder'" >> ~/.bashrc

RUN echo 'alias currencies:update="python -c \"import asyncio; \
from scheduler.currency_rates_updater_schedule import CurrencyRatesUpdaterSchedule; \
asyncio.run(CurrencyRatesUpdaterSchedule().update_currency_rates())\""' >> ~/.bashrc

RUN /bin/sh -c "source ../home/myuser/.bashrc"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]