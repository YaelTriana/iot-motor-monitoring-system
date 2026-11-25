FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && useradd --create-home motormon
USER motormon

ENV PYTHONUNBUFFERED=1
# The compose file picks the entrypoint: motormon-simulator or motormon-collector.
CMD ["motormon-collector"]
