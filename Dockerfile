FROM python:3.8.10

RUN apt-get install apt-transport-https ca-certificates gnupg -y

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry install --no-interaction

CMD ['./docker-entrypoint.sh']
