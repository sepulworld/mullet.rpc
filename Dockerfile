FROM python:3.10.4-buster

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13 

# Install gpcurl
COPY install-grpcurl.sh /root/install-grpcurl.sh
RUN chmod +x /root/install-grpcurl.sh
RUN /root/install-grpcurl.sh

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
RUN useradd mulletrpc 

WORKDIR /home/mulletrpc

COPY poetry.lock pyproject.toml /home/mulletrpc

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY app app
COPY migrations migrations

COPY mulletrpc.py config.py boot.sh ./
RUN chmod a+x boot.sh
RUN chown -R mulletrpc:mulletrpc ./
USER mulletrpc 

EXPOSE 5000/tcp

ENV FLASK_APP mulletrpc.py
ENV PYTHONPATH=/app/
ENTRYPOINT ["./boot.sh"]
