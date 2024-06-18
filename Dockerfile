FROM python:3.11

WORKDIR /

RUN pip install "poetry==1.3.1"

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    rm -rf /var/lib/apt/lists/*

# Генерация ru_RU.UTF-8 локали
RUN locale-gen ru_RU.UTF-8

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV RUN_IN_DOCKER True

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8000
ENTRYPOINT ["bash","entrypoint.sh"]
CMD ["gunicorn", "backend.wsgi", "-b", "0.0.0.0:8000"]
