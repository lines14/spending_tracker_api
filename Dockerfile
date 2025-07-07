FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add bash alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev

RUN addgroup -g 1000 mygroup && adduser -u 1000 -G mygroup -S myuser
RUN chown -R myuser:mygroup /app

ENV PATH=$PATH:/home/myuser/.local/bin

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 777 /app

USER myuser

RUN echo "migrate() { if [ -n \"\$1\" ]; then alembic upgrade +\$1; else alembic upgrade head; fi; }" >> ~/.bashrc
RUN echo "downgrade() { if [ -n \"\$1\" ]; then alembic downgrade -\$1; else alembic downgrade base; fi; }" >> ~/.bashrc
RUN echo "alias migrate:fresh='alembic downgrade base && alembic upgrade head'" >> ~/.bashrc
RUN echo "alias seed='python database/config/seed.py'" >> ~/.bashrc
RUN echo "alias migration='python database/config/create_migration.py'" >> ~/.bashrc
RUN echo "alias seeder='python database/config/create_seeder.py'" >> ~/.bashrc

RUN echo 'alias currencies:update="python -c \"import asyncio; \
from scheduler.currency_rates_updater_schedule import CurrencyRatesUpdaterSchedule; \
asyncio.run(CurrencyRatesUpdaterSchedule().update_currency_rates())\""' >> ~/.bashrc

RUN /bin/sh -c "source ../home/myuser/.bashrc"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]