FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

ENTRYPOINT [ "./entrypoint.sh" ]

CMD [ "uv", "run", "." ]
