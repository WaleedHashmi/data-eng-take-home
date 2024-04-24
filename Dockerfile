FROM python:3.11.7@sha256:63bec515ae23ef6b4563d29e547e81c15d80bf41eff5969cb43d034d333b63b8

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

# tomorrow app
COPY ./tomorrow /app/tomorrow

# fastAPI layer
COPY ./wrapper_api /app/wrapper_api
CMD ["uvicorn", "wrapper_api.main:app", "--host", "0.0.0.0", "--port", "8000"]