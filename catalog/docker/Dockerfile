###########################
# BASE
###########################
FROM python:3.13-slim-bookworm as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install curl -y

ENV VENV_PATH="/opt/.venv" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

###########################
# DEPENDENCIES
###########################
FROM builder as dependencies

WORKDIR /opt

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH" \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1


RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

RUN find $VENV_PATH -maxdepth 1 -type l -delete

###########################
# DEPENDENCIES
###########################
FROM builder as production

WORKDIR /opt

ENV PATH="$VENV_PATH/bin:$PATH"

COPY . .

COPY --from=dependencies --chmod=777 $VENV_PATH $VENV_PATH
