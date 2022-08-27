FROM python:3.10.6-slim-bullseye
WORKDIR /app
COPY requirements.txt .

RUN python3 -m venv ./venv
ENV PATH="/app/venv/bin:$PATH"
    # This one updates the version of pip3
RUN pip3 install --upgrade pip && \
    # This makes sure to fetch from repo instead of using local cached one
    pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python && \
    chown -R python:python /app/
USER python
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application" ]
