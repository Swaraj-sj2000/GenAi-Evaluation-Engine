FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip setuptools wheel

FROM python:3.11-slim
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder --chown=appuser:appgroup /opt/venv /opt/venv
COPY --chown=appuser:appgroup . .
COPY --chown=appuser:appgroup entrypoint.sh .
RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
