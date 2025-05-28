FROM python:3.12-slim

RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

RUN pip install --no-cache-dir --upgrade pip

COPY --chown=user requirements.txt /tmp/pip-tmp/

RUN pip install --no-cache-dir --upgrade -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp

WORKDIR $HOME/app

COPY --chown=user src $HOME/app

CMD [ "gunicorn", "main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:7860", "--workers", "5", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "--max-requests", "1000", "--max-requests-jitter", "50", "--timeout", "100", "--preload", "--worker-tmp-dir", "/dev/shm" ]